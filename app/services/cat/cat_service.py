import httpx
import os
from dotenv import load_dotenv
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.thecatapi.com/v1")
API_KEY = os.getenv("API_KEY")


class CatService:
    headers = {
        "x-api-key": API_KEY
    }

    @staticmethod
    async def get_all_breeds():
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/breeds", headers=CatService.headers)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_breed_by_id(breed_id: str):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{API_BASE_URL}/breeds/{breed_id}", headers=CatService.headers)
                if response.status_code == 404:
                    return None
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"API error: {e}")
                return None
            except Exception as e:
                print(f"Unexpected error: {e}")
                return None

    @staticmethod
    async def search_breeds(query: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/breeds/search", params={"q": query}, headers=CatService.headers)
            response.raise_for_status()
            return response.json()


