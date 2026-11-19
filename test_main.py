"""Regression tests for main.py's PNG validators (standard library only)."""

import struct
import tempfile
import unittest
from pathlib import Path

import main

REPO = Path(__file__).resolve().parent
ENTRY = REPO / "entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _chunk(kind: bytes, payload: bytes) -> bytes:
    return struct.pack(">I", len(payload)) + kind + payload + b"\x00\x00\x00\x00"


def _png_over_limit() -> bytes:
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    filler = _chunk(b"tEXt", b"\x00" * main.MAX_FILE_BYTES)
    return PNG_SIGNATURE + _chunk(b"IHDR", ihdr) + filler + _chunk(b"IEND", b"")


class ValidateTests(unittest.TestCase):
    def test_good_image_passes(self):
        main.validate(ENTRY.read_bytes())

    def test_truncated_image_refused(self):
        data = ENTRY.read_bytes()
        for cut in (len(data) // 2, len(data) - 12, 20):
            with self.subTest(cut=cut):
                with self.assertRaises(ValueError):
                    main.validate(data[:cut])

    def test_oversize_image_refused(self):
        data = _png_over_limit()
        self.assertGreater(len(data), main.MAX_FILE_BYTES)
        with self.assertRaises(ValueError):
            main.validate(data)


if __name__ == "__main__":
    unittest.main()
