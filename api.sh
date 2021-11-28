curl 'https://api.cnft.io/market/listings' \
  -H 'authority: api.cnft.io' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'content-type: application/json' \
  --data-raw '{"nsfw":false,"page":1,"priceMin":1000000,"priceMax":501000000,"project":"VeggieMates","search":"","sold":false,"sort":{"_id":-1},"verified":true,"types":["offer","listing"]}' \
  --compressed | jq