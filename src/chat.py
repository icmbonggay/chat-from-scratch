from history import trim_history
from pathlib import Path
from client import send_message
from config import INPUT_RATE, OUTPUT_RATE, BUDGET



def load_system_prompt():
    prompt_path = Path(__file__).parent / "system_prompt.txt"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8").strip()
    else:
        return "You are a helpful assistant"

def calculate_cost(usage_history):
    input_tokens = [i["prompt_tokens"] for i in usage_history]
    output_tokens = [i["completion_tokens"] for i in usage_history]
    session_cost = sum(input_tokens) * INPUT_RATE + sum(output_tokens) * OUTPUT_RATE
    return input_tokens, output_tokens, session_cost



def main(): 
    system_prompt = load_system_prompt()
    history = [{"role": "system", "content": system_prompt}]
    usage_history = []

    while True:
        text = input("Enter your prompt: ")
        
        match text:
            case "/quit":
                break
            case "/reset":
                history = [history[0]]
            case "/cost":
                input_tokens, output_tokens, session_cost = calculate_cost(usage_history)
                print("Input tokens: ", input_tokens)
                print("Output tokens: ", output_tokens)
                print("Session Cost: ","{:.10f}".format(session_cost))
            case _:
                history.append({"role": "user", "content": text})
                history = trim_history(history, BUDGET)
                response, usage = send_message(history)
                history.append({"role": "assistant", "content": response})
                usage_history.append(usage)




if __name__ == "__main__":
    main()

