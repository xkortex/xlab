#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import time
import shlex
import asyncio

from spaghetr.protos import aio_subproc_pb2, aio_subproc_pb2_grpc


def arg_parser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument(
        'cmd', nargs='?', default='ls', type=str,
        help="Command to run"
    )

    return parser


async def main(n=0):
    proc = await asyncio.subprocess.create_subprocess_exec(
        "./hello.py", stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )
    proc.stdin.write('alice{}\n'.format(n).encode())
    print(await proc.stdout.read(1024))
    proc.stdin.write('bob{}\n'.format(n).encode())
    print(await proc.stdout.read(1024))
    proc.stdin.write('quit\n'.encode())
    await proc.wait()


async def got_stdin_data(q: asyncio.Queue):
    await q.put(sys.stdin.readline())


async def get_input_data(q: asyncio.Queue):
    while True:
        await q.put(input('name?: '))
        await asyncio.sleep(0)


async def greet(q: asyncio.Queue, reader: asyncio.Future):
    """
    loop: asyncio.AbstractEventLoop
    :param q:
    :return:
    """

    proc = await asyncio.subprocess.create_subprocess_shell(
        './hello.py --pipe', stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )
    while True:
        name = await q.get()
        print('<sending {}>'.format(name), flush=True)
        proc.stdin.write('{}\n'.format(name).encode())
        res = await proc.stdout.read(1024)
        if not res:
            print('<break>')
            break
        print(res.decode(), flush=True)
        # await asyncio.sleep(0.1)
    await proc.wait()
    print('<done waiting>')
    # tasks = asyncio.tasks
    # loop.close()
    # print(tasks)
    reader.cancel()
    print('<reader cancelled>')


class NumberServicer(aio_subproc_pb2_grpc.AioSubprocessServicer):
    def __init__(self):
        pass


    async def attach(self):
        self.proc = await asyncio.subprocess.create_subprocess_shell(
            './hello.py --pipe', stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE)


async def get_nums(q: asyncio.Queue):
    proc = await asyncio.subprocess.create_subprocess_shell(
        './hello.py --pipe', stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )

async def test_queue(q: asyncio.Queue):
    while True:
        name = await q.get()
        print('hi {}'.format(name), flush=True)


if __name__ == '__main__':
    args = arg_parser().parse_args()

    q1 = asyncio.Queue()
    loop = asyncio.get_event_loop()
    # loop.add_reader(sys.std)
    readert = asyncio.ensure_future(get_input_data(q1))
    # readert = loop.create_task(get_input_data(q1))
    loop.run_until_complete(greet(q1, readert))

    ## this allows us to shut down more cleanly on 'quit'
    loop.run_until_complete(asyncio.wait([readert]))
    # loop.run_forever()
    loop.close()
