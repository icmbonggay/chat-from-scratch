from pathlib import Path
from client import send_message

def load_system_prompt():
    prompt_path = Path(__file__).parent / "system_prompt.txt"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8").strip()
    else:
        return "You are a helpful assistant"



def main(): 
    system_prompt = load_system_prompt()
    history = [{"role": "system", "content": system_prompt}]

    while True:
        text = input("Enter your prompt: ")
        
        match text:
            case "/quit":
                break
            case "/reset":
                history = [history[0]]
            case _:
                history.append({"role": "user", "content": text})
                response = send_message(history)
                history.append({"role": "assistant", "content": response})




if __name__ == "__main__":
    main()

