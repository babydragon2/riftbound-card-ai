import requests
import os

# URL of the Riftbound card gallery
url = "https://cdn.rgpub.io/public/live/map/riftbound/latest/OGN/cards/OGN-002/full-desktop.jpg"

# Directory to save images
save_dir = "riftbound_card_images"
if not os.path.exists(save_dir):
    
    os.makedirs(save_dir)

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

# Download each image
for i in range(0, 400):
    code = f"{i:03}"
    url = f"https://cdn.rgpub.io/public/live/map/riftbound/latest/OGN/cards/OGN-{code}/full-desktop.jpg"

    try:
        # Download the image
        img_response = requests.get(url, headers=headers)
        img_response.raise_for_status()

        # Generate a filename (e.g., card_1.jpg)
        img_name = f"OGN_{code}.{url.split('.')[-1]}"
        img_path = os.path.join(save_dir, img_name)

        
        if os.path.exists(img_path):
            print(f"Already exists: {img_name}, skipping.")
            continue

        # Save the image
        with open(img_path, "wb") as f:
            f.write(img_response.content)
        print(f"Downloaded: {img_name}")
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")

print(f"Finished downloading images to {save_dir}")

