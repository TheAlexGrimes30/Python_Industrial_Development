import httpx


def configure_transport() -> None:
    client = httpx.Client()
    client.close()
