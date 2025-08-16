import cv2
import numpy as np
import requests
import pyttsx3
from PIL import Image, ImageDraw, ImageFont
import time
import json

# Mock GPIO (for relay simulation)
class MockGPIO:
    BCM = 0
    OUT = 0
    def setmode(self, mode): print("Mock GPIO mode set")
    def setup(self, pin, mode): print(f"Mock GPIO pin {pin} setup")
    def output(self, pin, state): print(f"Mock GPIO pin {pin} set to {state}")

GPIO = MockGPIO()

# Mock OLED with PIL (Enhanced for neat display)
def mock_oled_display(text_lines):
    img = Image.new('1', (128, 32), 0)  # Black background
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    line_height = 12
    for i, line in enumerate(text_lines[:3]):
        display_line = (str(line)[:20] + "...") if len(str(line)) > 20 else str(line)  # Smart truncation
        text_width = draw.textlength(display_line, font=font)
        x = max(0, (128 - text_width) // 2)
        draw.text((x, i * line_height + 2), display_line, fill=255, font=font)
        draw.text((x + 1, i * line_height + 2), display_line, fill=255, font=font)
    img.show()

# Initialize TTS
engine = pyttsx3.init()

# Capture image
use_webcam = False
if use_webcam:
    cap = cv2.VideoCapture(0)
    ret, image = cap.read()
    cap.release()
else:
    image = cv2.imread('leaf.jpg')

if image is None:
    print("Error: Failed to load image")
    exit()

# Advanced Disease Detection
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# Multi-threshold for diverse symptoms
lower_yellow = np.array([15, 50, 50])  # Yellow spots
upper_yellow = np.array([35, 255, 255])
lower_brown = np.array([5, 50, 50])   # Brown spots
upper_brown = np.array([15, 255, 255])
lower_white = np.array([0, 0, 200])   # Powdery Mildew
upper_white = np.array([180, 50, 255])
lower_wilt = np.array([0, 0, 100])    # Wilting
upper_wilt = np.array([180, 50, 255])
mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
mask_white = cv2.inRange(hsv, lower_white, upper_white)
mask_wilt = cv2.inRange(hsv, lower_wilt, upper_wilt)
mask_disease = cv2.bitwise_or(mask_yellow, mask_brown)
mask_disease = cv2.bitwise_or(mask_disease, mask_white)
mask_disease = cv2.bitwise_or(mask_disease, mask_wilt)
diseased_area = cv2.countNonZero(mask_disease)
total_area = image.shape[0] * image.shape[1]
disease_percentage = max(0.01, (diseased_area / total_area) * 100) if total_area > 0 else 0  # Minimum 0.01% to avoid false negatives

# Wilting and Texture Detection
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
wilting_score = sum(1 for cnt in contours if cv2.contourArea(cnt) > 100 and cv2.arcLength(cnt, True) ** 2 / (4 * np.pi * cv2.contourArea(cnt)) > 1.5)
# Spot circularity for pattern analysis
circularity = [4 * np.pi * cv2.contourArea(cnt) / (cv2.arcLength(cnt, True) ** 2) for cnt in contours if cv2.contourArea(cnt) > 50]
avg_circularity = np.mean(circularity) if circularity else 0

# Determine severity
severity = "Low" if disease_percentage <= 1 else "Medium" if disease_percentage <= 10 else "High"

# LLM Advice with refined prompt engineering
prompt = f"""
Step-by-step analysis of a leaf image (likely from India, August 2025) with the following data:
1. Diseased area: {disease_percentage:.2f}% (detected via yellow/brown/white spots or wilting).
2. Wilting score: {wilting_score} (indicating leaf droop or texture change).
3. Spot circularity: {avg_circularity:.2f} (average, where ~1 suggests round spots, <0.5 suggests irregular patterns).
4. Regional context: Monsoon season increases Leaf Spot, Early Blight, Downy Mildew, and Powdery Mildew prevalence.

Tasks:
- Identify the disease name by matching symptoms: 
  - Leaf Spot: Yellow/brown round spots, 0.1-0.5% common.
  - Early Blight: Dark brown spots with concentric rings, 1-5% typical.
  - Powdery Mildew: White powdery coating, 0.5-2% coverage.
  - Downy Mildew: Yellow spots with grayish mold, 1-3%.
  - Healthy: No significant symptoms (<0.1% or low wilting).
- Assign severity: {severity} based on 0-1% (Low), 1-10% (Medium), 10%+ (High).
- Recommend treatment: 1-2 sentences with specific fungicide (e.g., Mancozeb for Leaf Spot, Copper Oxychloride for Early Blight, Sulfur for Powdery Mildew, Metalaxyl for Downy Mildew) and application method.

Output only the JSON: {{ "disease_name": "name", "severity": "{severity}", "treatment": "action" }}. 
If unsure, use 'Unknown' and suggest expert consultation.
"""
try:
    response = requests.post('http://localhost:11434/api/generate', 
                            json={'model': 'tinyllama', 'prompt': prompt, 'stream': False, 'format': 'json'})
    raw_response = response.json()
    print(f"Raw LLM Response: {raw_response}")
    advice_json = raw_response.get('response', '{}').strip()
    advice = json.loads(advice_json)
except Exception as e:
    advice = {"disease_name": "Unknown", "severity": severity, "treatment": "Check plant and consult expert"}
    print(f"LLM Error: {e}")

# Extract from JSON
disease_name = str(advice.get("disease_name", "Unknown"))
treatment = str(advice.get("treatment", "Check plant and consult expert"))[:20]
print(f"Parsed - Disease: {disease_name}, Severity: {severity}, Treatment: {treatment}")

# Output to mock OLED and TTS
mock_oled_display([disease_name, f"Severity: {severity}", treatment])
engine.say(f"{disease_name}. {treatment}")
engine.runAndWait()
print(f"Advice Details: Disease: {disease_name}, Severity: {severity}, Treatment: {advice.get('treatment', 'Check plant and consult expert')}")

# Mock irrigation
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
if "irrigate" in str(advice.get("treatment", "")).lower():
    GPIO.output(23, "HIGH")
    print("Irrigation triggered (mock)")
    time.sleep(2)
    GPIO.output(23, "LOW")

# Save image
cv2.imwrite('crop_analysis.jpg', image)