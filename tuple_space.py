import threading

class TupleSpace:
    def _init_(self):
        self.data = {}
        self.lock = threading.Lock

    def read(self, key):
        with self.lock:
            if key in self.data:
                return True, self.data[key]
            else: return False, None

    def get(self, key):
        with self.lock:
            if key in self.data:
                value = self.data[key]
                del self.data[key]
                return True, value
            else: return False, None

    def put(self, key, value):
        with self.lock:
            if key in self.data:
                return False
            else: 
                self[key] = value
                return True