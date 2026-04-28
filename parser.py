import json
import re


def _strip_markdown_blocks(text: str) -> str:
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = re.sub(r"```", "", text)
    return text


def _find_json_candidates(text: str) -> list[str]:
    candidates = []
    i = 0
    while i < len(text):
        if text[i] == "{":
            depth = 0
            in_string = False
            escape_next = False
            start = i
            j = i
            while j < len(text):
                ch = text[j]
                if escape_next:
                    escape_next = False
                    j += 1
                    continue
                if ch == "\\" and in_string:
                    escape_next = True
                    j += 1
                    continue
                if ch == '"':
                    in_string = not in_string
                elif not in_string:
                    if ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            candidates.append(text[start:j + 1])
                            i = j
                            break
                j += 1
        i += 1
    return candidates


def _fix_unescaped_newlines(text: str) -> str:
    result = []
    in_string = False
    escape_next = False
    i = 0
    while i < len(text):
        ch = text[i]
        if escape_next:
            result.append(ch)
            escape_next = False
            i += 1
            continue
        if ch == "\\" and in_string:
            result.append(ch)
            escape_next = True
            i += 1
            continue
        if ch == '"':
            in_string = not in_string
            result.append(ch)
            i += 1
            continue
        if in_string and ch == "\n":
            result.append("\\n")
            i += 1
            continue
        if in_string and ch == "\r":
            result.append("\\r")
            i += 1
            continue
        if in_string and ch == "\t":
            result.append("\\t")
            i += 1
            continue
        result.append(ch)
        i += 1
    return "".join(result)


def _fix_trailing_commas(text: str) -> str:
    text = re.sub(r",\s*}", "}", text)
    text = re.sub(r",\s*]", "]", text)
    return text


def _fix_single_quotes(text: str) -> str:
    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        pass
    result = []
    in_double = False
    in_single = False
    escape_next = False
    i = 0
    while i < len(text):
        ch = text[i]
        if escape_next:
            result.append(ch)
            escape_next = False
            i += 1
            continue
        if ch == "\\" :
            result.append(ch)
            escape_next = True
            i += 1
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            result.append(ch)
            i += 1
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            result.append('"')
            i += 1
            continue
        result.append(ch)
        i += 1
    return "".join(result)


def _attempt_parse(candidate: str) -> dict | None:
    attempts = [
        candidate,
        _fix_unescaped_newlines(candidate),
        _fix_trailing_commas(candidate),
        _fix_trailing_commas(_fix_unescaped_newlines(candidate)),
        _fix_single_quotes(_fix_trailing_commas(_fix_unescaped_newlines(candidate))),
    ]
    for attempt in attempts:
        try:
            result = json.loads(attempt)
            if isinstance(result, dict):
                return result
        except (json.JSONDecodeError, ValueError):
            continue
    return None


def parse_llm_json(output: str) -> dict | None:
    if not output or not isinstance(output, str):
        print("[parse_llm_json] ERROR: input is empty or not a string")
        print(f"[parse_llm_json] RAW OUTPUT: {repr(output)}")
        return None

    try:
        cleaned = _strip_markdown_blocks(output)
        cleaned = cleaned.strip()

        candidates = _find_json_candidates(cleaned)

        if not candidates:
            inline_match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if inline_match:
                candidates = [inline_match.group(0)]

        if not candidates:
            print("[parse_llm_json] ERROR: no JSON object found in output")
            print(f"[parse_llm_json] RAW OUTPUT: {repr(output[:500])}")
            return None

        for candidate in candidates:
            result = _attempt_parse(candidate)
            if result is not None:
                return result

        print("[parse_llm_json] ERROR: found JSON-like structures but all failed to parse")
        print(f"[parse_llm_json] FIRST CANDIDATE: {repr(candidates[0][:300])}")
        print(f"[parse_llm_json] RAW OUTPUT: {repr(output[:500])}")
        return None

    except Exception as e:
        print(f"[parse_llm_json] UNEXPECTED ERROR: {e}")
        print(f"[parse_llm_json] RAW OUTPUT: {repr(output[:500])}")
        return None
