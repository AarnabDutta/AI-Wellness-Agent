import requests
import os
import json

class UnifiedLLMClient:
    def __init__(self, api_url=None, api_key=None, default_model=None):
        self.api_url = api_url or os.getenv("OPENROUTER_API_URL")
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.default_model = default_model or os.getenv("LLAMA_MODEL_ID")

        missing = []
        if not self.api_url:
            missing.append('OPENROUTER_API_URL')
        if not self.api_key:
            missing.append('OPENROUTER_API_KEY')
        if not self.default_model:
            missing.append('LLAMA_MODEL_ID or default_model')
        if missing:
            raise ValueError(f"Missing required .env variables: {', '.join(missing)}")

    def generate_response(
        self, prompt, history=None, system_prompt=None,
        temperature=0.2, max_tokens=1024, model=None, extra_headers=None
    ):
        messages = history[:] if history else []
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        if extra_headers:
            headers.update(extra_headers)
        
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        try:
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload), timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        except Exception as e:
            try:
                print("API error details:", response.json())
            except Exception:
                pass
            print("Exception:", e)
            return "Sorry, the AI service is temporarily unavailable."

    def generate_response_stream(
        self, prompt, history=None, system_prompt=None,
        temperature=0.2, max_tokens=1024, model=None, extra_headers=None
    ):
        messages = history[:] if history else []
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        if extra_headers:
            headers.update(extra_headers)
        
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True      # Streaming enabled here
        }
        try:
            with requests.post(self.api_url, headers=headers, data=json.dumps(payload), stream=True, timeout=60) as response:
                response.raise_for_status()
                full_reply = ""
                for line in response.iter_lines():
                    if line:
                        try:
                            dataline = line.decode("utf-8")
                            if dataline.startswith("data: "):
                                dataline = dataline[6:].strip()
                            if dataline == "[DONE]":
                                break
                            data = json.loads(dataline)
                        except Exception:
                            continue

                        if "choices" in data and data["choices"]:
                            delta = data["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                print(content, end="", flush=True)
                                full_reply += content
                print()  # Newline after completion
                return full_reply
        except Exception as e:
            try:
                print("Streaming API error details:", response.json())
            except Exception:
                pass
            print("Streaming Exception:", e)
            return "Sorry, the AI service is temporarily unavailable."

if __name__ == "__main__":
    llm = UnifiedLLMClient()
    print("==== NON-STREAMING TEST ====")
    reply = llm.generate_response(
        "Is this multi-provider wrapper working?", 
        system_prompt="You are an AI wellness coach."
    )
    print(reply)

    print("==== STREAMING TEST ====")
    reply_stream = llm.generate_response_stream(
        "Say hi in a streaming fashion.", 
        system_prompt="You are an AI wellness coach."
    )
    # reply_stream output is already printed live, but available for use if needed
