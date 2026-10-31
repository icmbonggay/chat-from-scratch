from config import MODEL
import tiktoken

enc = tiktoken.encoding_for_model(MODEL)

TOKENS_PER_MESSAGE = 3
REPLY_PRIMING = 3


def count_tokens(messages):
    total = 0
    for message in messages:
        total += TOKENS_PER_MESSAGE
        total += len(enc.encode(message["role"]))
        total += len(enc.encode(message["content"]))
    return total + REPLY_PRIMING


def trim_history(history, budget):
    trimmed = history[:]  

    while len(trimmed) > 2 and count_tokens(trimmed) > budget:
        trimmed = [trimmed[0]] + trimmed[3:]  

    return trimmed