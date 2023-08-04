import asyncio

from core.crypto import Crypto
from core.ui.cli import offline
from core.ui.cli import online


def start(instance: Crypto) -> None:
    print("Start offline? (y/n)")
    answer = input()
    if 'y' in answer.lower():
        offline.init(instance)
    else:
        asyncio.run(online.init(instance))
