# main.py
import logging

from AgentGenHdr_tail import hdr_azure, hdr_openai, tail_azure, tail_openai
from converter import convert_json_to_python
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from PlannerLLM import generateDAG

app = FastAPI()

# Mount the static folder to serve static files
app.mount("/static", StaticFiles(directory="UI/static"), name="static")


def generatePYProgram(objective: str, llm_choice: str) -> HTMLResponse:
    # tool_list = [{"MyCalculator" : "Calculated the values of mathematical expressions with the help of python."}]
    tool_list = []
    logging.debug(f"objective: {objective}")
    reply = generateDAG(objective, tool_list, llm_choice)
    logging.debug(f"planner output: {reply}")
    start_input_number = reply.index("[\n    {")
    end_output_number = reply.rfind("]")
    input = reply[start_input_number : end_output_number + 1]
    output_code = convert_json_to_python(input)
    logging.debug(f"code fragment generated:: {output_code}")
    if llm_choice == "openai":
        code1 = hdr_openai + output_code + tail_openai
    else:
        code1 = hdr_azure + output_code + tail_azure

    logging.debug(f"final  generated code :: {code1}")
    return HTMLResponse(content=code1, status_code=200)


@app.get("/", response_class=HTMLResponse)
async def get_form():
    return HTMLResponse(content=open("UI/static/index.html", "r").read(), status_code=200)


@app.post("/generate")
async def generate_code(objective: str = Form(...), llm_choice: str = Form(...)):
    code = generatePYProgram(objective, llm_choice)
    return code


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
