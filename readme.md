# Offline Crop Health and Irrigation Advisor

## Project Description
The **Offline Crop Health and Irrigation Advisor** is an innovative tool designed to help farmers and gardeners monitor the health of their plants offline. This application analyzes leaf images to detect common diseases (e.g., Leaf Spot, Early Blight, Powdery Mildew, Downy Mildew), assesses their severity, and provides tailored treatment recommendations, including specific fungicides and irrigation advice. Built with Python, it leverages OpenCV for image processing, TinyLlama (via Ollama) for disease diagnosis, and simulates an OLED display and irrigation system for a hands-on experience. Ideal for use in areas with limited internet access, this tool is particularly useful during the monsoon season in India (e.g., August 2025), where fungal diseases are prevalent. The project includes a standalone executable (`crop_advisor.exe`) for Windows users, making it accessible without requiring technical setup.

## Features
- Detects diseases like Leaf Spot, Early Blight, Powdery Mildew, and Downy Mildew based on leaf image analysis.
- Assesses disease severity (Low, Medium, High) and suggests specific treatments (e.g., Mancozeb, Copper Oxychloride).
- Simulates an OLED display for visual feedback and uses text-to-speech for audio guidance.
- Includes mock irrigation control based on treatment needs.
- Works offline with a pre-trained TinyLlama model via a local Ollama server.

## Prerequisites
- **Windows Operating System** (tested on Windows 10/11).
- A leaf image file named `leaf.jpg` (place it in the same folder as the executable).
- No Python installation required for the executable version.

## Installation and Usage
### Downloading the Executable
1. Visit the [GitHub repository](https://github.com/dhaniyashreer-code/cropDiseaseDect).
2. Download the `crop_advisor.exe` file from the `dist` folder or the latest release section.
3. Save `crop_advisor.exe` to a folder on your computer (e.g., `C:\CropAdvisor`).

### Preparing to Run
1. Obtain a clear leaf image (e.g., a photo of a tomato or other plant leaf).
2. Rename the image to `leaf.jpg` and place it in the same folder as `crop_advisor.exe`.

### Running the Executable
1. Double-click `crop_advisor.exe` to launch the application.
2. The app will:
   - Analyze `leaf.jpg` for disease symptoms (yellow/brown spots, wilting, powdery coating).
   - Display the results on a simulated 128x32 OLED screen (opens as an image window).
   - Announce the diagnosis and treatment via text-to-speech.
   - Simulate irrigation if recommended in the treatment.
3. A file named `crop_analysis.jpg` will be saved in the same folder, showing the analyzed image.

### Example Output
- **Display (OLED Simulation)**:
  - Line 1: "Leaf Spot"
  - Line 2: "Severity: Medium"
  - Line 3: "Apply Mancozeb..."
- **Text-to-Speech**: "Leaf Spot. Apply Mancozeb spray every 10 days."
- **Console (if visible)**: "Parsed - Disease: Leaf Spot, Severity: Medium, Treatment: Apply Mancozeb..."

### Troubleshooting
- **Image Not Loading**: Ensure `leaf.jpg` is in the correct folder and is a valid image file.
- **No Sound**: Check your system’s audio settings; text-to-speech requires speakers or headphones.
- **Error on Launch**: Re-download `crop_advisor.exe` or report the issue on the GitHub page.
- **Large File Warning**: The `.exe` is large due to included dependencies; ensure sufficient disk space.

## Building from Source (Optional)
For developers who prefer to build the executable themselves:
1. Install Python 3.13 and dependencies:
   ```bash
   pip install opencv-python numpy requests pyttsx3 pillow pyinstaller

Clone the repository:
bashgit clone https://github.com/dhaniyashreer-code/cropDiseaseDect.git
cd cropDiseaseDect

Set up Ollama (required for TinyLlama):

Install Ollama from https://ollama.com/.
Run ollama serve and load the TinyLlama model with ollama pull tinyllama.


Build the executable:
bashpyinstaller --onefile crop_advisor.py

Find crop_advisor.exe in the dist folder and follow the usage steps above.

Contributing

Report bugs or suggest features by opening an issue on GitHub.
Fork the repository, make changes, and submit a pull request.
 