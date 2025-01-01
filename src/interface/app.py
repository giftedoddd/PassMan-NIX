import customtkinter as ctk
from tkinter import END

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.width, self.height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.img = imageprocessor.get_image()
        self.canvas, self.entry, self.search_button, self.create_button, self.username_entry, self.password_entry, self.generate_button \
            , self.hidden_err_frame, self.hidden_err_label, self.qr_scan_button = self.make_widgets()

    def maximize_window(self):
        self.geometry(f"{self.width}x{self.height}")
        self.attributes('-fullscreen', True)

    def make_widgets(self):
        canvas = ctk.CTkCanvas(master=self, width=self.width, height=self.height, highlightthickness=False)
        canvas.create_image(self.width / 2, self.height / 2, image=self.img)

        entry = ctk.CTkEntry(master=self, width=700, height=70, border_width=2, corner_radius=0, placeholder_text="Website:",
                             font=("System", 22, "normal"), justify="center", fg_color="#393E46")

        create_button = ctk.CTkButton(master=self, text="Create", font=("System", 20, "normal"), width=160, border_width=0,
                                      command=lambda func_name="create": self.event_handler(func_name))
        search_button = ctk.CTkButton(master=self, text="Search", font=("System", 20, "normal"), width=160, border_width=0,
                                      command=lambda func_name="search": self.event_handler(func_name))
        qr_scan_button  = ctk.CTkButton(master=self, text="QR Scan", font=("System", 20, "normal"), width=160, border_width=0,
                                        command=lambda func_name="qr_scan": self.event_handler(func_name))

        username_entry = ctk.CTkEntry(master=self, width=700, height=70, border_width=2, corner_radius=0, placeholder_text="Username:",
                                      font=("System", 22, "normal"), justify="center", fg_color="#393E46")
        password_entry = ctk.CTkEntry(master=self, width=700, height=70, border_width=2, corner_radius=0, placeholder_text="Password:",
                                      font=("System", 22, "normal"), justify="center", fg_color="#393E46")
        generate_button = ctk.CTkButton(master=self, text="Auto Generate", font=("System", 20, "normal"), width=150, height=32, border_width=0,
                                        command=lambda func_name="generate": self.event_handler(func_name))

        hidden_err_frame = ctk.CTkFrame(master=self, width=700, height=70, border_width=4, fg_color="transparent", bg_color="transparent", border_color="red")
        hidden_err_label = ctk.CTkLabel(master=hidden_err_frame, corner_radius=0, font=("System", 25, "normal"), text="", fg_color="#212121")

        canvas.grid()
        entry.place(relx=0.37, rely=0.45)
        search_button.place(relx=0.38, rely=0.50)
        create_button.place(relx=0.55, rely=0.50)
        username_entry.place(relx=0.37, rely=0.40)
        qr_scan_button.place(relx=0.465, rely=0.50)

        return (canvas, entry, search_button, create_button, username_entry, password_entry, generate_button, hidden_err_frame, hidden_err_label
                , qr_scan_button)

    def event_handler(self, func_name):
        def reset_widgets():
            self.entry.delete(0, END)
            self.username_entry.delete(0, END)
            self.password_entry.delete(0, END)
            self.password_entry.place_forget()
            self.generate_button.place_forget()
            self.hidden_err_frame.place_forget()
            self.hidden_err_label.place_forget()

        if func_name == "create" and self.entry.get():
            self.password_entry.place(relx=0.37, rely=0.35)
            self.generate_button.place(relx=0.62, rely=0.355)
            self.password_entry.configure(placeholder_text="Password:")
            if all([len(self.username_entry.get()), len(self.password_entry.get()), len(self.entry.get())]):
                pm.create_password(website=self.entry.get(), user=self.username_entry.get(), password=self.password_entry.get(), is_topt=False)
                reset_widgets()

        if func_name == "generate" and self.entry.get():
            password = pm.generate_random_password()
            self.password_entry.delete(0, END)
            self.password_entry.insert(0, password)

        if func_name == "search" and self.entry.get():
            self.password_entry.place_forget()
            self.username_entry.place(relx=0.37, rely=0.40)
            result, err_type = pm.search_password(website=self.entry.get(), user=self.username_entry.get())
            if not result:
                self.hidden_err_frame.place(relx=0.37, rely=0.40)
                self.hidden_err_label.place(relx=0.5, rely=0.5, anchor='center')
                self.hidden_err_label.configure(text=err_type)
                self.after(2000, reset_widgets)
                return
            self.hidden_err_frame.place(relx=0.37, rely=0.40)
            self.hidden_err_label.place(relx=0.5, rely=0.5, anchor='center')
            self.hidden_err_label.configure(text=err_type)
            self.after(2000, reset_widgets)

        if func_name == "qr_scan" and self.entry.get():
            data = QR_scanner.auto_detect()
            if not data:
                self.hidden_err_frame.place(relx=0.37, rely=0.40)
                self.hidden_err_label.place(relx=0.5, rely=0.5, anchor='center')
                self.hidden_err_label.configure(text="No QR Code Detected")
                self.after(2000, reset_widgets)
                return
            if not totp_processor.otp_match(data):
                self.hidden_err_frame.place(relx=0.37, rely=0.40)
                self.hidden_err_label.place(relx=0.5, rely=0.5, anchor='center')
                self.hidden_err_label.configure(text="Wrong QR Code")
                self.after(2000, reset_widgets)
                return

            secret = totp_processor.get_secret(data)
            pm.create_password(website=self.entry.get(), user=self.username_entry.get(), password=secret, is_topt=True)
            reset_widgets()
