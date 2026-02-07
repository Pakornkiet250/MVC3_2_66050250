def valid_8digit_id(x: str) -> bool:
    return isinstance(x, str) and len(x) == 8 and x.isdigit() and x[0] != "0"
