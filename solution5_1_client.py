#5_1
import time
import socket
from collections import defaultdict


class ClientError(socket.error):
    pass


class Client:

    def __init__(self, host, port, timeout=None):
        self.sock = socket.create_connection((host, port), timeout)

    def put(self, name: str, value: float, timestamp=None):
        try:
            if not timestamp:
                timestamp = int(time.time())
            self.sock.sendall(f'put {name} {value} {timestamp}\n'.encode())
            self._check_answer(self.sock.recv(1024))
        except:
            raise ClientError

    def get(self, name: str) -> dict:
        try:
            self.sock.sendall(f'get {name}\n'.encode())
            text = self._check_answer(self.sock.recv(1024))
            return self._parse_row(text)
        except:
            raise ClientError

    @staticmethod
    def _check_answer(row):
        answ_list = row.decode().split('\n')
        if answ_list[0] != 'ok':
            raise ClientError
        return answ_list[1:]

    @staticmethod
    def _parse_row(answ_list) -> dict:
        answer = defaultdict(list)
        for i in range(len(answ_list) - 2):
            element = answ_list[i].split()
            answer[element[0]].append((int(element[2]), float(element[1])))
        for value in answer.values():
            value.sort(key=lambda tup: tup[0])
        return dict(answer)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()
