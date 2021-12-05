import json

def construct_sales_url(listing_id:str) -> str:
    return f"https://cnft.io/token/{listing_id}"

def process_data():
    with open('listings.json') as f:
        listings = json.load(f)

    with open('metadata.json') as f:
        metadata = json.load(f)

    for item in metadata:
        listing = listings.get(item["name"])
        if listing is not None:
            item["price_lovelace"] = listing["price_lovelace"]
            item["sales_url"] = construct_sales_url(listing["listing_id"])
        else:
            item["price_lovelace"] = None
            item["sales_url"] = None

    sorted_serial = sorted(metadata, key=lambda x: x['serial'])
    filtered_price = [item for item in metadata if item["price_lovelace"] is not None]
    sort_by_date = sorted(filtered_price, key=lambda x: x['listing_id'], reverse=True)
    sorted_price = sorted(sort_by_date, key=lambda x: x['price_lovelace'])
    indexed_final = {
        int(item["serial"]): item
        for item in metadata
    }

    with open("metadata_serial_sorted.json", "w") as f:
        json.dump(sorted_serial, f)
        
    with open("metadata_price_sorted.json", "w") as f:
        json.dump(sorted_price, f)
        
    with open("metadata_indexed.json", "w") as f:
        json.dump(indexed_final, f)
