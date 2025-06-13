import httpx


async def TriggerFetchByNesEmail(email: str) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://external.nes.ru/api/trigger_fetch",
            params={"email": email},
            headers={"Authorization": "..."},
        )
        # response = await client.post(
        #     "https://external.nes.ru/api/trigger_fetch",
        #     json={"email": email},
        #     headers={"Authorization": "..."}
        # )

        response.raise_for_status()
