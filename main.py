"""Entry for make.fun's news-image-20261119 competition.

The entry is a single 1024x1024 PNG summarising the world news first reported
on Thursday 19 November 2026.  This program validates that bundled image and
ships it byte for byte to the output directory (``/output`` by default, or
``$MAKEFUN_OUTPUT_DIR`` when set).

It is deterministic: the same input file always produces the same output bytes,
and it writes nothing at all when validation fails.
"""

from __future__ import annotations

import os
import struct
import sys
from pathlib import Path
from typing import Iterator

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_FILE_BYTES = 1_048_576
MAX_DIMENSION = 1024
BIT_DEPTH_8 = 8
SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"


def repo_dir() -> Path:
    """Directory holding this program, i.e. where entry.png lives."""
    return Path(__file__).resolve().parent


def output_dir() -> Path:
    """Honour MAKEFUN_OUTPUT_DIR, otherwise write to /output."""
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    return Path(override) if override else Path("/output")


def read_source() -> bytes:
    """Read the bundled PNG, refusing anything over the size limit."""
    data = (repo_dir() / SOURCE_NAME).read_bytes()
    if len(data) > MAX_FILE_BYTES:
        raise ValueError(f"{SOURCE_NAME} is {len(data)} bytes, limit is {MAX_FILE_BYTES}")
    return data


def iter_chunks(data: bytes) -> Iterator[tuple[bytes, int, int]]:
    """Yield (kind, payload_start, payload_end) for every chunk in the file."""
    offset = 8
    while offset < len(data):
        if offset + 8 > len(data):
            raise ValueError("truncated chunk header")
        length, kind = struct.unpack(">I4s", data[offset : offset + 8])
        start = offset + 8
        end = start + length
        if end + 4 > len(data):
            raise ValueError(f"chunk {kind!r} declares {length} bytes past end of file")
        yield kind, start, end
        offset = end + 4


def validate_signature(data: bytes) -> None:
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("missing PNG signature")


def validate(data: bytes) -> None:
    """Validate the PNG signature, IHDR and every chunk through IEND."""
    validate_signature(data)
    if len(data) < 8 + 25:
        raise ValueError("file is too short to contain an IHDR chunk")

    first = True
    saw_iend = False
    for kind, start, end in iter_chunks(data):
        if first:
            if kind != b"IHDR":
                raise ValueError("first chunk is not IHDR")
            check_ihdr(data[start:end])
            first = False
        elif kind == b"IHDR":
            raise ValueError("duplicate IHDR chunk")
        elif kind == b"IEND":
            if end != start:
                raise ValueError("IEND chunk is not empty")
            if end + 4 != len(data):
                raise ValueError("data after IEND chunk")
            saw_iend = True

    if first:
        raise ValueError("missing IHDR chunk")
    if not saw_iend:
        raise ValueError("missing IEND chunk; file is truncated")


def check_ihdr(chunk: bytes) -> None:
    """Check the IHDR payload: dimensions and bit depth."""
    if len(chunk) != 13:
        raise ValueError("IHDR chunk is not 13 bytes")
    width, height = struct.unpack(">II", chunk[:8])
    bit_depth = chunk[8]
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise ValueError(f"image is {width}x{height}, limit is {MAX_DIMENSION}x{MAX_DIMENSION}")
    if bit_depth != BIT_DEPTH_8:
        raise ValueError(f"pixel data is {bit_depth}-bit, expected {BIT_DEPTH_8}-bit")


def main() -> int:
    try:
        data = read_source()
        validate(data)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    target_dir = output_dir()
    target = target_dir / OUTPUT_NAME
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    except OSError as exc:
        print(f"error: cannot write {target}: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {target} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
