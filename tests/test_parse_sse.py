from pathlib import Path

from client import DONE, parse_sse

SAMPLE_STREAM = Path(__file__).parent / "data" / "sample_stream.txt"

EXPECTED_REPLY = (
    "Lines of code align,  \n"
    "Logic weaves through dark and light,  \n"
    "Syntax sings, divine.  "
)


def read_sample_lines():
    return SAMPLE_STREAM.read_bytes().splitlines()


def test_sample_stream_rebuilds_full_reply():
    pieces = []
    for line in read_sample_lines():
        parsed = parse_sse(line)
        if parsed is None:
            continue
        if parsed is DONE:
            break
        pieces.append(parsed)

    assert "".join(pieces) == EXPECTED_REPLY


def test_done_appears_once_and_last():
    results = [parse_sse(line) for line in read_sample_lines()]
    real_results = [r for r in results if r is not None]

    assert real_results.count(DONE) == 1
    assert real_results[-1] is DONE


def test_blank_line_is_skipped():
    assert parse_sse(b"") is None


def test_empty_delta_is_skipped():
    line = b'data: {"choices":[{"delta":{}}]}'
    assert parse_sse(line) is None


def test_model_saying_done_is_text_not_stop():
    line = b'data: {"choices":[{"delta":{"content":"DONE"}}]}'
    assert parse_sse(line) == "DONE"
