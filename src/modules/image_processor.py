from PIL import ImageGrab, ImageFilter, ImageTk, Image
from customtkinter import CTkImage

def get_image():
    screenshot = ImageGrab.grab()
    blured_image = screenshot.filter(ImageFilter.GaussianBlur(5))

    size = blured_image.size
    raw_image_bytes = screenshot.tobytes()
    blur_image_bytes = blured_image.tobytes()

    img = Image.frombytes(mode="RGB", size=size, data=blur_image_bytes)
    return CTkImage(img, size=size)
