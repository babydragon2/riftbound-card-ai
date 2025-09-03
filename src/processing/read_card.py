import cv2
import pytesseract


def minimal_preprocess(image_path):
    img = cv2.imread(image_path)  # Works for .avif if OpenCV supports it
    if img is None:
        raise ValueError(f"Failed to load {image_path}. Check OpenCV/libavif support.")

    img = cv2.resize(img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    gray = cv2.medianBlur(gray, 3)
    return gray


def get_rois(img):
    height, width = img.shape[:2]
    rois = {
        'mana_cost': img[int(height*0.05):int(height*0.125), int(height*0.075):int(width*0.20)],  # Top-left for "6"
        'card_type': img[int(height*0.35):int(height*0.45), 0:int(width*0.15)],  # Mid-left for "SPELL"
        'set_code': img[int(height*0.90):height, 0:int(width*0.30)],  # Bottom-left for "OGS - 002/024"
        'text_box': img[int(height*0.45):int(height*0.85), int(width*0.15):int(width*0.85)]  # Main text
    }
    
    return rois

def extract_text(image):
    
    rois = get_rois(image)
    mana_text = pytesseract.image_to_string(rois['mana_cost'], config='--psm 8 --oem 3')  # PSM 8 for single word/number
    type_text = pytesseract.image_to_string(rois['card_type'], config='--psm 8 --oem 3')
    set_text = pytesseract.image_to_string(rois['set_code'], config='--psm 7 --oem 3')  # PSM 7 for single line
    main_text = pytesseract.image_to_string(rois['text_box'], config='--psm 6 --oem 3')  # PSM 6 for block  

    print("Mana Text: ", mana_text)
    print("Type Text: ", type_text)
    print("Set Text: ", set_text)
    print("Main Text: ", main_text)


# Usage
image_path = "../riftbound-card-ai/riftbound_card_images/OGS_002.jpg"
try:
    preprocessed = minimal_preprocess(image_path)
    extract_text(preprocessed)
except Exception as e:
    print(f"Error processing {image_path}: {e}")




