# AI Shorts Generator

## Description
This project generates short motivational or inspirational videos using AI-generated text, background music, and images fetched from external APIs (e.g., Pixabay or Picsum). The project uses `gTTS` for text-to-speech conversion, `moviepy` for video creation, and integrates with **Gemini** for AI-powered text generation.

### Features:
- Fetches random images or videos from external APIs (Pixabay or Picsum).
- Converts text into speech using `gTTS`.
- Combines images, text, and audio to create a video.
- Allows for text wrapping and dynamic video creation.
- Configurable background music overlay and voice track addition.
- Generates a JSON file with video metadata for easy sharing or further processing.

---

## Requirements

- **Python version**: 3.13 or higher.
- **Dependencies**: Listed in the `requirements.txt` file.

---

## Setup

### 1. **Clone the repository**

Clone the repository to your local machine:

```bash
git clone https://github.com/NitishNaskar/AI-Shorts-Generator.git
cd AI-Shorts-Generator
```

### 2. **Create a virtual environment (recommended)**

It’s a good practice to use a virtual environment for Python projects to manage dependencies. You can create a virtual environment with the following command:

```bash
python3.13 -m venv venv
```

Activate the virtual environment:

- **On macOS/Linux**:
    ```bash
    source venv/bin/activate
    ```
- **On Windows**:
    ```bash
    .\venv\Scripts\activate
    ```

### 3. **Install dependencies**

Once the virtual environment is activated, you can install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### 4. **Environment Variables**

You need to configure the environment variables for API keys. Create a `.env` file in the root directory of the project and add the following:

```dotenv
IMAGE_API_KEY=your_pixabay_api_key
GOOGLE_API_KEY=your_google_api_key
```

- Replace `your_pixabay_api_key` with your actual [Pixabay API key](https://pixabay.com/api/docs/).
- Replace `your_google_api_key` with your actual **Google Gemini API key**.

### 5. **FFmpeg Installation**

For video processing, you need **FFmpeg** installed on your system. Follow the installation instructions below:

- [FFmpeg Download](https://ffmpeg.org/download.html)
- Once downloaded, make sure FFmpeg is added to your system’s **PATH** environment variable.

---

## Usage

### 1. **Run the Script**

You can run the script directly to generate the video:

```bash
python ved.py
```

This will create a video based on randomly fetched images from the image API, with text-to-speech narration and background music.

### 2. **Customizing the Video Content**

You can modify the following settings in the script to customize the video:

- **Category Zone (default)**: 
    The category for generating quotes is randomly chosen from the list:

    ```python
    quote = random.choice(["motivational", "inspirational", "positivevibes kind of", "mindset thing", "growthmindset thing", "selfloveness", "innerstrength thing", "resilience", "nevergiveup", "believeinyourself", "keepgoing", "success", "journey", "lifequotes", "dailymotivation", "inspirationdaily", "quoteoftheday", "motivationmonday", "wisdom"])
    ```

    These values are categories of motivational and inspirational themes. You can modify this list if you want to add more categories.

- **Language**:
    The script dynamically selects between Hindi or English for the narration. You can modify this section to change the language based on your needs:
    
    ```python
    if language == 1:
        language = 'Hindi'
        font = "Kalam-Regular.ttf"
    else:
        language = "English"
        font = "Roboto-Regular.ttf"
    ```

- **Text-to-Speech**:
    The text-to-speech conversion is handled by the `gTTS` library. You can adjust the text or let the AI generate it for you.

- **Background Music**:
    The script will randomly pick background music from the `music/` directory. You can add your own MP3 or WAV files to this directory.

### 3. **Output Files**

- **Generated Video**: The final video is saved in the working directory as `final_video.mp4`.
- **Audio File**: The text-to-speech and background music are saved in `temp/` as `story.mp3` and `final_audio.mp3`, respectively.
- **Video Metadata**: The metadata is saved in a JSON file (`video-meta.json`).

---

## File Structure

```
AI-Shorts-Generator/
│
├── music/                  # Background music files
├── temp/                   # Temporary files (images, audio, etc.)
│   ├── story.mp3           # Text-to-speech audio
│   └── final_audio.mp3     # Final audio (with background music)
├── font/                   # Fonts (e.g., Roboto-Regular.ttf)
├── ved.py                  # Main Python script to generate video
├── .env                    # Environment variables (IMAGE_API_KEY, GOOGLE_API_KEY)
├── requirements.txt        # Python dependencies
└── video-meta.json         # Video metadata (JSON file)
```

---

## Dependencies

The following libraries are required for this project:

- `gtts`: For text-to-speech conversion.
- `moviepy`: For video creation and manipulation.
- `requests`: For making HTTP requests to external APIs.
- `pydub`: For audio file manipulation (e.g., merging background music).
- `pyGPT`: For generating text via Gemini (Google's AI).
- `textwrap`: For text wrapping functionality.
- `json`: For saving video metadata.
- `python-dotenv`: For loading environment variables.

You can install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## Troubleshooting

1. **FFmpeg Not Found**: If you encounter issues with FFmpeg not being found, ensure that it’s correctly installed and that its path is added to your system's environment variables.

2. **API Key Issues**: If you encounter issues with fetching images from the API or using Gemini, double-check that you’ve added your **Pixabay API Key** and **Google API Key** in the `.env` file.

3. **Audio/Video Issues**: If you experience issues with audio or video not playing correctly, check that the correct audio and video files are being generated in the `temp/` directory. Also, ensure that the required Python libraries (`moviepy`, `pydub`, etc.) are installed.

---

## Contributing

Feel free to fork this repository and submit pull requests if you have improvements or fixes. Contributions are always welcome!

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---