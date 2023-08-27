from api.services.queue.in_memory_queue import InMemoryQueue


class BaseQueue:
    def push(self, item):
        pass

    def get(self, item):
        pass


class QueueFactory:
    queue = None

    # singleton
    @staticmethod
    def get_queue():
        if QueueFactory.queue is None:
            # this is where the right Queue needs to be initialized
            QueueFactory.queue = InMemoryQueue()
        return QueueFactory.queue
