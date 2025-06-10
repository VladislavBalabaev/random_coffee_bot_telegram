from opensearchpy import AsyncHttpConnection, AsyncOpenSearch

from nespresso.core.configs.settings import settings

client = AsyncOpenSearch(
    hosts=[
        {
            "host": "nespresso_opensearch",
            "port": 9200,
            "scheme": "http",
        }
    ],
    http_auth=("admin", settings.OPENSEARCH_INITIAL_ADMIN_PASSWORD.get_secret_value()),
    connection_class=AsyncHttpConnection,
    use_ssl=False,
    verify_certs=False,
)


async def CloseOpenSearchClient() -> None:
    await client.close()
