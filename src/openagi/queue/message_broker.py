import logging
import threading

from openagi.queue.pq import MultiThreadPriorityQueue, consumer, producer
from openagi.queue.timer_pool import TimerList
from openagi.utils.yamlParse import read_yaml_config

num_queues = read_yaml_config("MAX_NUMBER_OF_AGENTS")


class NameIndexMapper:
    def __init__(self):
        self.name_to_index = {}
        self.index_to_name = {}
        self.PQ_LIST = [MultiThreadPriorityQueue() for i in range(num_queues)]
        self.COND_LIST = [threading.Condition() for i in range(num_queues)]
        self.lock = threading.Lock()
        self.timerPool = TimerList()
        logging.debug(f"created message broker infra with agents no {num_queues}")

    def add_mapping(self, name):
        with self.lock:
            if name not in self.name_to_index:
                index = len(self.name_to_index)
                self.name_to_index[name] = index
                self.index_to_name[index] = name

    def get_index_by_name(self, name):
        with self.lock:
            return self.name_to_index.get(name)

    def get_name_by_index(self, index):
        with self.lock:
            return self.index_to_name.get(index)

    def get_PQ_by_name(self, agentName):
        index = self.get_index_by_name(agentName)
        logging.debug(f"index of {agentName} is {index}")
        return self.PQ_LIST[index]

    def get_COND_by_name(self, agentName):
        index = self.get_index_by_name(agentName)
        logging.debug(f"index of {agentName} is {index}")
        return self.COND_LIST[index]

    def timerStartMapper(self, agentName, timerName, callback, timervalue):
        newTimer = self.timerPool.add_timer(agentName, timerName, callback, timervalue)
        return newTimer

    def timerStopMapper(self, agentName, timerName):
        self.timerPool.remove_timerWithNames(agentName, timerName)


# Example Usage:
if __name__ == "__main__":
    mapper = NameIndexMapper()

    # Adding mappings
    mapper.add_mapping("Alice")
    mapper.add_mapping("Bob")
    mapper.add_mapping("Charlie")

    # Using the mapper
    index_for_alice = mapper.get_index_by_name("Alice")
    name_for_index_1 = mapper.get_name_by_index(1)

    logging.info(f"Index for Alice: {index_for_alice}")
    logging.info(f"Name for index 1: {name_for_index_1}")

    PQ1 = mapper.get_PQ_by_name("Alice")
    PQ2 = mapper.get_PQ_by_name("Bob")
    PQ3 = mapper.get_PQ_by_name("Charlie")
    # mapper.sleepAgent("Alice",100)
    # mapper.sleepAgent("Bob",100)
    # mapper.sleepAgent("Charlie",100)
    # mapper.wakeupAgent("Alice")
    # mapper.wakeupAgent("Bob")
    # mapper.wakeupAgent("Charlie")

    producer_thread = threading.Thread(target=producer, args=(PQ1,))
    producer_thread = threading.Thread(target=producer, args=(PQ2,))
    producer_thread = threading.Thread(target=producer, args=(PQ3,))
    consumer_thread = threading.Thread(target=consumer, args=(PQ1,))
    consumer_thread = threading.Thread(target=consumer, args=(PQ2,))
    consumer_thread = threading.Thread(target=consumer, args=(PQ3,))

    # Start the threads
    producer_thread.start()
    consumer_thread.start()

    # Wait for threads to finish
    producer_thread.join()
    consumer_thread.join()

    # List all elements in the queue after threads finish
    all_elements = PQ1.list_all_elements()
    logging.info("\nAll Elements in Priority Queue1:")
    for element in all_elements:
        logging.info(element.__dict__)

    all_elements = PQ3.list_all_elements()
    logging.info("\nAll Elements in Priority Queue3:")
    for element in all_elements:
        logging.info(element.__dict__)

    all_elements = PQ2.list_all_elements()
    logging.info("\nAll Elements in Priority Queue2:")
    for element in all_elements:
        logging.info(element.__dict__)
