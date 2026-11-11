# HEK decoding and synthetic verification

[decode_hek.py](decode_hek.py) adapts the supplied Daybreak `analysis/decrypt_hek.py` into a standalone tool with a caller-supplied key. The byte transforms follow that source; this is not a claim of a newly discovered format. The original script and its private source archive are identified in [the tooling review](../../evidence/analysis-tooling.md).

The public adaptation removes embedded application key material, adds explicit errors for unsupported inputs, and refuses to overwrite an existing output file. It does not execute recovered JavaScript, fetch CDN resources, or connect to a device.

## Usage

Use Python 3.10 or later. Compressed Type 01 input also requires the `Brotli` Python package. Supply the independently obtained key in a local file containing exactly 16 raw bytes, without a trailing newline. No application key is distributed here.

```bash
python3 tools/hek/decode_hek.py /path/to/private/input.hek /path/to/private/output.bin \
  --key-file /path/to/private/local.key
```

The output path must be new. The tool prints the decoded byte count and SHA-256. Compare that hash and the relevant source path with the evidence manifests; successful decoding alone does not authenticate an asset or establish its distribution date.

## Implemented layout

| Bytes | Handling in the supplied implementation |
| --- | --- |
| 0–3 | Must equal ASCII `HEK:` |
| 4 | Variant: `01` or `03` |
| 5–7 | Skipped; their meaning is not established by this script |
| 8 onward | Variant-specific payload |

**Type 01:** Decode the payload as little-endian 32-bit XXTEA words with a 16-byte key. The final decoded word stores the plaintext byte count. Validate it against the available words and remove padding. If the result starts with `af fa`, read the following four bytes as the expected decompressed size in big-endian order, decompress the remaining bytes as Brotli, and compare the actual size. Otherwise, return the decoded bytes directly.

**Type 03:** Apply repeating XOR with the supplied 16-byte key, starting at payload index zero. If the result begins with gzip magic `1f 8b`, decompress it; otherwise return it directly. The examined source uses the same key for both variants. That does not establish that every application build does so.

These checks are format checks, not cryptographic authentication. In particular, Type 03 data without gzip and uncompressed Type 01 data have no content checksum in this implementation. The decoder handles whole buffers in memory and is research tooling rather than a hardened file-processing service.

## Validation and limits

```bash
python3 -m unittest discover -s tools/hek -p 'test_*.py' -v
```

[test_decode_hek.py](test_decode_hek.py) uses only synthetic payloads and a synthetic key. Fixed XXTEA fixtures were produced with a separate C encoder, covering several padding lengths. The Brotli fixture was also decoded with Node's `zlib` implementation. Tests cover both HEK variants, compressed and uncompressed paths, malformed wrappers, declared-size errors, key length, and output overwrite refusal.

The synthetic suite passed using Python 3.13.5 and Brotli 1.1.0 during the initial tooling update.

With the additional Android archive supplied on 12 November 2026, the public decoder was also checked against real retained assets. Three APK-embedded settings files decode byte-for-byte to their evaluator captures. The encrypted 700f5 standard reward-harvest module decodes to the retained source and all four matching trait captures. Its Type 03 bundle configuration decodes to the same parsed JSON object as the retained counterpart. The [Android verification report](../../findings/android-multiversion.md) identifies those files and hashes and distinguishes package metadata from later runtime resources.

These checks validate decoding and source identity, not final gameplay execution. The original iOS IPA and separate Android 10.8.1 archive were not re-examined during this supplementary update; their earlier checks remain separately reported in [the methodology](../../methodology.md).
