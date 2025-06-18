"""Запуск приложения без докера."""

import uvicorn

if __name__ == "__main__":
    config = uvicorn.Config(app="studlk.main:app", reload=True)
    server = uvicorn.Server(config)
    server.run()
