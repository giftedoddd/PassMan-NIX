from src.modules.qr_scanner import auto_detect
import customtkinter as ctk
from src.modules import core
from src.modules import otp

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self, blur_image, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgets = {}
        self.blur_image = blur_image
        self.width, self.height = self.winfo_screenwidth(), self.winfo_screenheight()

    def base_init(self):
        self.resizable(False, False)
        # self.geometry(f"{self.width}x{self.height}")
        # self.attributes('-fullscreen', True)

    def make_widgets(self):
        image_label = ctk.CTkLabel(master=self, width=self.width, height=self.height, image=self.blur_image, text="")
        image_label.pack()
        self.widgets["image_label"] = image_label

        website_entry = ctk.CTkEntry(master=self, width=700, height=70, border_width=2, corner_radius=0, placeholder_text="Website:",
                                     font=("System", 22, "normal"), justify="center", fg_color="#393E46")
        website_entry.place(relx=0.37, rely=0.40)
        self.widgets["website_entry"] = website_entry

        create_button = ctk.CTkButton(master=self, text="Create", font=("System", 20, "normal"), width=160, border_width=0,
                                      height=45, command=lambda func_name="create_password": self.events(func_name))
        create_button.place(relx=0.55, rely=0.51)
        self.widgets["create_button"] = create_button

        search_button = ctk.CTkButton(master=self, text="Search", font=("System", 20, "normal"), width=160, border_width=0,
                                      height=45, command=lambda func_name="search_password": self.events(func_name))
        search_button.place(relx=0.38, rely=0.51)
        self.widgets["search_button"] = search_button

        qr_scan_button  = ctk.CTkButton(master=self, text="QR Scan", font=("System", 20, "normal"), width=160, border_width=0,
                                        height=45, command=lambda func_name="qr_scan": self.events(func_name))
        qr_scan_button.place(relx=0.465, rely=0.51)
        self.widgets["qr_scan_button"] = qr_scan_button

        password_entry = ctk.CTkEntry(master=self, width=700, height=70, border_width=2, corner_radius=0, placeholder_text="Password:",
                                      font=("System", 22, "normal"), justify="center", fg_color="#393E46")
        self.widgets["password_entry"] = password_entry

        username_entry = ctk.CTkEntry(master=self, width=700, height=70, border_width=2, corner_radius=0, placeholder_text="Username:",
                                      font=("System", 22, "normal"), justify="center", fg_color="#393E46")
        username_entry.place(relx=0.37, rely=0.45)
        self.widgets["username_entry"] = username_entry

        generate_button = ctk.CTkButton(master=self, text="Auto Generate", font=("System", 20, "normal"), width=150,
                                        height=32, border_width=0, command=lambda func_name="generate": self.events(func_name))
        self.widgets["generate_button"] = generate_button

        hidden_err_frame = ctk.CTkFrame(master=self, width=700, height=70, border_width=4, fg_color="transparent",
                                        bg_color="transparent", border_color="red")
        hidden_err_label = ctk.CTkLabel(master=hidden_err_frame, corner_radius=0, font=("System", 25, "normal"), text="",
                                        fg_color="#212121")
        hidden_err_label.place()
        self.widgets["hidden_err_frame"] = hidden_err_frame
        self.widgets["hidden_err_label"] = hidden_err_label

    def events(self, function_name):
        def reset_widgets():
            self.widgets["website_entry"].delete(0, ctk.END)
            self.widgets["username_entry"].delete(0, ctk.END)
            self.widgets["password_entry"].delete(0, ctk.END)
            self.widgets["password_entry"].place_forget()
            self.widgets["generate_button"].place_forget()
            self.widgets["hidden_err_frame"].place_forget()
            self.widgets["hidden_err_label"].place_forget()
        def create_password():
            condition = self.widgets["website_entry"].get() and self.widgets["username_entry"].get()
            if condition:
                self.widgets["password_entry"].place(relx=0.37, rely=0.35)
                self.widgets["generate_button"].place(relx=0.62, rely=0.355)
                self.widgets["password_entry"].configure(placeholder_text="Password:")
                if all([len(self.widgets["website_entry"].get()),
                        len(self.widgets["username_entry"].get()),
                        len(self.widgets["password_entry"].get())]):
                    core.create_password(
                        website=self.widgets["website_entry"].get(),
                        username=self.widgets["username_entry"].get(),
                        password=self.widgets["password_entry"].get(),
                        is_otp=False
                    )
                    reset_widgets()
        def search_password():
            result, err_type = core.search_password(
                website=self.widgets["website_entry"].get(),
                username=self.widgets["username_entry"].get()
            )
            if not result:
                self.widgets["hidden_err_frame"].place(relx=0.37, rely=0.40)
                self.widgets["hidden_err_label"].place(relx=0.5, rely=0.5, anchor='center')
                self.widgets["hidden_err_label"].configure(text=err_type)
                self.after(2000, reset_widgets)
                return
            self.widgets["hidden_err_frame"].place(relx=0.37, rely=0.40)
            self.widgets["hidden_err_label"].place(relx=0.5, rely=0.5, anchor='center')
            self.widgets["hidden_err_label"].configure(text=err_type)
            self.after(2000, reset_widgets)

        def qr_scan():
            data = auto_detect()
            if not data:
                self.widgets["hidden_err_frame"].place(relx=0.37, rely=0.40)
                self.widgets["hidden_err_label"].place(relx=0.5, rely=0.5, anchor='center')
                self.widgets["hidden_err_label"].configure(text="No QR Code detected!")
                self.after(2000, reset_widgets)
                return
            if not otp.otp_match(data):
                self.widgets["hidden_err_frame"].place(relx=0.37, rely=0.40)
                self.widgets["hidden_err_label"].place(relx=0.5, rely=0.5, anchor='center')
                self.widgets["hidden_err_label"].configure(text="Wrong QR Code")
                self.after(2000, reset_widgets)
                return

            secret = otp.get_secret(data)
            condition = self.widgets["website_entry"].get() and self.widgets["username_entry"].get()
            if condition:
                if all([len(self.widgets["website_entry"].get()),
                        len(self.widgets["username_entry"].get())
                        ]):
                    core.create_password(
                        website=self.widgets["website_entry"].get(),
                        username=self.widgets["username_entry"].get(),
                        password=secret,
                        is_otp=True
                    )

        def generate():
            password = core.generate_random_password()
            self.widgets["password_entry"].delete(0, ctk.END)
            self.widgets["password_entry"].insert(0, password)

        commands = {
            "create_password": create_password,
            "search_password": search_password,
            "qr_scan": qr_scan,
            "generate": generate
        }

        commands[function_name]()
