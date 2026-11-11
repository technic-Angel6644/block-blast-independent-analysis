"""Synthetic decoder checks; all keys and payloads here are test data.

Fixed XXTEA ciphertexts were generated with a separate C encoder during the
tooling review. The compressed payload was also decoded with Node's Brotli
implementation. No application assets or application key are used.
"""

import gzip
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from decode_hek import decode, xxtea_decrypt


KEY = bytes(range(16))
HEADER = b"HEK:\x01\x00\x00\x00"
PLAIN = b"Independent HEK fixture.\x00Binary tail\xff"
RAW_VECTORS = {
    1: "39fdedec1b2eda73",
    2: "2057b300e7afff4d",
    3: "4b76449b5b8af48e",
    4: "96624779a283d89c",
    5: "c66e9f765a5e82e60ea1e73a",
    24: "ba2001735741496e1f6aba4b3147eb340669205e4ebe3ae92c60aa11",
    25: "4464c2442cd0298e16e127207afe62f21cc69dcea19b82bd8a1da09f5580409e",
    26: "445fbfd944b5c125c946bd577135c6b772f46f6bf54814f952623f999709c7f4",
}
WRAPPED = bytes.fromhex(
    "5da3abdcc606571ef59b0dbe60d87212c155b0f1ebf1fb15342b9f02e346b8d6"
    "70117bda7da8f6f1108a26b6af0cd0789e770775"
)
BAD_SIZE = bytes.fromhex(
    "f8d407dbe23621f4dda097cb0321c55cddda167279da415448679d4f59b281d60"
    "010d58af737bac93ad22c557c4e0797481d1be5"
)


def type03(payload):
    return b"HEK:\x03\x00\x00\x00" + bytes(
        value ^ KEY[index % len(KEY)] for index, value in enumerate(payload)
    )


class DecoderTests(unittest.TestCase):
    def test_fixed_xxtea_vectors_and_padding(self):
        for length, ciphertext in RAW_VECTORS.items():
            with self.subTest(length=length):
                payload = bytes.fromhex(ciphertext)
                self.assertEqual(xxtea_decrypt(payload, KEY), bytes(range(length)))
                self.assertEqual(decode(HEADER + payload, KEY), bytes(range(length)))

    def test_brotli_wrapper(self):
        self.assertEqual(decode(HEADER + WRAPPED, KEY), PLAIN)

    def test_brotli_declared_length(self):
        with self.assertRaisesRegex(ValueError, "size mismatch"):
            decode(HEADER + BAD_SIZE, KEY)

    def test_truncated_wrapper(self):
        with self.assertRaisesRegex(ValueError, "truncated"):
            decode(HEADER + bytes.fromhex("8b8b577ea0ef1024"), KEY)

    def test_invalid_brotli(self):
        with self.assertRaisesRegex(ValueError, "Brotli stream"):
            decode(HEADER + bytes.fromhex("c743c2e38fd09592c043cd54"), KEY)

    def test_type03_uncompressed(self):
        self.assertEqual(decode(type03(PLAIN), KEY), PLAIN)

    def test_type03_gzip(self):
        self.assertEqual(decode(type03(gzip.compress(PLAIN, mtime=0)), KEY), PLAIN)

    def test_header_validation(self):
        for blob in [b"", b"HEK:\x01", b"NOPE\x03\x00\x00\x00"]:
            with self.subTest(blob=blob), self.assertRaises(ValueError):
                decode(blob, KEY)

    def test_unsupported_variant(self):
        with self.assertRaisesRegex(ValueError, "unsupported"):
            decode(b"HEK:\x02\x00\x00\x00", KEY)

    def test_key_length(self):
        for key in [b"", KEY[:-1], KEY + b"\x00"]:
            with self.subTest(length=len(key)), self.assertRaisesRegex(ValueError, "16 bytes"):
                decode(HEADER + WRAPPED, key)

    def test_ciphertext_word_count(self):
        for payload in [b"", b"\x00" * 4, b"\x00" * 9]:
            with self.subTest(length=len(payload)), self.assertRaisesRegex(ValueError, "words"):
                xxtea_decrypt(payload, KEY)

    def test_invalid_trailing_length(self):
        with self.assertRaisesRegex(ValueError, "plaintext length"):
            xxtea_decrypt(bytes(8), KEY)

    def test_cli_output_and_overwrite_refusal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output, key = root / "input", root / "output", root / "test.key"
            source.write_bytes(type03(PLAIN))
            key.write_bytes(KEY)
            command = [sys.executable, str(Path(__file__).with_name("decode_hek.py")),
                       str(source), str(output), "--key-file", str(key)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(output.read_bytes(), PLAIN)
            self.assertIn("SHA-256", first.stdout)
            second = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(output.read_bytes(), PLAIN)

    def test_cli_invalid_input_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output, key = root / "input", root / "output", root / "test.key"
            source.write_bytes(b"not an HEK container")
            key.write_bytes(KEY)
            result = subprocess.run(
                [sys.executable, str(Path(__file__).with_name("decode_hek.py")),
                 str(source), str(output), "--key-file", str(key)],
                capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
