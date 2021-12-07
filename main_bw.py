import requests
from pydantic import BaseModel
import json
from datetime import datetime
import time

from data_processing import process_data
from gcloud_utils import upload_blob

import logging


def main():
    headers = {
        "authority": "api.cnft.io",
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
    }

    class CNFTlisting(BaseModel):
        listing_id: str
        asset_id: str
        price_lovelace: int

    def get_price_data(data: dict) -> CNFTlisting:
        listing = CNFTlisting(
            listing_id=data["_id"],
            asset_id=data["asset"]["assetId"],
            price_lovelace=data["price"],
        )
        return listing

    final_data = {}

    page = 1
    while True:
        http_data = (
            '{"nsfw":false,"page":'
            f"{page}"
            ',"project":"VeggieMates Exclusives","search":"","sold":false,"sort":{"price":1},"verified":true,"types":["offer","listing"]}'
        )

        response = requests.post(
            "https://api.cnft.io/market/listings", headers=headers, data=http_data
        )
        print(f"Getting {page=}")

        if response.status_code != 200:
            raise Exception("Http response not 200")

        try:
            response_data = response.json()
        except Exception as e:
            print(e)

        try:
            if len(response_data["results"]) == 0:
                break
        except Exception as e:
            print(e)
            print(response_data)

        for data in response_data["results"]:
            listing = get_price_data(data)
            final_data[listing.asset_id] = listing.dict()

        page += 1

    print(f"Total listing : {len(final_data.keys())}")

    with open("listings_bw.json", "w") as f:
        json.dump(final_data, f)

    print("Processing BW Data")
    process_data(suffix="_bw")
    print("Processing BW Data Done")

    # Metadata
    meta = {"last_updated": f"{str(datetime.utcnow())} UTC"}

    with open("meta_bw.json", "w") as f:
        json.dump(meta, f)

    bucket_name = "vegexplore.jaye.es"

    # Uploading to GCS
    upload_blob(
        bucket_name=bucket_name,
        source_file_name="meta_bw.json",
        destination_blob_name="data/meta_bw.json",
    )

    upload_blob(
        bucket_name=bucket_name,
        source_file_name="metadata_serial_sorted_bw.json",
        destination_blob_name="data/metadata_serial_sorted_bw.json",
    )

    upload_blob(
        bucket_name=bucket_name,
        source_file_name="metadata_price_sorted_bw.json",
        destination_blob_name="data/metadata_price_sorted_bw.json",
    )

    upload_blob(
        bucket_name=bucket_name,
        source_file_name="metadata_indexed_bw.json",
        destination_blob_name="data/metadata_indexed_bw.json",
    )


if __name__ == "__main__":
    while True:
        try:
            print(f"Start fetching data. Time now:{datetime.utcnow()}")
            main()
            print(f"Resting for 60 secs")
            time.sleep(60)
        except Exception as e:
            print(e)