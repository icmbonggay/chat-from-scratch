from history import count_tokens, trim_history


def make_history(pairs):
    history = [{"role": "system", "content": "You are a helpful assistant."}]
    for n in range(1, pairs + 1):
        history.append({"role": "user", "content": f"Question {n}: tell me about topic {n}."})
        history.append({"role": "assistant", "content": f"Answer {n}: here is some detail about topic {n}."})
    return history


def test_under_budget_nothing_changes():
    history = make_history(3)
    budget = count_tokens(history)

    result = trim_history(history, budget)

    assert result == history


def test_over_budget_oldest_pair_goes_first():
    history = make_history(3)
    budget = count_tokens(history) - 1

    result = trim_history(history, budget)

    assert result == [history[0]] + history[3:]


def test_system_prompt_always_stays():
    history = make_history(3)

    result = trim_history(history, budget=1)

    assert result[0] == history[0]
    assert result[0]["role"] == "system"


def test_long_chat_stays_under_budget():
    history = make_history(50)
    budget = 200

    result = trim_history(history, budget)

    assert count_tokens(result) <= budget
    assert result[0] == history[0]
    assert result[-1] == history[-1]


def test_original_history_is_not_changed():
    history = make_history(3)
    original = [dict(message) for message in history]

    trim_history(history, budget=1)

    assert history == original
