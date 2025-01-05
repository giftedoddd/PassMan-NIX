from PIL import ImageGrab, ImageFilter, Image
from customtkinter import CTkImage
from threading import Thread
import io

def get_image():
    screenshot = ImageGrab.grab()
    blured_image = screenshot.filter(ImageFilter.GaussianBlur(5))

    size = blured_image.size
    blur_image_bytes = blured_image.tobytes()

    save_image = Thread(target=keep_raw, args=(screenshot,), daemon=True)
    save_image.start()

    img = Image.frombytes(mode="RGB", size=size, data=blur_image_bytes)
    return CTkImage(img, size=size)

def keep_raw(raw_image):
    raw_image.save("/tmp/raw_image.png")
