import random
import tempfile
import os


class File:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        if not os.path.exists(path_to_file):
            new_file = open(path_to_file, 'w')
            new_file.close()

    def __str__(self):
        return self.path_to_file

    def read(self):
        with open(self.path_to_file, 'r') as f:
            return f.read()

    def write(self, text):
        with open(self.path_to_file, 'w') as f:
            return f.write(text)

    def __add__(self, other):
        full_path = os.path.join(tempfile.gettempdir(), f'new_file_{random.randint(0, 100)}')
        f3 = File(full_path)
        f3.write(self.read() + other.read())
        return f3

    def __iter__(self):
        self.f = open(self.path_to_file, 'r')
        return self

    def __next__(self):
        f = self.f.readline()
        if f:
            return f
        else:
            self.f.close()
            raise StopIteration
