#5_2
import asyncio
from collections import defaultdict

data_dict_g = defaultdict(list)
ERROR_MSG = 'error\nwrong command\n\n'


class ClientServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self._process_data(data.decode())
        self.transport.write(resp.encode())

    def _process_data(self, data) -> str:
        try:
            method, values = data.split(' ', 1)
            if method == 'get':
                return self._proc_get(values)
            elif method == 'put':
                return self._proc_put(values)
            else:
                return ERROR_MSG
        except:
            return ERROR_MSG

    def _proc_get(self, values):
        key = values.strip('\n ')
        text = 'ok\n'
        if len(key.split()) > 1 or len(key) == 0:
            return ERROR_MSG
        answ_list = self._get_list_answers(key)
        for el in answ_list:
            text += el
        return text + '\n'

    @staticmethod
    def _get_list_answers(key) -> list:
        answ_list = []
        if key == '*':
            for key, values in data_dict_g.items():
                for val in values:
                    answ_list.append(f'{key} {val[0]} {val[1]}\n')
        else:
            if data_dict_g.get(key):
                answ_list += [f'{key} {val[0]} {val[1]}\n' for val in data_dict_g.get(key)]
        return answ_list

    def _proc_put(self, values):
        try:
            metric, val, timestamp = values.strip('\n ').split()
            if not self._check_some_timestamp(metric, float(val), float(timestamp)):
                data_dict_g[metric].append([float(val), int(timestamp)])
            return 'ok\n\n'
        except ValueError:
            return ERROR_MSG

    @staticmethod
    def _check_some_timestamp(metric, val, timestamp):
        already_val = data_dict_g.get(metric)
        if already_val:
            for elem in already_val:
                if elem[1] == timestamp:
                    elem[0] = val
                    return True
        return False


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

# run_server('127.0.0.1', 8888)
