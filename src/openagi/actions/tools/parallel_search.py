"""Opt-in, anonymous web search through Parallel's Search MCP server."""

import json
from importlib.metadata import version
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from uuid import uuid4

from pydantic import Field

from openagi.actions.base import BaseAction
from openagi.exception import OpenAGIException


class _SearchMCPClient:
    """Small synchronous client for this server's Streamable HTTP endpoint."""

    endpoint = "https://search.parallel.ai/mcp"
    protocol = "2025-03-26"

    def __init__(self, timeout: float):
        self.timeout = timeout
        self.session: Optional[str] = None
        self.request_id = 0
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": f"openagi/{version('openagi')}",
        }

    def request(
        self, method: str, params: Optional[Dict[str, Any]] = None, notification: bool = False
    ):
        payload = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = params
        if not notification:
            self.request_id += 1
            payload["id"] = self.request_id
        request = Request(self.endpoint, data=json.dumps(payload).encode(), headers=self.headers)
        try:
            with urlopen(request, timeout=self.timeout) as response:
                session = response.headers.get("Mcp-Session-Id")
                if session:
                    self.session = session
                    self.headers["Mcp-Session-Id"] = session
                if notification:
                    return None
                if response.headers.get_content_type() == "text/event-stream":
                    message = self._read_event(response, payload["id"])
                else:
                    message = json.load(response)
        except HTTPError as exc:
            raise OpenAGIException(f"Parallel Search MCP returned HTTP {exc.code}.") from exc
        except (URLError, OSError) as exc:
            raise OpenAGIException("Parallel Search MCP request failed or timed out.") from exc
        except (ValueError, UnicodeError) as exc:
            raise OpenAGIException("Parallel Search MCP returned an invalid response.") from exc
        if not isinstance(message, dict) or message.get("id") != payload["id"]:
            raise OpenAGIException("Parallel Search MCP returned an unexpected response ID.")
        if "error" in message:
            raise OpenAGIException(f"Parallel Search MCP error: {message['error']}")
        if "result" not in message:
            raise OpenAGIException("Parallel Search MCP response has no result.")
        return message["result"]

    @staticmethod
    def _read_event(response, request_id):
        data = []
        for raw_line in response:
            line = raw_line.decode("utf-8").rstrip("\r\n")
            if line.startswith("data:"):
                data.append(line[5:].lstrip(" "))
            elif not line and data:
                message = json.loads("\n".join(data))
                data = []
                if isinstance(message, dict) and message.get("id") == request_id:
                    return message
        raise ValueError("No matching MCP response event")

    def initialize(self):
        result = self.request(
            "initialize",
            {
                "protocolVersion": self.protocol,
                "capabilities": {},
                "clientInfo": {"name": "openagi", "version": version("openagi")},
            },
        )
        if not isinstance(result, dict) or result.get("protocolVersion") != self.protocol:
            raise OpenAGIException("Parallel Search MCP negotiated an unsupported protocol.")
        self.headers["MCP-Protocol-Version"] = self.protocol
        self.request("notifications/initialized", notification=True)

    def close(self):
        if self.session:
            try:
                request = Request(self.endpoint, headers=self.headers, method="DELETE")
                with urlopen(request, timeout=self.timeout):
                    pass
            except (URLError, OSError):
                # Session cleanup must not hide search results or the original error.
                pass


class ParallelSearch(BaseAction):
    """Search the web using free, keyless Parallel Search MCP.

    Returns source URLs and relevant excerpts as text for the agent to use.
    Select this action explicitly in an actions list to enable it.
    """

    query: str = Field(..., min_length=1, description="Question or objective for web search.")
    timeout: float = Field(
        default=30, gt=0, allow_inf_nan=False, description="Timeout in seconds per HTTP request."
    )
    session_id: str = Field(
        default_factory=lambda: uuid4().hex,
        max_length=100,
        description="Stable identifier for related searches.",
    )

    def execute(self) -> str:
        client = _SearchMCPClient(self.timeout)
        try:
            client.initialize()
            result = client.request(
                "tools/call",
                {
                    "name": "web_search",
                    "arguments": {
                        "objective": self.query,
                        "search_queries": [self.query],
                        "session_id": self.memory.session_id if self.memory else self.session_id,
                    },
                },
            )
            if not isinstance(result, dict):
                raise OpenAGIException("Parallel Search MCP returned an invalid tool result.")
            if result.get("isError"):
                raise OpenAGIException(
                    f"Parallel Search MCP tool failed: {result.get('content')}"
                )
            content = result.get("content", [])
            if not isinstance(content, list):
                raise OpenAGIException("Parallel Search MCP returned invalid tool content.")
            text = "\n".join(
                item["text"]
                for item in content
                if isinstance(item, dict)
                and item.get("type") == "text"
                and isinstance(item.get("text"), str)
            )
            if not text.strip():
                raise OpenAGIException("Parallel Search MCP returned no text content.")
            return text
        finally:
            client.close()
