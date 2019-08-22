#!/usr/bin/env python
# -*- coding: utf-8 -*-


def square(x: float) -> float:
    return x * x

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.add_reader(
        sys.stdin.fileno(), lambda x: print(sys.stdin.read()))
    loop.run_forever()