import cv2
import os
import torch
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor

API_TOKEN = ('BOT-TOKEN') # Replace with your correct token

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Argument parser for CPU/GPU selection
parser = argparse.ArgumentParser()
parser.add_argument("--cpu", action="store_true")
args = parser.parse_args()

# Set device to CUDA if available and not overridden by --cpu flag
device = torch.device("cuda" if torch.cuda.is_available() and not args.cpu else "cpu")

if device.type == "cuda":
    logging.info(f"Using device: {torch.cuda.get_device_name(device)}")
else:
    logging.info("Using CPU")

# Load the Moondream model and tokenizer
model_id = "vikhyatk/moondream2"
revision = "2024-05-08"
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, revision=revision).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

#This function is used to determine if a your object is present in a frame of video.
def detect_bird(frame):
    """A function for determining the presence of a object in the frame"""
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    enc_image = model.encode_image(image)
    response = model.answer_question(enc_image, "Is there a object in the image? (ONLY ANSWER WITH YES OR NO)", tokenizer) #replace the object with what you want to detect
    return "yes" in response.lower()


#This function is an asynchronous function that sends a message and a video to a Telegram chat.
async def send_telegram_message(video_path):
    """A function for sending messages and videos in Telegram"""
    chat_id = ('ID')  # Replace with your correct chat_id
    try:
        await bot.send_message(chat_id, "A object has been detected on the webcam.")
        video = InputFile(video_path)
        await bot.send_video(chat_id, video)
    except Exception as e:
        logging.error(f"Failed to send message: {e}")

# Initialize webcam
cap = cv2.VideoCapture("")  # Replace with your URL or camera index(0 for camera)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')


#This is an asynchronous function that continuously reads frames from a webcam, 
#checks if an object is present in each frame using a pre-trained model, 
#and if so, captures a video of the object for 4 seconds and sends it as a Telegram message.
async def detect_and_notify():
    """Basic function for detecting objects and sending notifications"""
    while True:
        ret, frame = cap.read()
        if not ret:
            logging.error("Failed to read from webcam")
            break

        if detect_bird(frame):
            out = cv2.VideoWriter('detected_object.mp4', fourcc, 25.0, (frame.shape[1], frame.shape[0]))
            for _ in range(100):  # Capture 4 seconds of video at 25 fps
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
            out.release()
            await send_telegram_message('detected_object.mp4')
            os.remove('detected_object.mp4')

        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

async def on_startup(_):
    """The function that is performed when the bot is started"""
    asyncio.create_task(detect_and_notify())
    logging.info('Bot is online')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
