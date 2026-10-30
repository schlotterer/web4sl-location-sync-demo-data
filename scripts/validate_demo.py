#!/usr/bin/env python3
"""Validate the versioned CSV, its filter columns and its pinned image bytes."""
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess


def validate(root):
    manifest = json.loads((root / 'dataset.json').read_text())
    image_commit = manifest['image_commit']
    assert re.fullmatch(r'[0-9a-f]{40}', image_commit), 'Images need an exact commit'
    path = root / manifest['csv']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == manifest['csv_sha256'], 'CSV checksum differs'
    with path.open(newline='', encoding='utf-8-sig') as stream:
        records = list(csv.reader(stream))
    assert records[0] == manifest['columns'], 'CSV schema differs'
    assert len(records) - 1 == manifest['rows'] == 99, 'Expected 99 communities'
    assert len(records[0]) == len(set(records[0])) == 20, 'Expected 20 distinct columns'
    assert 'web4sl_sync_address_hash' not in records[0], 'Internal hash is not an import column'
    assert len(manifest['images']) == 100, 'Expected the original 100 images'
    assert set(manifest['images']) == {p.relative_to(root).as_posix() for p in (root / 'images').glob('*.jpeg')}, 'Image membership differs'
    for name, expected in manifest['images'].items():
        assert re.fullmatch(r'images/[a-z0-9-]+\.jpeg', name), 'Unexpected image path'
        data = (root / name).read_bytes()
        assert hashlib.sha256(data).hexdigest() == expected, f'Image checksum differs: {name}'
        pinned = subprocess.check_output(['git', 'show', f'{image_commit}:{name}'], cwd=root)
        assert pinned == data, f'Pinned image bytes differ: {name}'
    prefix = f"https://raw.githubusercontent.com/{manifest['image_repository']}/{image_commit}/"
    identities = set()
    referenced = set()
    for line, cells in enumerate(records[1:], 2):
        assert len(cells) == len(records[0]), f'Row {line}: shifted columns'
        row = dict(zip(records[0], cells))
        identity = (row['post_title'], row['location_city'], row['location_state'])
        assert all(identity) and identity not in identities, f'Row {line}: missing or duplicate community'
        identities.add(identity)
        assert row['managed_by'] in ('csv', 'cms'), f'Row {line}: invalid ownership'
        assert row['location_featured'] in ('0', '1'), f'Row {line}: invalid featured value'
        assert row['featured_image'].startswith(prefix), f'Row {line}: image URL is not pinned'
        image = row['featured_image'][len(prefix):]
        assert image in manifest['images'], f'Row {line}: unknown image'
        referenced.add(image)
        paths = [part.strip() for part in row['filters'].split('|') if part.strip()]
        assert paths and paths == json.loads(row['filters_json']), f'Row {line}: filter columns differ'
        assert all('/' in part and all(part.split('/')) for part in paths), f'Row {line}: invalid filter path'
        for key, bound in (('location_lat', 90), ('location_lng', 180)):
            if row[key]:
                assert -bound <= float(row[key]) <= bound, f'Row {line}: invalid coordinate'
    assert len(referenced) == 99, 'Expected one featured image per community'
    print(f"Validated {manifest['rows']} communities, 20 columns and 100 pinned image files")


if __name__ == '__main__':
    validate(Path(__file__).resolve().parents[1])
