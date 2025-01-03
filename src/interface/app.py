import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self, image, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgets = []
        self.image = image
        self.width, self.height = self.winfo_screenwidth(), self.winfo_screenheight()

    def base_init(self):
        self.resizable(False, False)
        self.geometry(f"{self.width}x{self.height}")
        self.attributes('-fullscreen', True)

    def make_widgets(self):
        image_label = ctk.CTkLabel(master=self, width=self.width, height=self.height, image=self.image, text="")
        image_label.pack()

        website_entry = ctk.CTkEntry(master=self, width=700, height=70, border_width=2, corner_radius=0, placeholder_text="Website:",
                                     font=("System", 22, "normal"), justify="center", fg_color="#393E46")
        website_entry.place(relx=0.37, rely=0.40)

        create_button = ctk.CTkButton(master=self, text="Create", font=("System", 20, "normal"), width=160, border_width=0,
                                      height=45)
        create_button.place(relx=0.55, rely=0.51)

        search_button = ctk.CTkButton(master=self, text="Search", font=("System", 20, "normal"), width=160, border_width=0,
                                      height=45)
        search_button.place(relx=0.38, rely=0.51)

        qr_scan_button  = ctk.CTkButton(master=self, text="QR Scan", font=("System", 20, "normal"), width=160, border_width=0,
                                        height=45)
        qr_scan_button.place(relx=0.465, rely=0.51)

        password_entry = ctk.CTkEntry(master=self, width=700, height=70, border_width=2, corner_radius=0, placeholder_text="Password:",
                                      font=("System", 22, "normal"), justify="center", fg_color="#393E46")

        username_entry = ctk.CTkEntry(master=self, width=700, height=70, border_width=2, corner_radius=0, placeholder_text="Username:",
                                      font=("System", 22, "normal"), justify="center", fg_color="#393E46")
        username_entry.place(relx=0.37, rely=0.45)

        generate_button = ctk.CTkButton(master=self, text="Auto Generate", font=("System", 20, "normal"), width=150, height=32, border_width=0)

        hidden_err_frame = ctk.CTkFrame(master=self, width=700, height=70, border_width=4, fg_color="transparent", bg_color="transparent", border_color="red")
        hidden_err_label = ctk.CTkLabel(master=hidden_err_frame, corner_radius=0, font=("System", 25, "normal"), text="", fg_color="#212121")

        self.widgets.append(image_label)
