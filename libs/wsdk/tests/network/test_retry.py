import pytest

from wsdk.network.http import retry


@retry(retries=3, delay=0.1)
async def fetch(url: str) -> bytes:
    import httpx

    with httpx.Client() as client:
        response = client.get(url)
        return response.read()


@retry(retries=3, delay=0.1)
def fetch_sync(url: str) -> bytes:
    import httpx

    with httpx.Client() as client:
        response = client.get(url)
        return response.read()


@pytest.mark.asyncio
async def test_fetch_with_retry():
    url = "https://httpbin.org/get"

    assert await fetch(url)
    assert fetch_sync(url)
