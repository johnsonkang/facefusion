#!/usr/bin/env python3
"""
One-time strict validator for downloaded model files.
Checks CRC32 of each .onnx against its sibling .hash file.
"""
import sys
from pathlib import Path

from facefusion.hash_helper import compute_crc32


def main() -> int:
	root_path = Path(__file__).resolve().parent
	models_dir = root_path / '.assets' / 'models'

	if not models_dir.is_dir():
		print(f"models directory not found: {models_dir}")
		return 1

	onnx_files = sorted(models_dir.glob('*.onnx'))
	if not onnx_files:
		print("no .onnx files found to validate.")
		return 1

	failed = []

	for onnx_path in onnx_files:
		hash_path = onnx_path.with_suffix('.hash')
		expected_crc = hash_path.read_text().strip() if hash_path.is_file() else None
		actual_crc = compute_crc32(str(onnx_path))

		if expected_crc and actual_crc and expected_crc == actual_crc:
			print(f"[OK]    {onnx_path.name}")
		else:
			print(f"[FAIL]  {onnx_path.name} expected={expected_crc or 'missing'} actual={actual_crc or 'missing'}")
			failed.append(onnx_path.name)

	if failed:
		print(f"\nFailed {len(failed)} file(s): {', '.join(failed)}")
		return 1

	print(f"\nAll {len(onnx_files)} model files validated successfully.")
	return 0


if __name__ == '__main__':
	sys.exit(main())
