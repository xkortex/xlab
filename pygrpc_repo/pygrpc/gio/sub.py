#!/usr/bin/env python
# -*- coding: utf-8 -*-


# py37 only
# import asyncio
# async def run(cmd):
#     proc = await asyncio.create_subprocess_shell(
#         cmd,
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE)
#
#     stdout, stderr = await proc.communicate()
#
#     print(f'[{cmd!r} exited with {proc.returncode}]')
#     if stdout:
#         print(f'[stdout]\n{stdout.decode()}')
#     if stderr:
#         print(f'[stderr]\n{stderr.decode()}')
#
# asyncio.run(run('ls /tmp'))

import sys
import time
import shlex
from subprocess import PIPE, Popen
from threading  import Thread

from queue import Queue, Empty


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


def arg_parser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument(
        'cmd', nargs='?', default='ls', type=str,
        help="Command to run"
    )

    return parser

import asyncio
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
        await asyncio.sleep(0.1)


async def greet(q: asyncio.Queue, reader: asyncio.Future):
    """
    loop: asyncio.AbstractEventLoop
    :param q:
    :return:
    """
    # proc = await asyncio.subprocess.create_subprocess_exec(
    #     './hello.py', stdin=asyncio.subprocess.PIPE,
    #     stdout=asyncio.subprocess.PIPE
    # )
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


async def test_queue(q: asyncio.Queue):
    while True:
        name = await q.get()
        print('hi {}'.format(name), flush=True)


# def run_greeter():


def queue_nonblock():
    p = Popen(shlex.split(args.cmd), stdout=PIPE, bufsize=1)
    q = Queue()
    t = Thread(target=enqueue_output, args=(p.stdout, q))
    t.daemon = True  # thread dies with the program
    t.start()

    # ... do other things here
    while True:
        # read line without blocking
        try:
            # line = q.get_nowait()
            line = q.get(timeout=.1)
            print('\n[{}]'.format(line))
            # if line == EF
        except Empty:
            print('.', end='', flush=True)
            time.sleep(0.25)
        else:  # got line
            # ... do something with line
            print('_', flush=True)


if __name__ == '__main__':
    args = arg_parser().parse_args()
    # queue_nonblock()
    # asyncio.run(main())
    # futures = [main(n) for n in range(3)]
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
