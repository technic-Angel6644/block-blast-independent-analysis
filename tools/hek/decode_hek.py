#!/usr/bin/env python3
"""Decode the examined HEK Type 01/03 formats with a caller-supplied key.

Adapted from Daybreak's supplied analysis/decrypt_hek.py. No application key,
game assets, or game code is included. See README.md for scope and validation.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
from pathlib import Path
import struct


HEADER_SIZE = 8
COMPRESSION_MAGIC = b"\xaf\xfa"


def xxtea_decrypt(payload: bytes, key: bytes) -> bytes:
    """Decode little-endian XXTEA words and validate the trailing byte count."""
    if len(key) != 16:
        raise ValueError("key must contain exactly 16 bytes")
    if len(payload) < 8 or len(payload) % 4:
        raise ValueError("XXTEA payload must contain at least two complete words")

    words = list(struct.unpack(f"<{len(payload) // 4}I", payload))
    key_words = struct.unpack("<4I", key)
    last = len(words) - 1
    delta = 0x9E3779B9
    total = ((6 + 52 // len(words)) * delta) & 0xFFFFFFFF
    y = words[0]
    while total:
        selector = (total >> 2) & 3
        for position in range(last, 0, -1):
            z = words[position - 1]
            mix = (
                (((z >> 5) ^ (y << 2)) + ((y >> 3) ^ (z << 4)))
                ^ ((total ^ y) + (key_words[(position & 3) ^ selector] ^ z))
            ) & 0xFFFFFFFF
            y = words[position] = (words[position] - mix) & 0xFFFFFFFF
        z = words[last]
        mix = (
            (((z >> 5) ^ (y << 2)) + ((y >> 3) ^ (z << 4)))
            ^ ((total ^ y) + (key_words[selector] ^ z))
        ) & 0xFFFFFFFF
        y = words[0] = (words[0] - mix) & 0xFFFFFFFF
        total = (total - delta) & 0xFFFFFFFF

    decoded = struct.pack(f"<{len(words)}I", *words)
    length = int.from_bytes(decoded[-4:], "little")
    if not len(decoded) - 7 <= length <= len(decoded) - 4:
        raise ValueError("invalid XXTEA plaintext length")
    return decoded[:length]


def decode(blob: bytes, key: bytes) -> bytes:
    """Return decoded bytes; never evaluate or execute the recovered payload."""
    if len(key) != 16:
        raise ValueError("key must contain exactly 16 bytes")
    if len(blob) < HEADER_SIZE or blob[:4] != b"HEK:":
        raise ValueError("not a complete HEK header")

    variant = blob[4]
    payload = blob[HEADER_SIZE:]
    if variant == 3:
        decoded = bytes(value ^ key[index % len(key)]
                        for index, value in enumerate(payload))
        return gzip.decompress(decoded) if decoded.startswith(b"\x1f\x8b") else decoded
    if variant != 1:
        raise ValueError(f"unsupported HEK type {variant:02x}")

    decoded = xxtea_decrypt(payload, key)
    if not decoded.startswith(COMPRESSION_MAGIC):
        return decoded
    if len(decoded) < 6:
        raise ValueError("truncated Type 01 compression wrapper")
    expected_size = int.from_bytes(decoded[2:6], "big")
    try:
        import brotli
    except ImportError as error:
        raise RuntimeError("compressed Type 01 input requires the Brotli Python package") from error
    try:
        expanded = brotli.decompress(decoded[6:])
    except brotli.error as error:
        raise ValueError("invalid Type 01 Brotli stream") from error
    if len(expanded) != expected_size:
        raise ValueError(f"Brotli size mismatch: expected {expected_size}, got {len(expanded)}")
    return expanded


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path, help="new file; existing files are never overwritten")
    parser.add_argument("--key-file", type=Path, required=True,
                        help="local file containing exactly 16 raw bytes, without a newline")
    args = parser.parse_args()
    try:
        decoded = decode(args.input.read_bytes(), args.key_file.read_bytes())
        with args.output.open("xb") as destination:
            destination.write(decoded)
    except (OSError, EOFError, ValueError, RuntimeError) as error:
        parser.exit(1, f"decode_hek: {error}\n")
    print(f"decoded {len(decoded)} bytes; SHA-256 {hashlib.sha256(decoded).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
