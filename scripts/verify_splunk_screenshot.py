"""Validate published PNG evidence structurally, without altering it.

The image is a size-reduced crop from an operator-provided real Splunk screen.
This validates PNG integrity, not authenticity of the remote Splunk job.
"""
import hashlib
from pathlib import Path
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "assets/evidence/splunk-native-dashboard-results.png"
PNG = b"\x89PNG\r\n\x1a\n"


def main():
    data = EVIDENCE.read_bytes()
    assert data.startswith(PNG), "Splunk screenshot is not a PNG"
    assert len(data) >= 1000, "Screenshot unexpectedly empty"
    pos = 8
    dimensions = None
    ended = False
    while pos < len(data):
        assert pos + 12 <= len(data), "Incomplete PNG chunk"
        count = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        end = pos + 12 + count
        assert end <= len(data), "Truncated PNG"
        body = data[pos + 8:pos + 8 + count]
        expected = struct.unpack(">I", data[pos + 8 + count:end])[0]
        assert zlib.crc32(kind + body) == expected, f"Corrupt PNG chunk {kind!r}"
        if kind == b"IHDR":
            dimensions = struct.unpack(">II", body[:8])
        if kind == b"IEND":
            ended = True
            assert end == len(data), "Trailing data in published screenshot"
            break
        pos = end
    assert ended and dimensions == (800, 193), f"Unexpected PNG dimensions {dimensions}"
    print("PASS: original-source cropped screenshot PNG CRC integrity, dimensions 800x193")
    print("Scope: screenshot image integrity, NOT source-job authentication")


if __name__ == "__main__":
    main()
