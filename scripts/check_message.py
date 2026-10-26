from client import send_message


messages = [
    {"role": "user", "content": "Write a haiku about coding. It should rhyme"}
]

print(send_message(messages))