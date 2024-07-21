import tkinter as tk
from PIL import Image, ImageTk

from View.retrieve_jira import RetrieveJiraPage
from View.training import TrainingPage
from View.processing import ProcessingPage  
from View.eccoladigital import EccolaDigitalCards 
from View.DownloadECCOLAQuestions import DownloadECCOLAQuestions


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automate Eccola")
        self.geometry("1200x630")
        self.configure(bg="#FFDD44")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.sidebar_frame = tk.Frame(self, bg="#FFF2E6", width=300)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.main_frame = tk.Frame(self, bg="#FFDD44")
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create sidebar content
        self.create_sidebar()

        # Create pages
        self.pages = {}
        self.create_pages()

        # Show Retrieve JIRA page by default
        self.show_page("Retrieve JIRA")

    def create_sidebar(self):
        # Load and resize the profile image
        profile_img = Image.open("Resources\profile.png")
        profile_img = profile_img.resize((50, 50), Image.LANCZOS)
        profile_photo = ImageTk.PhotoImage(profile_img)

        profile_label = tk.Label(self.sidebar_frame, image=profile_photo, bg="#FFF2E6")
        profile_label.image = profile_photo  # Keep a reference to avoid garbage collection
        profile_label.pack(pady=20)

        name_label = tk.Label(self.sidebar_frame, text="ECCOLA", font=("Helvetica", 18), bg="#FFF2E6")
        name_label.pack()

        role_label = tk.Label(self.sidebar_frame, text="Ethical IT Framework", font=("Helvetica", 14), fg="#FFA500", bg="#FFF2E6")
        role_label.pack()

        #DOWNLOAD JIRA USER STORIES
        self.retrieve_button = tk.Button(self.sidebar_frame, text="RETRIEVE JIRA", font=("Helvetica", 14),
                                         command=lambda: self.show_page("Retrieve JIRA"))
        self.retrieve_button.pack(pady=10)

        #DOWNLOAD ECCOLA QUESTIONS
        self.download_button = tk.Button(self.sidebar_frame, text="DOWNLOAD\nECCOLA QUESTIONS", font=("Helvetica", 14),
                                         command=self.download_eccola_questions)
        self.download_button.pack(pady=10)

        #TRAINING
        self.training_button = tk.Button(self.sidebar_frame, text="TRAINING", font=("Helvetica", 14),
                                         command=lambda: self.show_page("Training"))
        self.training_button.pack(pady=10)

        #PROCESS
        self.processing_button = tk.Button(self.sidebar_frame, text="PROCESSING", font=("Helvetica", 14),
                                           command=lambda: self.show_page("Processing"))
        self.processing_button.pack(pady=10)

        #ECCOLA CARD
        self.eccoladigital_button = tk.Button(self.sidebar_frame, text="ECCOLA DIGITAL CARDS", font=("Helvetica", 14),
                                           command=lambda: self.show_page("EccolaDigitalCards"))
        self.eccoladigital_button.pack(pady=10)

    def create_pages(self):
        self.pages["Retrieve JIRA"] = RetrieveJiraPage(self.main_frame)
        self.pages["Training"] = TrainingPage(self.main_frame)
        self.pages["Processing"] = ProcessingPage(self.main_frame)
        self.pages["EccolaDigitalCards"] = EccolaDigitalCards(self.main_frame)

    def show_page(self, page_name):
        for page in self.pages.values():
            page.pack_forget()
        self.pages[page_name].pack(fill=tk.BOTH, expand=True)

        self.update_sidebar(page_name)

    def update_sidebar(self, active_page):
        self.retrieve_button.config(bg="#FFF2E6")
        self.training_button.config(bg="#FFF2E6")
        self.processing_button.config(bg="#FFF2E6")
        self.eccoladigital_button.config(bg="#FFF2E6")

        if active_page == "Retrieve JIRA":
            self.retrieve_button.config(bg="#FFA500")
        elif active_page == "Training":
            self.training_button.config(bg="#FFA500")
        elif active_page == "Processing":
            self.processing_button.config(bg="#FFA500")
        elif active_page == "EccolaDigitalCards":
            self.eccoladigital_button.config(bg="#FFA500")

    def download_eccola_questions(self):
        download = DownloadECCOLAQuestions(self)
        download.download_questions_1()
        download.download_questions_2()

    def on_closing(self):
        self.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
