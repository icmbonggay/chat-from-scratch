import os
import requests
from dotenv import load_dotenv
from errors import APIError

load_dotenv()

api_key = os.getenv("API_KEY")
url = os.getenv("API_URL")

def send_message(messages):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": messages
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            try:
                error_json = response.json()
                error_message = error_json.get("error", {}).get("message", response.text)
            except Exception:
                error_message = response.text
                
            raise APIError(error_message, response.status_code)

        response_json = response.json()
        reply_text = response_json["choices"][0]["message"]["content"]
        return " ".join(reply_text.split())

    except requests.exceptions.RequestException as e:
        raise APIError(f"Network error: {str(e)}", 500) from e
        
    except (KeyError, IndexError) as e:
        raise APIError(f"Malformed response from API: {str(e)}", 500) from e
