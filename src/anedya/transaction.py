"""
Transaction provides a way to communicate data between mqtt callback
and utility functions
"""

import queue
import random
import string
from .errors import AnedyaInvalidTransaction


class Transaction:
    def __init__(self, id: str):
        self._id = id
        self._is_complete = False
        self._data = None
        self._queue = queue.Queue(maxsize=1)

    def wait_to_complete(self, timeout: int | None = None):
        return self._queue.get(timeout=timeout)

    def is_complete(self):
        return self._is_complete

    def get_id(self):
        return self._id

    def set_data(self, data):
        self._data = data
        return

    def get_data(self):
        return self._data

    def mark_complete(self, data=None):
        self._is_complete = True
        self._data = data
        self._queue.put(True)
        return


class Transactions:
    def __init__(self):
        self._transactions = {}

    def create_transaction(self):
        # Create a unique ID for the transaction
        id = "req_" + ''.join(random.choices(
            string.ascii_letters + string.digits, k=16))
        # Create a new transaction object in dictionary
        self._transactions[id] = Transaction(id)
        return self._transactions[id]

    def mark_complete(self, id: str, data=None):
        if id in self._transactions:
            self._transactions[id].mark_complete(data)
        else:
            raise AnedyaInvalidTransaction("Unknown or Uninitiated transaction")
        return

    def clear_transaction(self, transaction):
        del self._transactions[transaction._id]
        return
