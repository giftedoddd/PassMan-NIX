from modules import image_processor
from interface.app import App

if __name__ == '__main__':
    image = image_processor.get_image()
    app = App(image=image)
    app.base_init()
    app.make_widgets()
    app.mainloop()
