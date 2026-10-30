import os
import requests
import json
from dotenv import load_dotenv
from errors import APIError

load_dotenv()

api_key = os.getenv("API_KEY")
url = os.getenv("API_URL")
DONE = object()

def send_message(messages):
    pieces = []
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": messages,
        "stream": True
    }

    try:
        response = requests.post(url, headers=headers, json=payload, stream=True)
        if response.status_code != 200:
            try:
                error_json = response.json()
                error_message = error_json.get("error", {}).get("message", response.text)
            except Exception:
                error_message = response.text
                
            raise APIError(error_message, response.status_code)

        for line in response.iter_lines():
            parsed = parse_sse(line)

            if parsed is None:
                continue
            elif parsed is DONE:
                print("\n")
                return "".join(pieces)
            else:
                print(parsed, end="", flush=True)
                pieces.append(parsed)

           
    except requests.exceptions.RequestException as e:
        raise APIError(f"Network error: {str(e)}", 500) from e
        
    except (KeyError, IndexError) as e:
        raise APIError(f"Malformed response from API: {str(e)}", 500) from e
 

def parse_sse(line):
    if line == b'':
        return None
    decoded_line = line.decode("utf-8")
    data_value = decoded_line.removeprefix("data:").strip()

    if data_value == "[DONE]":
        return DONE

    try:
        parsed_data = json.loads(data_value)
        if "choices" in parsed_data and "content" in parsed_data["choices"][0]["delta"]:
            output = parsed_data["choices"][0]["delta"]["content"]
            return output
    except json.JSONDecodeError:
        return None   
