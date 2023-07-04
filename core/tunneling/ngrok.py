def init() -> str:
    from fastapi.logger import logger
    from pyngrok import ngrok
    import sys

    # Get the dev server address and port (defaults to 8000 for Uvicorn, can be overridden with `--port`)
    address = sys.argv[sys.argv.index("--address") + 1] if "--address" in sys.argv else "127.0.0.1"
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000

    # Open a ngrok tunnel to the dev server
    public_url = ngrok.connect(port).public_url
    logger.info("ngrok tunnel \"{}\" -> \"http://{}:{}\"".format(public_url, address, port))

    # Return the public ngrok URL
    return public_url
