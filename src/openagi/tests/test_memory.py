import pytest
from openagi.memory.STMemory import STMemory
from openagi.memory.LTMemory import LTMemory
from openagi.memory.storage import clear_collection

@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    """Setup and teardown for the tests."""
    # Setup: Clear the collection before tests
    clear_collection()

    yield

    # Teardown: Clear the collection after tests
    clear_collection()

def test_stmemory_add_and_search():
    st_memory = STMemory("test_agent")

    task = "Test Task"
    tools = ["Tool1", "Tool2"]
    consumer = "Test Consumer"

    # Save to STMemory
    st_memory.save_admin_exec(task, tools, consumer)

    # Search for the task
    query = "Test Task"
    results = st_memory.search(query)

    assert results, "No results found"
    assert results[0]['metadata']['task'] == task
    assert results[0]['metadata']['tools'] == tools
    assert results[0]['metadata']['consumer'] == consumer

def test_stmemory_update_tool_exec():
    st_memory = STMemory("test_agent")

    task = "Update Task"
    tools = ["Tool1"]
    consumer = "Consumer1"

    # Save to STMemory
    st_memory.save_admin_exec(task, tools, consumer)

    # Update tool execution
    tool_name = "Tool1"
    tool_output = "Output1"
    st_memory.save_tool_exec(tool_name, tool_output)

    # Search for the task
    query = "Update Task"
    results = st_memory.search(query)

    assert results, "No results found"
    assert 'tool_output' in results[0]['metadata']
    assert results[0]['metadata']['tool_output'][0]['tool_name'] == tool_name
    assert results[0]['metadata']['tool_output'][0]['tool_output'] == tool_output

def test_stmemory_display_memory():
    st_memory = STMemory("test_agent")

    task = "Display Task"
    tools = ["Tool1"]
    consumer = "Consumer1"

    # Save to STMemory
    st_memory.save_admin_exec(task, tools, consumer)

    # Display memory
    memory = st_memory.display_memory()

    assert memory, "Memory is empty"
    assert memory['metadata']['task'] == task
    assert memory['metadata']['tools'] == tools
    assert memory['metadata']['consumer'] == consumer

def test_ltmemory_add_and_get():
    lt_memory = LTMemory("test_agent")

    task = "Long Term Test Task"
    information = {"detail": "This is a detailed description"}

    # Memorize in LTMemory
    lt_memory.memorize(task, information)

    # Retrieve from LTMemory
    query = "Long Term Test Task"
    results = lt_memory.get(query)

    assert results, "No results found"
    assert results[0]['metadata']['task'] == task
    assert results[0]['metadata']['information'] == information

def test_ltmemory_display_memory():
    lt_memory = LTMemory("test_agent")

    task = "Display Long Term Task"
    information = {"detail": "This is another detailed description"}

    # Memorize in LTMemory
    lt_memory.memorize(task, information)

    # Display memory
    memory = lt_memory.display_memory()

    assert memory, "Memory is empty"
    assert memory['metadata']['task'] == task
    assert memory['metadata']['information'] == information

if __name__ == "__main__":
    pytest.main()