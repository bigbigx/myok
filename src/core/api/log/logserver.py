# -*- coding: utf-8 -*-

import time
import re
import os.path
import asyncio
import logging
import argparse
import websockets
from collections import deque
from urllib.parse import urlparse, parse_qs
from ansi2html import Ansi2HTMLConverter


# from ...core.models import (
#     HostUserPwd
# )
NUM_LINES = 1000
HEARTBEAT_INTERVAL = 1200 # seconds

# init
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
allowed_prefixes = []
conv = Ansi2HTMLConverter(inline=True)

@asyncio.coroutine
def view_log(websocket, path):

    logging.info('Connected, remote={}, path={}'.format(websocket.remote_address, path))

    try:
        file_path=""
        try:
            parse_result = urlparse(path)
            print(parse_result)
            file_path = (parse_result.path).strip('/')
        except Exception:
            raise ValueError('Fail to parse URL')

        # file_path = os.path.abspath(parse_result.path)

        rereobj = re.compile('/')
        result = rereobj.sub('\\\\', file_path)
        # res = rereobj.findall(file_path)
        # result, number = rereobj.subn('\\', file_path)
        print(result)
        # result, number = rereobj.subn('\\', file_path)
        # file_path.replace('//', '\\')
        print('1111')
        print(result)
        allowed = False
        for prefix in allowed_prefixes:
            print(prefix)
            if result.startswith(prefix):
                allowed = True
                print('allowed')
                break
        if not allowed:
            print('1')
            raise ValueError('Forbidden')

        if not os.path.isfile(file_path):
            print('2')
            raise ValueError('Not found')

        query = parse_qs(parse_result.query)
        print(query)
        # file_path=""
        # if query and query['file']:
        #     file_path = query['file'][0]
        #     allowed = True
        tail = query and query['tail'] and query['tail'][0] == '1'

        with open(file_path) as f:
            content = ''.join(deque(f, NUM_LINES))
            content = conv.convert(content, full=False)
            yield from websocket.send(content)

            if tail:
                last_heartbeat = time.time()

                while True:
                    content = f.read()
                    if content:
                        content = conv.convert(content, full=False)
                        yield from websocket.send(content)
                        # last_heartbeat = time.time()
                    else:
                        yield from asyncio.sleep(1)
                    # print(last_heartbeat)
                    # # heartbeat
                    # print(time.time())
                    if time.time() - last_heartbeat > HEARTBEAT_INTERVAL:
                        print('ping timeout')
                        try:
                            yield from websocket.send('ping')
                            pong = yield from asyncio.wait_for(websocket.recv(), 60)
                            if pong != 'pong':
                                raise Exception()
                        except Exception:
                            raise Exception('Ping error')
                        else:
                            last_heartbeat = time.time()

            else:
                yield from websocket.close()
                log_close(websocket, path)

    except ValueError as e:
    # except Exception as e:
        print(e)
        try:
            # yield from websocket.send('<font color="red"><strong>{}</strong></font>'.format(e))
            yield from websocket.send('{}'.format(e))
            yield from websocket.close()
        except Exception:
            pass

        log_close(websocket, path, e)

    except Exception as e:
        log_close(websocket, path, e)

    else:
        log_close(websocket, path)

def log_close(websocket, path, exception=None):
    message = 'Closed, remote={}, path={}'.format(websocket.remote_address, path)
    if exception is not None:
        message += ', exception={}'.format(exception)
    logging.info(message)

# def getUserPwd(ip, user):
#     obj = HostUserPwd.objects.filter(public_IP=ip, user_name=user).first()
#     print(obj)
#     pwd = obj.password
#     return pwd


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=3320)
    parser.add_argument('--prefix', required=True, action='append', help='Allowed directories')
    args = parser.parse_args()

    allowed_prefixes.extend(args.prefix)
    start_server = websockets.serve(view_log, args.host, args.port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()