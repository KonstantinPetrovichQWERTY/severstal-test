import asyncio

from src.app import create_app

app = create_app()
if __name__ == "__main__":
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config.from_pyfile("hypercorn.conf.py")
    asyncio.run(serve(app, config, mode="asgi"))  # type: ignore
