import asyncio
import httpx
import uuid
from typing import Any


BASE = "https://vipfapwm3x.us-east-1.awsapprunner.com/mcp"
DISCOVERY_PATHS = [
    "/tools",
    "/tools/list",
    "/tools/manifest",
    "/manifest",
]
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

async def try_get(client: httpx.AsyncClient, path: str) -> Any:
    url = BASE.rstrip("/") + path
    try:
        response = await client.get(url, headers=HEADERS, timeout=10.0)
        if response.status_code == 200:
            try:
                return response.json()
            except Exception:
                return response.text
        else:
            return {"status": response.status_code, "text": response.text[:200]}
    except Exception as e:
        return {"error": str(e)}
    
async def try_post(client: httpx.AsyncClient, path: str) -> Any:
    url = BASE.rstrip("/") + path
    try:
        response = await client.post(url, headers=HEADERS, timeout=10.0)
        if response.status_code == 200:
            try:
                return response.json()
            except Exception:
                return response.text
        else:
            return {"status": response.status_code, "text": response.text[:200]}
    except Exception as e:
        return {"error": str(e)}
    
async def try_post_jsonrpc(client: httpx.AsyncClient) -> Any:
    url = BASE.rstrip("/")
    payload = {"jsonrpc": "2.0", "id": str(uuid.uuid4()), "method": "tools/list", "params": {}}
    try:
        response = await client.post(url, headers=HEADERS, json=payload, timeout=10.0)
        if response.status_code == 200:
            try:
                return response.json()
            except Exception:
                return response.text
        else:
            return {"status": response.status_code, "text": response.text[:200]}
    except Exception as e:
        return {"error": str(e)}
    
async def main():
    async with httpx.AsyncClient(verify=True, timeout=20.0) as client:
        print("--- Trying discovery endpoints (GET) ---")
        for endpoint in DISCOVERY_PATHS:
            res = await try_get(client, endpoint)
            print(endpoint, "->", type(res).__name__)
            print(res)
            print("---")

        print("--- Trying discovery endpoints (POST) ---")
        for endpoint in DISCOVERY_PATHS:
            res = await try_post(client, endpoint)
            print(endpoint, "->", type(res).__name__)
            print(res)
            print("---")

        print("--- Trying discovery (JSON-RPC POST tools/list) ---")
        res = await try_post_jsonrpc(client)
        print("tools/list", "->", type(res).__name__)
        print(res)
        print("---")


if __name__ == "__main__":
    asyncio.run(main())