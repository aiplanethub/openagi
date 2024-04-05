import logging
import queue
import random
import threading
import time
from enum import Enum


class MessageType(Enum):
    TIMER_MSG = 1
    PROF_AGENT_TRIGGER = 2
    STOP_MSG = 3
    SHUTDOWN_MSG = 4
    AGENT_MSG = 5
    FEEDBACK_MSG = 6
    STATUS_RSP = 7
    LLM_CHANGE_MSG = 8


class Message:
    def __init__(self, priority, perception_type, message_type, srcAgent, dstAgent, body):
        self.priority = priority
        self.perception_type = perception_type
        self.message_type = message_type
        self.srcAgent = srcAgent
        self.dstAgent = dstAgent
        self.body = body
        logging.debug(
            f"message contents:{priority}:{perception_type}::{message_type} ::{srcAgent} ->{dstAgent} :{body}"
        )

    def __lt__(self, other):
        return self.priority < other.priority


class MultiThreadPriorityQueue:
    def __init__(self):
        self.priority_queue = queue.PriorityQueue()
        self.lock = threading.Lock()

    def insert(self, message):
        with self.lock:
            self.priority_queue.put(message)

    def retrieve_first_message(self):
        with self.lock:
            if not self.priority_queue.empty():
                return self.priority_queue.get()
            else:
                return None

    def list_all_elements(self):
        with self.lock:
            return list(self.priority_queue.queue)


def producer(queue):
    for _ in range(5):
        priority = random.randint(1, 10)
        perception_type = 0
        message_type = random.choice(list(MessageType))
        body = f"Body_{random.randint(100, 999)}"
        message = Message(priority, perception_type, message_type, "", "", body)
        queue.insert(message)
        time.sleep(random.uniform(0.1, 0.5))


def consumer(queue):
    for _ in range(5):
        message = queue.retrieve_first_message()
        if message:
            logging.debug(f"Consumer retrieved message: {message.__dict__}")
        else:
            logging.info("Consumer found no messages.")
        time.sleep(10)


if __name__ == "__main__":
    mt_priority_queue = MultiThreadPriorityQueue()

    # Create producer and consumer threads
    producer_thread = threading.Thread(target=producer, args=(mt_priority_queue,))
    consumer_thread = threading.Thread(target=consumer, args=(mt_priority_queue,))

    # Start the threads
    producer_thread.start()
    consumer_thread.start()

    # Wait for threads to finish
    producer_thread.join()
    consumer_thread.join()

    # List all elements in the queue after threads finish
    all_elements = mt_priority_queue.list_all_elements()
    logging.info("\nAll Elements in Priority Queue:")
    for element in all_elements:
        logging.info(element.__dict__)
