from App import App
import customtkinter as ctk

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    app.center_window(900, 700)
    root.mainloop()