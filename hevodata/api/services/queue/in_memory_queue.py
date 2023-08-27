from queue import SimpleQueue

from api.services.queue.base import BaseQueue


class InMemoryQueue(BaseQueue):
    queue = SimpleQueue()

    def push(self, item):
        self.queue.put(item=item)

    def get(self, item):
        if self.queue.empty():
            return None
        return self.queue.get()
