import httpx, asyncio, os

async def test():
    api_key = os.environ.get("GRADIENT_API_KEY", "sk-do-4hojrk5BPCcUc9DIGE6N4FN0bfk3frNSyy5SmklVDhht4vguSWMVz2MYHe")
    base_url = "https://inference.do-ai.run/v1"
    model = "meta-llama/Meta-Llama-3.3-70B-Instruct"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Say hello in exactly 5 words."}],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    print(f"Testing Gradient AI at {base_url}...")
    print(f"Model: {model}")
    print(f"API Key: {api_key[:15]}...")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            r = await client.post(f"{base_url}/chat/completions", headers=headers, json=payload)
            print(f"Status: {r.status_code}")
            if r.status_code == 200:
                data = r.json()
                content = data["choices"][0]["message"]["content"]
                print(f"Response: {content}")
                print(f"Tokens used: {data.get('usage', {})}")
            else:
                print(f"Error: {r.text[:300]}")
        except Exception as e:
            print(f"Exception: {e}")

asyncio.run(test())
