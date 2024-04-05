import logging
import threading
import time

condition = threading.Condition()


def waitonCondition(condition, duration):
    condition.acquire()
    condition.wait(timeout=duration)
    condition.release()


def execute_function():
    logging.debug("Executing the function...")


def wakeupTimerThread():
    condition.acquire()
    condition.notify()
    condition.release()


class TimerNode:
    def __init__(self, agentName, timerName, callback, expiry_time):
        self.callback = callback
        self.expiry_time = expiry_time
        self.agentName = agentName
        self.timerName = timerName
        self.next = None
        self.prev = None


class TimerList:
    def __init__(self):
        self.head = None
        self.lock = threading.Lock()

    def add_timer(self, agentName, timerName, callback, interval):
        expiry_time = time.time() + interval
        logging.debug(f"current time: {time.time()} : internal {interval}")
        new_timer = TimerNode(agentName, timerName, callback, expiry_time)

        with self.lock:
            if not self.head or self.head.expiry_time > expiry_time:
                logging.debug("first timer inserted....")
                new_timer.next = self.head
                if self.head:
                    self.head.prev = new_timer
                self.head = new_timer
            # wakeupTimerThread()

            else:
                current = self.head
                while current.next and current.next.expiry_time <= expiry_time:
                    current = current.next

                new_timer.next = current.next
                if current.next:
                    current.next.prev = new_timer
                current.next = new_timer
                new_timer.prev = current
        wakeupTimerThread()
        return new_timer

    def remove_timer(self, timer_node):
        with self.lock:
            if timer_node.prev:
                timer_node.prev.next = timer_node.next
            else:
                self.head = timer_node.next

            if timer_node.next:
                timer_node.next.prev = timer_node.prev
            wakeupTimerThread()

    def remove_timerWithLock(self, timer_node):
        if timer_node.prev:
            timer_node.prev.next = timer_node.next
        else:
            self.head = timer_node.next

        if timer_node.next:
            timer_node.next.prev = timer_node.prev
        wakeupTimerThread()

    def remove_timerWithNames(self, agentName, timerName):
        logging.debug(f"remove timer is called for {agentName} {timerName}")
        with self.lock:
            if self.head:
                current = self.head
                while current:
                    if current.agentName == agentName and current.timerName == timerName:
                        logging.debug(
                            f"timer found for agent {agentName} timer name {timerName}  for removal"
                        )
                        self.remove_timerWithLock(current)
                        return True
                    else:
                        current = current.next

            logging.debug(f"timer of agent {agentName} timer name {timerName} not found ")
            return False

    def list_active_timers(self):
        with self.lock:
            current = self.head
            while current:
                print(
                    f"{current.agentName}::Timer :{current.timerName}expires at: {current.expiry_time} "
                )
                current = current.next

    def run(self):
        logging.debug("timer thread started..................")
        while True:
            with self.lock:
                if self.head:
                    current_time = time.time()
                    time_to_wait = max(0, self.head.expiry_time - current_time)
                else:
                    time_to_wait = 1000  # float('inf')
            logging.debug(f"time to sleep: {time_to_wait}")
            waitonCondition(condition, time_to_wait)
            # time.sleep(time_to_wait)
            # print("sleep is over....")
            with self.lock:
                if self.head and time.time() >= self.head.expiry_time:
                    print("timer call to be called as timer expired...")
                    callback = self.head.callback
                    agentName = self.head.agentName
                    timerName = self.head.timerName
                    timerValue = self.head.expiry_time
                    # print("timer to be revomed....")
                    self.remove_timerWithLock(self.head)
                    # print("timer is removed......")

                    if callback:
                        logging.debug(
                            f"Callback executed at {agentName}:{timerName}:{timerValue}"
                        )
                        callback(agentName, timerName, timerValue)


def example_callback(agentName, timerName, timerValue):
    logging.debug(f"Callback executed at {agentName}:{timerName}:{timerValue}")


def timerStart(agentName, timerName, callback, timervalue):
    newTimer = timer_list.add_timer(agentName, timerName, callback, timervalue)


if __name__ == "__main__":
    timer_list = TimerList()

    # Create two threads to create multiple timers

    # thread1 = threading.Thread(target=lambda: timer_list.add_timer("thread1", example_callback, 13))
    # thread2 = threading.Thread(target=lambda: timer_list.add_timer("thread2", example_callback, 15))

    # Create the worker thread and pass the condition and duration to it
    # timer_thread = threading.Thread(target=timer_list.run, args=(condition, wait_duration))
    # Start the worker thread
    # Start the timer thread
    timer_thread = threading.Thread(target=timer_list.run)
    timer_thread.start()

    time.sleep(1)
    for i in range(50):
        timerStart("agent1", "tmr" + str(i), example_callback, 10 + i)
        timerStart("agent2", "tmr" + str(i), example_callback, 11 + i)
    print("Active Timers:")
    timer_list.list_active_timers()
    # condition.notify()
    # Start the timer-setting threads
    # thread1.start()
    # thread2.start()
    # Keep the main thread alive
    try:
        time.sleep(100)

    except KeyboardInterrupt:
        print("exception.....")
        # If the user interrupts the program, stop all threads
        timer_thread.join()
        # thread1.join()
        # thread2.join()
