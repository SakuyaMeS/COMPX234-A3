import threading

class TupleSpcace:
    def _init_(self):
        self.data = {}
        self.lock = threading.Lock

        def read(self, key):
            with self.lock:
                if key in self.data:
                    return True, self.data[key]
                else: return False, None

        def get(self, key):
            pass

        def put(self, key, value):
            pass