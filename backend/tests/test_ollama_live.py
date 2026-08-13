import httpx
import asyncio

async def test_models():
    url = "http://host.docker.internal:11434/api/generate"
    
    print("🤖 1. Probando Modelo de Texto (llama3.2:3b)...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json={
                "model": "llama3.2:3b",
                "prompt": "Responde brevemente en una frase: ¿Cuál es el número único de emergencias en Colombia?",
                "stream": False
            })
            print("Status:", resp.status_code)
            answer = resp.json().get("response", "").strip()
            print("Respuesta LLaMA:", answer)
            print("--------------------------------------------------")
    except Exception as e:
        print("Error en LLaMA:", e)
        
    print("👁️ 2. Probando Modelo de Visión (gemma3:4b)...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json={
                "model": "gemma3:4b",
                "prompt": "Responde brevemente en una frase: ¿Qué organismo atiende incendios en Cartagena?",
                "stream": False
            })
            print("Status:", resp.status_code)
            answer = resp.json().get("response", "").strip()
            print("Respuesta Gemma:", answer)
            print("--------------------------------------------------")
    except Exception as e:
        print("Error en Gemma:", e)

if __name__ == "__main__":
    asyncio.run(test_models())
