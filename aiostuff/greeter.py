#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Silly dumb example of aio with user interaction"""
import asyncio


async def get_input_data(q: asyncio.Queue):
    while True:
        await q.put(input('name: '))
        await asyncio.sleep(0.01)


async def greet(q: asyncio.Queue):
    proc = await asyncio.subprocess.create_subprocess_exec(
        "./hello.py", stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )
    while True:
        name = await q.get()
        proc.stdin.write('{}\n'.format(name).encode())
        await proc.wait()


async def test_queue(q: asyncio.Queue):
    while True:
        name = await q.get()
        print('hi {}'.format(name), flush=True)


if __name__ == '__main__':

    q = asyncio.Queue()
    loop = asyncio.get_event_loop()
    loop.create_task(get_input_data(q))
    loop.create_task(test_queue(q))
    loop.run_forever()
    loop.close()
