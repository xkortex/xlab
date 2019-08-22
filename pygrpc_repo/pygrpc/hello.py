#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import asyncio

"""Mucking with piped processes. 
https://stackoverflow.com/questions/29081929/prompt-for-user-input-using-python-asyncio-create-server-instance
"""

def interact():
    """Basic dumb input mode"""
    while True:
        i = input()
        if i == "quit" or i == 'q':
            break
        print(f"hello {i}")


async def got_stdin_data(q: asyncio.Queue):
    """note: this needs a EOF / Ctrl-D to actually terminate it"""
    try:
        while True:
            # print('name: ', end='', flush=True)
            res = sys.stdin.readline()
            # res = input('n?: ')
            res = res.strip('\n')
            print('[{}]'.format(res), flush=True)
            await q.put(res)
            await asyncio.sleep(0.1)  # need this to `nice` this coroutine
    finally:
        print('][ input done ][ ', flush=True)


async def write_stdout_data(q: asyncio.Queue):
    out = await q.get()
    # sys.stdout.write(out)
    print('hello {}'.format(out.decode()), flush=True)


async def greet(q: asyncio.Queue, reader: asyncio.Future = None):
    """
    loop: asyncio.AbstractEventLoop
    :param q:
    :return:
    """
    while True:
        name = await q.get()

        if not name:
            print('][break][')
            break

        if name == 'q' or name == 'quit':
            print('][quit][')
            break

        print('salvete, {}'.format(name), flush=True)
        # await asyncio.sleep(0.1)
        print('___', flush=True)
    # await proc.wait()
    print('[terminating]')
    if reader:
        reader.cancel()
        print('[reader cancelled]')


def run_pipe_mode():
    print('running pipe')
    q1 = asyncio.Queue()
    loop = asyncio.get_event_loop()
    # loop.add_reader(sys.stdin, got_stdin_data, q)
    # loop.add_writer(sys.stdout, write_stdout_data, q)
    readert = asyncio.ensure_future(got_stdin_data(q1))
    # greeter = asyncio.ensure_future(greet(q1, readert))
    # loop.run_until_complete(asyncio.wait([greeter]))
    loop.run_until_complete(greet(q1, readert))
    loop.run_until_complete(asyncio.wait([readert]))
    loop.close()
    print('[][]fin[][]')
    # loop.run_forever()


def arg_parser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument(
        "-+", "--pipe", action="store_true",
        help="Run in pipe mode")

    return parser


if __name__ == '__main__':
    args = arg_parser().parse_args()
    if args.pipe:
        run_pipe_mode()
        sys.exit(0)


    interact()
