#
# codec.py
#
def encode_list(values: list[int]) -> bytes:
    return bytes(values)

def decode_list(encoded_values: bytes) -> list[int]:
    return list(encoded_values)