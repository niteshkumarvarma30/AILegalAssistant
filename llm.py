import requests

def generate_summary(query, docs, role, model="llama3"):
    # Compose the prompt with context from docs and role
    context = "\n".join(docs) if docs else ""
    prompt = f"Role: {role}\nContext: {context}\nQuestion: {query}"
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )
    response.raise_for_status()
    result = response.json()
    return result.get("response", "No answer generated.")