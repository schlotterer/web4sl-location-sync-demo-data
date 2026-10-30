# Web4SL Location Sync demo data

Optional community records and photographs for demonstrating the Web4SL Location Sync directory. This is demo content, not a WordPress plugin. It is delivered separately so plugin updates remain small.

## Download and import

1. [Download the demo communities CSV](https://github.com/schlotterer/web4sl-location-sync-demo-data/releases/download/v1.0.1/web4sl-location-sync-demo-communities.csv).
2. On your network's main site, open Location Sync's Import Locations section.
3. Upload the CSV and select **Import Locations**. This creates 99 published directory locations and associated filter terms. Re-importing can update matching CSV-managed records, so use a demo or staging site.
4. Leave WordPress scheduled tasks running while the featured-image queue downloads the photos into the Media Library. Once downloaded, photos are served by that WordPress site.

An optional [complete demo bundle](https://github.com/schlotterer/web4sl-location-sync-demo-data/releases/download/v1.0.1/web4sl-location-sync-demo-data-1.0.1.zip) contains the CSV, all 100 images, these instructions and the dataset manifest. Upload the CSV to the importer, not the ZIP. The CSV still uses pinned public image URLs.

The admin's **Download Sample CSV** button provides a blank-start example for your own data. **Download Demo Communities CSV** provides this populated dataset.

The communities, contact details, addresses and descriptions are demonstration data, not a verified directory of real businesses. The original placeholder contact details are preserved. All 99 rows include latitude and longitude, so map pins can be imported without a Google API key or a geocoding request. Coordinates are approximate ZIP-area representative points for demo use, not verified locations of the sample street addresses. Records use `managed_by=csv`; change that column to `cms` if you want imported locations to remain manually editable.

## Dataset contract

Version 1.0.1 contains 99 community rows with the plugin's current 20-column schema, aligned CSV fields and matching pipe-separated/JSON filter paths. Removed internal address-hash columns are not included. `dataset.json` records the schema, source, row count and file SHA256 values.

The repository retains all 100 JPEGs from the original demo library, unchanged. One is not referenced by the 99-row dataset. Each CSV image URL pins the original image commit rather than a moving branch. Existing published datasets should retain their image commits; publish changes under a new dataset version.

To validate the checkout, run `python3 scripts/validate_demo.py`. Validation uses local Git history and does not contact a site or import any records. CI fetches full history so it can verify the pinned image bytes.

## Provenance

Extracted from the existing `schlotterer/web4sl-location-sync` demo library. The CSV is rebuilt from `_demo_communities-2025.csv`, with updated image URLs and the current import schema. No plugin source code, credentials or customer records are included. No new license grant for the photographs is implied by this extraction.

## Coordinate provenance

Latitude and longitude are the `INTPTLAT` and `INTPTLONG` representative internal points matched by five-digit `GEOID` from the [2026 U.S. Census Gazetteer ZIP Code Tabulation Areas file](https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.html). These are demo map positions, not street-address geocodes or verified business locations. ZIP fields retain leading zeroes.

The exact original reference archive is retained at `references/2026_Gaz_zcta_national.zip`; its source URL and SHA256 are recorded in `dataset.json`. Validation requires both finite, in-range coordinates for every row and checks them against that archived source. Existing image URLs and image bytes are unchanged from dataset 1.0.0.
