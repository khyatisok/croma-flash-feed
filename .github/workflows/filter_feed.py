import requests
import re
from lxml import etree

CAMPAIGN_URL = "https://www.croma.com/campaign/24hrs-flash-sale-offers/c/7442"
GMC_FEED = "https://www.croma.com/gmcfeed.xml"

print("Downloading campaign page...")

html = requests.get(CAMPAIGN_URL).text

skus = set(re.findall(r'"sku"\s*:\s*"(\d+)"', html))

print(f"Found {len(skus)} live SKUs")
print(skus)

print("Downloading GMC Feed...")

xml = requests.get(GMC_FEED).content

root = etree.fromstring(xml)

ns = {
    "g": "http://base.google.com/ns/1.0"
}

channel = root.find("channel")

items = channel.findall("item")

removed = 0

for item in items:

    sku = item.find("g:id", ns)

    if sku is None:
        continue

    if sku.text not in skus:
        channel.remove(item)
        removed += 1

print(f"Removed {removed} products")

tree = etree.ElementTree(root)

tree.write(
    "flash_sale_feed.xml",
    encoding="utf-8",
    xml_declaration=True,
    pretty_print=True
)

print("flash_sale_feed.xml created successfully")
