#!/usr/bin/env python3
"""Verify privately retained evidence archives without extracting their contents.

Usage:
    python3 tools/verify_hashes.py --root /path/to/private/evidence
    python3 tools/verify_hashes.py --root /path/to/private/evidence --archive 'android10.tar(1).gz'

The --root folder should contain the files named in evidence/hashes.sha256.
Repeat --archive to verify selected available archives; omit it to check all.
This script uses only the Python standard library. It never executes game code.
"""
import argparse
import csv
import hashlib
import io
from pathlib import Path
import sys
import tarfile


REPO_ROOT = Path(__file__).resolve().parents[1]


def digest_and_size(stream):
    digest = hashlib.sha256()
    count = 0
    while True:
        block = stream.read(1024 * 1024)
        if not block:
            break
        digest.update(block)
        count += len(block)
    return digest.hexdigest(), count


def expected_archives():
    manifest = REPO_ROOT / "evidence" / "hashes.sha256"
    for lineno, text in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        if not text.strip() or text.lstrip().startswith("#"):
            continue
        parts = text.split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError(f"{manifest}:{lineno}: invalid SHA-256 line")
        yield parts[1].strip().lstrip("*"), parts[0]


def expected_members():
    manifest = REPO_ROOT / "evidence" / "internal-hashes.tsv"
    with manifest.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            yield row["archive"], row["member"], row["sha256"], int(row["size_bytes"])


def run(evidence_root, selected_archives=None):
    failed = 0
    archives_ok = set()
    if selected_archives is not None:
        selected_archives = set(selected_archives)
        unknown = selected_archives - {name for name, _ in expected_archives()}
        if unknown:
            raise ValueError(f"unknown archive selection: {', '.join(sorted(unknown))}")
    for name, expected_hash in expected_archives():
        if selected_archives is not None and name not in selected_archives:
            continue
        path = evidence_root / name
        if not path.is_file():
            print(f"MISSING  {name}")
            failed += 1
            continue
        with path.open("rb") as stream:
            actual_hash, count = digest_and_size(stream)
        if actual_hash != expected_hash:
            print(f"FAIL     {name}: expected {expected_hash}; got {actual_hash}")
            failed += 1
        else:
            print(f"OK       {name} ({count:,} bytes)")
            archives_ok.add(name)

    grouped = {}
    for name, member, digest, size in expected_members():
        if selected_archives is not None and name not in selected_archives:
            continue
        grouped.setdefault(name, []).append((member, digest, size))

    for name, members in grouped.items():
        if name not in archives_ok:
            print(f"SKIP     {len(members)} member(s) of {name}: archive unverified")
            continue
        try:
            with tarfile.open(evidence_root / name, "r:gz") as archive:
                for member, expected_hash, expected_size in members:
                    try:
                        entry = archive.getmember(member)
                        if not entry.isfile():
                            raise ValueError("not a regular file")
                        content = archive.extractfile(entry)
                        if content is None:
                            raise ValueError("no readable payload")
                        with content:
                            actual_hash, actual_size = digest_and_size(content)
                        correct = actual_hash == expected_hash and actual_size == expected_size
                        if correct:
                            print(f"OK       {name}:{member}")
                        else:
                            print(f"FAIL     {name}:{member}: hash/size mismatch")
                            failed += 1
                    except (KeyError, ValueError, OSError) as error:
                        print(f"FAIL     {name}:{member}: {error}")
                        failed += 1
        except (OSError, tarfile.TarError) as error:
            print(f"FAIL     cannot read {name}: {error}")
            failed += len(members)

    print(f"\nResult: {'PASS' if failed == 0 else f'{failed} failure(s)'}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True,
                        help="Private directory containing IPA and tar.gz evidence")
    parser.add_argument("--archive", action="append", choices=sorted(name for name, _ in expected_archives()),
                        help="Verify only this listed archive; may be repeated")
    args = parser.parse_args()
    sys.exit(run(args.root.expanduser().resolve(), args.archive))
