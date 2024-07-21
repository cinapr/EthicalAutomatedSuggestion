import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import threading

# UDF
from Controller.suggestion_action import suggestion_action  # Ensure correct import

class ProcessingPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#FFDD44")
        self.temp_data = None  # Temporary storage for the uploaded data

        title_label = tk.Label(self, text="PROCESSING PAGE", font=("Helvetica", 18, "bold"), bg="#FFDD44")
        title_label.grid(row=0, column=0, columnspan=3, pady=20, padx=20, sticky="w")

        # Upload buttons
        self.upload_jira_button = tk.Button(self, text="UPLOAD DOWNLOADED JIRA USER STORIES", bg="#D8DCD5", fg="white", font=("Helvetica", 12), command=self.upload_user_stories)
        self.upload_jira_button.grid(row=1, column=0, pady=10, padx=10, sticky="w")

        # API Key label and entry
        api_key_label = tk.Label(self, text="GPT API Key", font=("Helvetica", 12), bg="#FFDD44")
        api_key_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")
        self.api_key_entry = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.api_key_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        # Model ID label and entry
        jira_model_id_label = tk.Label(self, text="Trained GPT MODEL ID", font=("Helvetica", 12), bg="#FFDD44")
        jira_model_id_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")
        self.jira_model_id_entry = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.jira_model_id_entry.grid(row=3, column=1, pady=10, padx=10, sticky="w")

        # Acknowledgement points label and text box
        ack_points_label = tk.Label(self, text="ACKNOWLEDGEMENT POINTS", font=("Helvetica", 14), bg="#FFDD44")
        ack_points_label.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky="w")
        
        self.ack_points_text = tk.Text(self, height=10, width=110)
        self.ack_points_text.grid(row=5, column=0, columnspan=3, rowspan=2, pady=10, padx=10, sticky="w")

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
        self.agree_check.grid(row=7, column=1, columnspan=2, pady=10, padx=10, sticky="w")

        # Process button
        self.process_button = tk.Button(self, text="PROCESS", bg="#FFA500", fg="white", font=("Helvetica", 14), command=self.start_process_thread)
        self.process_button.grid(row=7, column=2, pady=20, padx=10, sticky="e")

        # Log MessageBox
        self.callback_log_text = tk.Text(self, height=5, width=110)
        self.callback_log_text.grid(row=8, column=0, columnspan=3, rowspan=2, pady=10, padx=10, sticky="w")

    def upload_user_stories(self):
        self.UserStories_csv = filedialog.askopenfilename(title="Select UserStories CSV", filetypes=[("CSV Files", "*.csv")])
        if self.UserStories_csv:
            try:
                self.temp_data = pd.read_csv(self.UserStories_csv)
                self.upload_jira_button.config(bg="#00FF00")
                self.log_message(f"Uploaded file: {self.UserStories_csv}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load the file: {str(e)}")

    def start_process_thread(self):
        # Disable UI elements
        self.toggle_ui_elements(state='disable')

        # Start the processing in a new thread
        thread = threading.Thread(target=self.start_process)
        thread.start()

    def start_process(self):
        if not self.agree_var.get():
            messagebox.showerror("Error", "You must agree to the risks.")
            self.toggle_ui_elements(state='normal')
            return

        if self.temp_data is None:
            messagebox.showerror("Error", "You must upload the JIRA user stories first.")
            self.toggle_ui_elements(state='normal')
            return

        api_key = self.api_key_entry.get()
        model_id = self.jira_model_id_entry.get()
        if not api_key or not model_id:
            messagebox.showerror("Error", "API Key and Trained GPT Model ID must be provided.")
            self.toggle_ui_elements(state='normal')
            return

        self.process_user_stories(api_key, model_id)
        self.toggle_ui_elements(state='normal')

    def process_user_stories(self, api_key, model_id):
        sa = suggestion_action(api_key, model_id)
        total_rows = len(self.temp_data)

        # Fill NaN values with empty strings
        self.temp_data['User_Story'] = self.temp_data['User_Story'].fillna('')
        self.temp_data['Comments'] = self.temp_data['Comments'].fillna('')
        
        # Add a column to mark rows to be deleted
        self.temp_data['Delete_Row'] = False

        for index, row in self.temp_data.iterrows():
            user_story = row['User_Story']
            comments = row['Comments']

            if not user_story and not comments:
                story = 'NO_CONTENT'
                self.temp_data.at[index, 'ECCOLA_Code'] = story  # Update the ECCOLA_Code cell with the response
                self.temp_data.at[index, 'Delete_Row'] = True  # Mark this row for deletion
                self.log_message(f"Processed row {index + 1}/{total_rows}: {story}")
                continue  # Skip the rest of the loop and move to the next iteration
            elif user_story and comments:
                story = user_story + '\n' + comments
            elif not user_story and comments:
                story = comments
            elif user_story and not comments:
                story = user_story

            response = sa.classify_ECCOLA(story)
            self.temp_data.at[index, 'ECCOLA_Code'] = response  # Update the ECCOLA_Code cell with the response
            self.log_message(f"Processed row {index + 1}/{total_rows}: {response}")

        # Remove the marked rows
        self.temp_data = self.temp_data[self.temp_data['Delete_Row'] == False]
        
        # Drop the 'Delete_Row' column as it's no longer needed
        self.temp_data = self.temp_data.drop(columns=['Delete_Row'])

        # Save the updated DataFrame back to a CSV file
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save updated UserStories CSV")
        if save_path:
            self.temp_data.to_csv(save_path, index=False)
            self.log_message(f"Updated file saved: {save_path}")



    def toggle_ui_elements(self, state):
        self.upload_jira_button.config(state=state)
        self.api_key_entry.config(state=state)
        self.jira_model_id_entry.config(state=state)
        self.agree_check.config(state=state)
        self.process_button.config(state=state)

    def log_message(self, message):
        self.callback_log_text.insert(tk.END, message + "\n")
        self.callback_log_text.see(tk.END)