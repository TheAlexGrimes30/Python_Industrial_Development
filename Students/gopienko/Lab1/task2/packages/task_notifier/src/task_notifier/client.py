import httpx


def configure_transport() -> None:
    client = httpx.Client(proxies=None)
    client.close()
