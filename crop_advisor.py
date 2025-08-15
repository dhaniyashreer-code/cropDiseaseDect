import cv2
import numpy as np
import requests
import pyttsx3
from PIL import Image, ImageDraw, ImageFont
import time

# Mock GPIO (for relay simulation)
class MockGPIO:
    BCM = 0
    OUT = 0
    def setmode(self, mode): print("Mock GPIO mode set")
    def setup(self, pin, mode): print(f"Mock GPIO pin {pin} setup")
    def output(self, pin, state): print(f"Mock GPIO pin {pin} set to {state}")

GPIO = MockGPIO()

# Mock OLED with PIL
def mock_oled_display(text_lines):
    img = Image.new('1', (128, 32))  # 1-bit image for OLED
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    for i, line in enumerate(text_lines):
        draw.text((0, i*10), line[:20], fill=255, font=font)
    img.show()  # Opens in default image viewer

# Initialize TTS
engine = pyttsx3.init()

# Capture image (use webcam or sample image)
use_webcam = False  # Set to True if you have a webcam
if use_webcam:
    cap = cv2.VideoCapture(0)
    ret, image = cap.read()
    cap.release()
else:
    image = cv2.imread('leaf.jpg')  # Use sample image

if image is None:
    print("Error: Failed to load image")
    exit()

# Disease Detection
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower_disease = np.array([20, 100, 100])  # Yellow/brown spots
upper_disease = np.array([30, 255, 255])
mask_disease = cv2.inRange(hsv, lower_disease, upper_disease)
diseased_area = cv2.countNonZero(mask_disease)
total_area = image.shape[0] * image.shape[1]
disease_percentage = (diseased_area / total_area) * 100 if total_area > 0 else 0

# Irrigation Detection
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
wilting_score = sum(1 for cnt in contours if cv2.contourArea(cnt) > 100 and cv2.arcLength(cnt, True) ** 2 / (4 * np.pi * cv2.contourArea(cnt)) > 1.5)

# LLM Advice (via Ollama)
prompt = f"Crop analysis: {disease_percentage:.2f}% diseased area, wilting score {wilting_score}. Suggest actions for tomato crop."
response = requests.post('http://localhost:11434/api/generate', 
                        json={'model': 'tinyllama', 'prompt': prompt, 'stream': False})
advice = response.json()['response'].strip()

# Output to mock OLED and TTS
mock_oled_display([f"Disease: {disease_percentage:.1f}%", f"Wilt: {wilting_score}", advice[:20]])
engine.say(advice[:50])
engine.runAndWait()
print(f"Advice: {advice}")

# Mock irrigation
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
if "irrigate" in advice.lower():
    GPIO.output(23, "HIGH")
    print("Irrigation triggered (mock)")
    time.sleep(2)
    GPIO.output(23, "LOW")

# Save image
cv2.imwrite('crop_analysis.jpg', image)