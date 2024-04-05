import json


def convert_json_to_python(input_string):
    class Agent:
        def __init__(
            self,
            agentName,
            role,
            goal,
            backstory,
            capability,
            task,
            output_consumer_agent,
            tools_list,
        ):
            self.agentName = agentName
            self.role = role
            self.goal = goal
            self.backstory = backstory
            self.capability = capability
            self.task = task
            self.output_consumer_agent = output_consumer_agent
            self.tools_list = tools_list

    # Parse the JSON input
    input_data = json.loads(input_string)
    # Generate Python code
    python_code = "agent_list = [\n"
    for agent_data in input_data:
        tools_list = agent_data.get("tools_list", [])  # Handle missing 'tools_list' key
        tools_code = [f"{tool}" for tool in tools_list] if tools_list else []
        agent_code = (
            f"    Agent(\n"
            f"        agentName = \"{agent_data['agentName']}\",\n"
            f"        role = \"{agent_data['role']}\",\n"
            f"        goal = \"{agent_data['goal']}\",\n"
            f"        backstory = \"{agent_data['backstory']}\",\n"
            f"        capability = \"{agent_data['capability']}\",\n"
            f"        task = \"{agent_data['task']}\",\n"
            f"        output_consumer_agent = [\"{agent_data['output_consumer_agent']}\"],\n"
            f"        tools_list = [{', '.join(tools_code)}]\n"
            f"    ),\n"
        )
        python_code += agent_code

    python_code += "]\n"

    return python_code
