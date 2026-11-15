#!/usr/bin/env python3
"""Inspect a LayerSeparator sample archive without extracting its files."""
import argparse
import io
import json
import struct
import sys
import zipfile
from pathlib import Path


def inspect(path):
    with zipfile.ZipFile(path) as outer:
        bad = outer.testzip()
        if bad:
            raise ValueError(f'corrupt outer ZIP member: {bad}')
        names = set(outer.namelist())
        for name in ('source.webp', 'sample-layers.psd', 'sample-layers.zip'):
            if name not in names:
                raise ValueError(f'missing {name}')
        with outer.open('sample-layers.psd') as psd:
            if psd.read(4) != b'8BPS':
                raise ValueError('invalid PSD signature')
        with zipfile.ZipFile(io.BytesIO(outer.read('sample-layers.zip'))) as layers_zip:
            bad = layers_zip.testzip()
            if bad:
                raise ValueError(f'corrupt nested ZIP member: {bad}')
            manifest = json.loads(layers_zip.read('manifest.json'))
            pngs = []
            for name in layers_zip.namelist():
                if name.lower().endswith('.png'):
                    with layers_zip.open(name) as png:
                        header = png.read(24)
                    if len(header) != 24 or header[:8] != b'\x89PNG\r\n\x1a\n' or header[12:16] != b'IHDR':
                        raise ValueError(f'invalid PNG header: {name}')
                    width, height = struct.unpack('>II', header[16:24])
                    pngs.append({'file': name, 'width': width, 'height': height})
            return {'archive': str(path), 'canvas': manifest.get('canvas'),
                    'layers': [x.get('name') for x in manifest.get('layers', [])],
                    'pngs': pngs, 'psd': 'signature valid; editor compatibility unverified'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.archive), ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        print(f'inspection failed: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
