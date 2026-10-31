from client import send_message


messages = [
    {"role": "user", "content": "Write a haiku about coding. It should rhyme"}
]

response, usage = send_message(messages)
print(usage)
