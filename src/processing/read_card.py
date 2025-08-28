import cv2
import pytesseract
#import psycopg2
import re
from datetime import datetime

class RiftboundCard:
    def __init__(self, name, card_type, mana_cost, attack, health, ability_text, rarity):
        self.name = name
        self.card_type = card_type
        self.mana_cost = mana_cost
        self.attack = attack
        self.health = health
        self.ability_text = ability_text
        self.rarity = rarity

def minimal_preprocess(image_path):
    img = cv2.imread(image_path)  # Works for .avif if OpenCV supports it
    if img is None:
        raise ValueError(f"Failed to load {image_path}. Check OpenCV/libavif support.")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    return gray

def extract_text(image):
    text = pytesseract.image_to_string(image, config='--psm 3')
    print("Extracted Raw Text: ", text)
    return text

def parse_card(text):
    name_match = re.search(r'^(.+?)\n', text)
    name = name_match.group(1).strip() if name_match else 'Unknown'
    type_match = re.search(r'(Champion|Spell|Item|Creature|Other)', text, re.IGNORECASE)
    card_type = type_match.group(1) if type_match else 'Unknown'
    mana_match = re.search(r'Cost:\s*(\d+)', text, re.IGNORECASE)
    mana_cost = int(mana_match.group(1)) if mana_match else None
    attack_match = re.search(r'Attack:\s*(\d+)', text, re.IGNORECASE)
    attack = int(attack_match.group(1)) if attack_match else None
    health_match = re.search(r'Health:\s*(\d+)', text, re.IGNORECASE)
    health = int(health_match.group(1)) if health_match else None
    ability_match = re.search(r'Ability:\s*(.+)', text, re.DOTALL | re.IGNORECASE)
    ability_text = ability_match.group(1).strip() if ability_match else ''
    rarity_match = re.search(r'(Common|Rare|Epic|Mythic|Legendary)', text, re.IGNORECASE)
    rarity = rarity_match.group(1) if rarity_match else 'Unknown'
    return RiftboundCard(name, card_type, mana_cost, attack, health, ability_text, rarity)

# Usage
image_path = "../riftdb/card_images/firestorm.avif"
try:
    preprocessed = minimal_preprocess(image_path)
    raw_text = extract_text(preprocessed)
    print("Raw OCR text:", raw_text)
    card_obj = parse_card(raw_text)
    print(f"Card stored: {card_obj.name} ({card_obj.card_type})")
except Exception as e:
    print(f"Error processing {image_path}: {e}")




