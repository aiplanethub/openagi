"""Exercise the real action loader and execution, replacing only HTTP I/O."""

import io
import json
from email.message import Message
from urllib.error import HTTPError, URLError

import pytest
from pydantic import ValidationError

from openagi.actions.tools import parallel_search
from openagi.actions.tools.parallel_search import ParallelSearch
from openagi.actions.utils import run_action
from openagi.exception import OpenAGIException
from openagi.utils.extraction import get_act_classes_from_json


class Response(io.BytesIO):
    def __init__(self, value=None, content_type="application/json", session=None, raw=None):
        super().__init__(raw if raw is not None else json.dumps(value).encode())
        self.headers = Message()
        self.headers["Content-Type"] = content_type
        if session:
            self.headers["Mcp-Session-Id"] = session


@pytest.fixture
def transport(monkeypatch):
    requests = []
    state = {
        "result": {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(
                        {
                            "results": [
                                {
                                    "url": "https://www.python.org/",
                                    "title": "Python",
                                    "excerpts": ["Python is a programming language."],
                                }
                            ]
                        }
                    ),
                }
            ]
        },
        "sse": False,
    }

    def send(request, timeout):
        requests.append((request, timeout))
        if request.get_method() == "DELETE":
            return Response()
        body = json.loads(request.data)
        if body["method"] == "initialize":
            return Response(
                {
                    "jsonrpc": "2.0",
                    "id": body["id"],
                    "result": {
                        "protocolVersion": state.get("protocol", "2025-03-26"),
                        "capabilities": {"tools": {}},
                    },
                },
                session="transport-session",
            )
        if body["method"] == "notifications/initialized":
            return Response(raw=b"")
        if state.get("exception"):
            raise state["exception"]
        message = {"jsonrpc": "2.0", "id": state.get("id", body["id"])}
        message.update(
            {"error": state["error"]} if "error" in state else {"result": state["result"]}
        )
        if state["sse"]:
            raw = (
                ": keepalive\r\n\r\n"
                'data: {"jsonrpc":"2.0","method":"notifications/progress"}\r\n\r\n'
                f"event: message\r\ndata: {json.dumps(message)}\r\n\r\n"
            ).encode()
            return Response(content_type="text/event-stream", raw=raw)
        return Response(message)

    monkeypatch.setattr(parallel_search, "urlopen", send)
    return requests, state


@pytest.mark.parametrize("sse", [False, True])
def test_loader_effective_configuration_and_execution(transport, monkeypatch, sse):
    requests, state = transport
    state["sse"] = sse
    monkeypatch.setenv("PARALLEL_API_KEY", "unused-test-value")
    action_doc = ParallelSearch.cls_doc()
    cls, params = get_act_classes_from_json(
        [
            {
                "cls": action_doc["cls"],
                "params": {
                    "query": "What is Python?",
                    "timeout": 7,
                    "session_id": "conversation",
                },
            }
        ]
    )[0]
    assert cls is ParallelSearch
    result = run_action(cls, memory=None, llm=None, **params)
    assert json.loads(result)["results"][0]["excerpts"] == ["Python is a programming language."]
    assert "https://www.python.org/" in result
    bodies = [json.loads(r.data) for r, _ in requests if r.data]
    assert [b["method"] for b in bodies] == [
        "initialize",
        "notifications/initialized",
        "tools/call",
    ]
    assert bodies[-1]["params"] == {
        "name": "web_search",
        "arguments": {
            "objective": "What is Python?",
            "search_queries": ["What is Python?"],
            "session_id": "conversation",
        },
    }
    for index, (request, timeout) in enumerate(requests):
        assert request.full_url == "https://search.parallel.ai/mcp"
        assert timeout == 7
        headers = dict((k.lower(), v) for k, v in request.header_items())
        assert headers["user-agent"] == "openagi/0.3.0"
        assert "authorization" not in headers and "x-api-key" not in headers
        if index:
            assert headers["mcp-session-id"] == "transport-session"
            assert headers["mcp-protocol-version"] == "2025-03-26"
    assert requests[-1][0].get_method() == "DELETE"


@pytest.mark.parametrize(
    "state,error",
    [
        ({"error": {"code": -32601, "message": "Unavailable"}}, "MCP error"),
        ({"result": {"isError": True, "content": []}}, "tool failed"),
        ({"result": {"content": []}}, "no text content"),
        ({"result": {"content": "invalid"}}, "invalid tool content"),
        ({"result": None}, "invalid tool result"),
        ({"id": 99}, "unexpected response ID"),
        ({"protocol": "unknown"}, "unsupported protocol"),
        ({"exception": TimeoutError()}, "timed out"),
        ({"exception": URLError("offline")}, "request failed"),
        ({"exception": HTTPError("url", 429, "Rate limited", None, None)}, "HTTP 429"),
        ({"exception": ValueError("bad JSON")}, "invalid response"),
    ],
)
def test_errors_are_visible_and_session_is_closed(transport, state, error):
    requests, active_state = transport
    active_state.update(state)
    with pytest.raises(OpenAGIException, match=error):
        run_action(ParallelSearch, memory=None, llm=None, query="Python")
    assert requests[-1][0].get_method() == "DELETE"


@pytest.mark.parametrize("params", [{"query": ""}, {"query": "Python", "timeout": 0}])
def test_invalid_input_makes_no_requests(transport, params):
    with pytest.raises(ValidationError):
        ParallelSearch(**params)
    assert not transport[0]


def test_existing_provider_configuration_is_untouched():
    from openagi.actions.base import ConfigurableAction

    previous = dict(ConfigurableAction.config)
    ParallelSearch(query="Python")
    assert ConfigurableAction.config == previous
    assert not issubclass(ParallelSearch, ConfigurableAction)


@pytest.mark.parametrize("sse", [False, True])
def test_admin_selection_to_final_answer(transport, sse):
    from parallel_search_fixtures import run_agent_search

    requests, state = transport
    state["sse"] = sse
    answer, llm, memory = run_agent_search("What is Python?")
    assert answer == {
        "final_output": "Python is a programming language. Source: https://www.python.org/"
    }
    assert llm.calls == 2
    search_request = next(
        json.loads(r.data)
        for r, _ in requests
        if r.data and json.loads(r.data)["method"] == "tools/call"
    )
    assert search_request["params"]["arguments"]["session_id"] == memory.session_id
