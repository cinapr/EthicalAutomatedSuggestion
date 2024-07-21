import tkinter as tk
from tkinter import filedialog, messagebox
from Model.ECCOLA import ECCOLA
import os
import threading

# UDF
from Controller.training_action import training_action

class TrainingPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#FFDD44")
        self.parent = parent
        self.ECCOLA_Questions_csv = None
        self.ECCOLA_QuestionsCorrelations_csv = None
        self.trainingDataSetCSV = None
        
        # Title label
        title_label = tk.Label(self, text="TRAINING PAGE", font=("Helvetica", 18, "bold"), bg="#FFDD44")
        title_label.grid(row=0, column=0, columnspan=3, pady=20, padx=20, sticky="w")

        # Upload buttons
        self.upload_questions_button = tk.Button(self, text="UPLOAD ECCOLA QUESTIONS", bg="#D8DCD5", fg="white", font=("Helvetica", 12), command=self.upload_questions)
        self.upload_questions_button.grid(row=1, column=0, pady=10, padx=10, sticky="w")

        self.upload_definition_button = tk.Button(self, text="UPLOAD ECCOLA DEFINITION", bg="#D8DCD5", fg="white", font=("Helvetica", 12), command=self.upload_definition)
        self.upload_definition_button.grid(row=1, column=1, pady=10, padx=10, sticky="w")

        self.upload_samples_button = tk.Button(self, text="UPLOAD TRAINING SAMPLES", bg="#D8DCD5", fg="white", font=("Helvetica", 12), command=self.upload_samples)
        self.upload_samples_button.grid(row=1, column=2, pady=10, padx=10, sticky="w")

        # API Key label and entry
        api_key_label = tk.Label(self, text="GPT API Key", font=("Helvetica", 12), bg="#FFDD44")
        api_key_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        self.api_key_entry = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.api_key_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        # Acknowledgement points label and text box
        ack_points_label = tk.Label(self, text="ACKNOWLEDGEMENT POINTS", font=("Helvetica", 14), bg="#FFDD44")
        ack_points_label.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="w")

        self.ack_points_text = tk.Text(self, height=10, width=110)
        self.ack_points_text.grid(row=4, column=0, columnspan=3, rowspan=2, pady=10, padx=10, sticky="w")

        acknowledgement_content = """
        Acknowledgement Points

        1. Data Retrieval:
        - The code retrieves user stories from JIRA using the provided API credentials.
        - These user stories are stored locally in a CSV file for further processing.

        2. Data Processing:
        - The uploaded JIRA user stories are cleaned and prepared for training and classification.
        - The ECCOLA Questions and Definitions are uploaded and used to form the training dataset.

        3. Model Training:
        - The training process uses the ECCOLA Questions and Definitions to fine-tune the GPT-3.5 model.
        - This involves uploading the prepared dataset to the GPT-3.5 API and initiating the fine-tuning process.
        - The model is trained to classify user stories based on the provided ethical considerations.

        4. Classification and Suggestion:
        - Once trained, the model can classify new user stories and provide ethical recommendations.
        - The code processes each user story, combining the story and comments to form a complete input.
        - The GPT-3.5 API is used to classify the input and provide relevant ECCOLA codes and ethical questions.

        5. Data Ownership:
        - All data processed and stored by the code, including JIRA user stories and training datasets, are owned by the client.
        - Data is stored and processed locally, ensuring confidentiality and control over sensitive information.
        - The only external service used is the GPT-3.5 API, which handles the actual language model processing.

        By understanding these points, you acknowledge the steps taken by the code to ensure ethical assessment and the secure handling of data.
        """

        self.ack_points_text.insert(tk.END, acknowledgement_content)
        self.ack_points_text.config(state=tk.DISABLED)  # To make the text box read-only

        
        # Agreement checkbox
        self.agree_var = tk.IntVar()
        self.agree_check = tk.Checkbutton(self, text="I have read and understand the risks", variable=self.agree_var, bg="#FFDD44")
        self.agree_check.grid(row=6, column=0, columnspan=2, pady=10, padx=10, sticky="w")

        # Training button
        self.training_button = tk.Button(self, text="TRAINING", bg="#FFA500", fg="white", font=("Helvetica", 14), command=self.start_training)
        self.training_button.grid(row=7, column=0, pady=20, padx=10, sticky="e")

        # Log MessageBox
        self.callback_log_text = tk.Text(self, height=5, width=110)
        self.callback_log_text.grid(row=8, column=0, columnspan=3, rowspan=2, pady=10, padx=10, sticky="w")

    def upload_questions(self):
        self.ECCOLA_Questions_csv = filedialog.askopenfilename(title="Select ECCOLA Questions CSV", filetypes=[("CSV Files", "*.csv")])
        if self.ECCOLA_Questions_csv:
            self.upload_questions_button.config(bg="#00FF00")

    def upload_definition(self):
        self.ECCOLA_QuestionsCorrelations_csv = filedialog.askopenfilename(title="Select ECCOLA Definition CSV", filetypes=[("CSV Files", "*.csv")])
        if self.ECCOLA_QuestionsCorrelations_csv:
            self.upload_definition_button.config(bg="#00FF00")

    def upload_samples(self):
        self.trainingDataSetCSV = filedialog.askopenfilename(title="Select Training Samples CSV", filetypes=[("CSV Files", "*.csv")])
        if self.trainingDataSetCSV:
            self.upload_samples_button.config(bg="#00FF00")

    def start_training(self):
        if self.agree_var.get() == 0:
            messagebox.showerror("Error", "You must agree to the risks before starting the training.")
            return

        if not all([self.ECCOLA_Questions_csv, self.ECCOLA_QuestionsCorrelations_csv, self.trainingDataSetCSV]):
            messagebox.showerror("Error", "All CSV files must be uploaded before starting the training.")
            return

        self.GPT_API_Key = self.api_key_entry.get()
        self.training_action = training_action(self.GPT_API_Key)

        # Disable all form elements
        self.disable_all_elements()

        # Start the training in a new thread
        training_thread = threading.Thread(target=self.run_training)
        training_thread.start()

    def run_training(self):
        success, message = self.training_action.run_ECCOLA_training(
            self.ECCOLA_Questions_csv, 
            self.ECCOLA_QuestionsCorrelations_csv, 
            self.trainingDataSetCSV,
            log_callback=self.log_message
        )

        if success:
            self.show_messagebox("Success", message)
        else:
            self.show_messagebox("Error", message)

        # Re-enable all form elements after training completes
        self.enable_all_elements()

    #UPLOAD BUTTON FUNCTIONS
    def upload_questions(self):
        self.ECCOLA_Questions_csv = filedialog.askopenfilename(title="Select ECCOLA Questions CSV", filetypes=[("CSV Files", "*.csv")])
        if self.ECCOLA_Questions_csv:
            self.upload_questions_button.config(bg="#00FF00")

    def upload_definition(self):
        self.ECCOLA_QuestionsCorrelations_csv = filedialog.askopenfilename(title="Select ECCOLA Definition CSV", filetypes=[("CSV Files", "*.csv")])
        if self.ECCOLA_QuestionsCorrelations_csv:
            self.upload_definition_button.config(bg="#00FF00")

    def upload_samples(self):
        self.trainingDataSetCSV = filedialog.askopenfilename(title="Select Training Samples CSV", filetypes=[("CSV Files", "*.csv")])
        if self.trainingDataSetCSV:
            self.upload_samples_button.config(bg="#00FF00")


    #GUI FUNCTIONS
    def show_messagebox(self, title, message):
        # Tkinter requires this method to be called from the main thread
        self.after(0, lambda: messagebox.showinfo(title, message))

    def log_message(self, message):
        self.callback_log_text.insert(tk.END, message + "\n")
        self.callback_log_text.see(tk.END)
        self.callback_log_text.update_idletasks()

    def disable_all_elements(self):
        self.upload_questions_button.config(state=tk.DISABLED)
        self.upload_definition_button.config(state=tk.DISABLED)
        self.upload_samples_button.config(state=tk.DISABLED)
        self.training_button.config(state=tk.DISABLED)
        self.api_key_entry.config(state=tk.DISABLED)
        self.agree_check.config(state=tk.DISABLED)
        #self.parent.protocol("WM_DELETE_WINDOW", self.disable_close)

    def enable_all_elements(self):
        self.upload_questions_button.config(state=tk.NORMAL)
        self.upload_definition_button.config(state=tk.NORMAL)
        self.upload_samples_button.config(state=tk.NORMAL)
        self.training_button.config(state=tk.NORMAL)
        self.api_key_entry.config(state=tk.NORMAL)
        self.agree_check.config(state=tk.NORMAL)
        #self.parent.protocol("WM_DELETE_WINDOW", self.parent.destroy)

    def disable_close(self):
        pass
