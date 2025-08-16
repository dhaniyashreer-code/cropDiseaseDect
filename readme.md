# Offline Crop Health and Irrigation Advisor

This is an offline Python application that analyzes leaf images to detect diseases, assess severity, and recommend treatments. It uses OpenCV for image processing, TinyLlama via Ollama for disease diagnosis, and simulates an OLED display and irrigation system.

## Prerequisites
- **Python 3.13** or later
- Required libraries: `opencv-python`, `numpy`, `requests`, `pyttsx3`, `pillow`
- Ollama server running locally (`ollama serve`) with TinyLlama model loaded
- A sample image file named `leaf.jpg` in the same directory

## Installation
1. Clone or download this repository.
2. Install Python dependencies:
   ```bash
   pip install opencv-python numpy requests pyttsx3 pillow

Start the Ollama server:
bash ollama serve
Load the TinyLlama model if not already loaded:
bash ollama pull tinyllama


Running the Script
From Source

Ensure leaf.jpg is in the project directory.
Run the script:
bash python crop_advisor.py

The app will analyze leaf.jpg, display results on a mock OLED, and use text-to-speech to announce the diagnosis.

