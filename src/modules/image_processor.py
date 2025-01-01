from PIL import ImageGrab, ImageFilter, ImageTk, Image

TMP_PATH = "/tmp"

def process_image():
    screenshot = ImageGrab.grab()
    screenshot.load()
    blur_image = screenshot.filter(ImageFilter.GaussianBlur(5))
    screenshot.save(TMP_PATH + "/raw_ss.png")
    blur_image.save(TMP_PATH + "/temp_ss.png")

def get_image():
    img = Image.open(TMP_PATH + "/temp_ss.png")
    return ImageTk.PhotoImage(img)
