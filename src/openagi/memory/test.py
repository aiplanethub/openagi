import unittest
from openagi.memory.memory import Memory

class TestMemory(unittest.TestCase):
    def setUp(self):
        self.memory = Memory()  # Ensure Memory is properly instantiated

    def test_display_memory(self):
        memory_state = self.memory.display_memory()
        self.assertIsInstance(memory_state, dict)  # Adjusted to match expected output type

    def test_memorize(self):
        task = "Learn Python"
        information = "Python is a popular programming language."
        self.memory.memorize(task, information)
        # Add assertions if needed to check the results of the memorize function

    def test_save(self):
        query = "Python programming"
        planned_tasks = ["Search for information", "Verify the answer"]
        final_res = "Python is a popular programming language."
        self.memory.save_task(query, planned_tasks, final_res)
        # Add assertions if needed to check the results of the save function

    def test_search(self):
        query = "Python programming"
        results = self.memory.search(query)
        self.assertIsInstance(results, dict)  # Adjusted to match expected output type
        self.assertIn('ids', results)
        self.assertIn('distances', results)
        self.assertIn('metadatas', results)
        self.assertIn('documents', results)

if __name__ == '__main__':
    unittest.main()