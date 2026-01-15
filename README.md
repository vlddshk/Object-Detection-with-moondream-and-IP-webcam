# Object Detection and Notification Bot with Moondream

This project implements an intelligent object detection system that monitors a video feed (Webcam or IP Camera) and sends real-time video alerts to Telegram when a specific object is detected. It leverages the **Moondream2** Vision-Language Model (VLM) for accurate visual understanding.

## Features

- **AI-Powered Detection**: Uses the `vikhyatk/moondream2` model to analyze frames and detect objects based on natural language queries (e.g., "Is there a bird in the image?").
- **Real-time Monitoring**: Continuously processes video frames from a webcam or IP camera.
- **Telegram Integration**: Instantly sends a text notification and a short video recording (approx. 4 seconds) to your Telegram chat upon detection.
- **Hardware Acceleration**: Automatically utilizes CUDA (GPU) if available for faster inference, with a CPU fallback option.
- **Asynchronous Design**: Built with `aiogram` and `asyncio` to handle bot operations and video processing concurrently.

## Prerequisites

- **Python**: 3.8 or higher.
- **Hardware**: A CUDA-capable GPU is highly recommended for real-time performance, though the script supports CPU execution.
- **Telegram Bot**: You need a Bot Token and your Chat ID.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/vlddshk/Object-Detection-with-moondream-and-IP-webcam
    cd Object-Detection-with-moondream-and-IP-webcam
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    pip install opencv-python
    ```
    *Note: `opencv-python` is required for video processing.*

## ⚙️ Configuration

Before running the bot, you must configure the sensitive information in `ObjectDetectionAndNotificationBot.py`:

1.  **Open the configuration file:**
    Open `main.py` in your code editor.

2.  **Set Telegram Credentials:**
    - Find the line `API_TOKEN = ('BOT-TOKEN')`. Replace `'BOT-TOKEN'` with your actual Telegram Bot Token.
    - Find the line `chat_id = ('ID')` inside `send_telegram_message` function. Replace `'ID'` with your numeric Telegram Chat ID (can be an integer or string).

3.  **Set Video Source:**
    - Find `cap = cv2.VideoCapture("")`.
    - For **Webcam**: Use `0` (e.g., `cap = cv2.VideoCapture(0)`).
    - For **IP Camera**: Enter the stream URL (e.g., `cap = cv2.VideoCapture("rtsp://admin:12345@192.168.1.10:554/stream")`).

4.  **Customize Detection (Optional):**
    - To change what the bot detects, modify the prompt in line 39:
      ```python
      response = model.answer_question(enc_image, "Is there a object in the image? (ONLY ANSWER WITH YES OR NO)", tokenizer)
      ```
      Replace `"object"` with `"bird"`, `"person"`, or any specific target you need.

## Usage

**Start the bot:**
```bash
python main.py
```

**Force CPU usage:**
If you encounter memory issues or want to force CPU execution:
```bash
python main.py --cpu
```

## License

This project is open-source. Please check the `LICENSE` file for more details.