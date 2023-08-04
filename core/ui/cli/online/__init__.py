from typing import Coroutine, Callable

from core.crypto import Crypto


def __init_listener(instance: Crypto) -> Callable[[], Coroutine]:
    from core.handler import listener
    import uvicorn

    config = uvicorn.Config(listener.init(instance), port=8000, log_level="info")
    server = uvicorn.Server(config)

    return server.serve


def __init_tunnel() -> str:
    from core.tunneling import ngrok

    # Start the tunnel
    return ngrok.init()


async def init(instance: Crypto) -> None:
    import asyncio

    # Start the listener
    listener_task = asyncio.create_task(__init_listener(instance)())

    tunnel_url = __init_tunnel()
    print("Tunnel URL: {}".format(tunnel_url))

    ''' UI '''
    await asyncio.sleep(50)
