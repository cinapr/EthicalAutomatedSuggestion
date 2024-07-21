import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import threading

# UDF
from Controller.eccoladigital_action import eccoladigital_action  
from Resources.clean_text import clean_text

class EccolaDigitalCards(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#FFDD44")
        self.parent = parent
        self.current_index = 0
        self.eccola_type_list = []

        title_label = tk.Label(self, text="RUN ECCOLA DIGITAL CARDS", font=("Helvetica", 18, "bold"), bg="#FFDD44")
        title_label.grid(row=0, column=0, columnspan=4, pady=20, padx=20, sticky="w")

        # Upload buttons QUESTION
        self.upload_questions_button = tk.Button(self, text="UPLOAD ECCOLA QUESTIONS", bg="#D8DCD5", fg="white", font=("Helvetica", 12), command=self.upload_eccola_questions)
        self.upload_questions_button.grid(row=1, column=0, pady=10, padx=10, sticky="w")

        # Upload buttons JIRA
        self.upload_jira_button = tk.Button(self, text="UPLOAD PROCESSED JIRA USER STORIES", bg="#D8DCD5", fg="white", font=("Helvetica", 12), command=self.upload_user_stories)
        self.upload_jira_button.grid(row=1, column=1, pady=10, padx=10, sticky="w")

        # Run ECCOLA button
        self.run_eccola_button = tk.Button(self, text="RUN CARD", bg="#D8DCD5", fg="white", font=("Helvetica", 12), command=self.run_digitalcard_thread)
        self.run_eccola_button.grid(row=1, column=2, pady=10, padx=10, sticky="w")

        # Next Question button
        self.next_question_button = tk.Button(self, text="NEXT QUESTION", bg="#D8DCD5", fg="white", font=("Helvetica", 12), command=self.show_next_question)
        self.next_question_button.grid(row=1, column=3, pady=10, padx=10, sticky="w")
        self.next_question_button.config(state=tk.DISABLED)

        # ECCOLA Cards Title
        eccolacards_label = tk.Label(self, text="ECCOLA Cards : ", font=("Helvetica", 14), bg="#FFDD44")
        eccolacards_label.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="w")
        self.eccolacardsnumber_label = tk.Label(self, text="", font=("Helvetica", 14), bg="#FFDD44")
        self.eccolacardsnumber_label.grid(row=2, column=3, columnspan=2, pady=10, padx=10, sticky="w")

        # ECCOLA Cards with Scrollbar
        self.text_frame = tk.Frame(self, bg="#FFDD44")
        self.text_frame.grid(row=3, column=0, columnspan=5, rowspan=4, pady=10, padx=10, sticky="nsew")

        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.eccolacards_text = tk.Text(self.text_frame, height=25, width=110, yscrollcommand=self.scrollbar.set)
        self.eccolacards_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.eccolacards_text.yview)

        self.eccolacards_text.config(state=tk.DISABLED)

    def upload_eccola_questions(self):
        self.ECCOLA_Questions_csv = filedialog.askopenfilename(title="Select ECCOLA Questions CSV", filetypes=[("CSV Files", "*.csv")])
        if self.ECCOLA_Questions_csv:
            try:
                # Block the button
                self.upload_questions_button.config(bg="#00FF00")

                # Load ECCOLA Questions CSV
                self.eccolaQuestions_data = pd.read_csv(self.ECCOLA_Questions_csv)

                # Apply cleaning to ECCOLA_Code before extracting distinct values
                self.eccolaQuestions_data['ECCOLA_Code'] = self.eccolaQuestions_data['ECCOLA_Code'].apply(clean_text.clean_text)

                # Sort the dataframe based on ECCOLA_Code
                self.eccolaQuestions_data = self.eccolaQuestions_data.sort_values(by='ECCOLA_Code')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load the file: {str(e)}")

    def upload_user_stories(self):
        self.UserStories_csv = filedialog.askopenfilename(title="Select UserStories CSV", filetypes=[("CSV Files", "*.csv")])
        if self.UserStories_csv:
            try:
                # Block the button
                self.upload_jira_button.config(bg="#00FF00")

                # Load User Stories CSV
                self.userStories_data = pd.read_csv(self.UserStories_csv)
                
                # Apply cleaning to ECCOLA_Code before extracting distinct values
                self.userStories_data['ECCOLA_Code'] = self.userStories_data['ECCOLA_Code'].apply(clean_text.clean_text)

                # Sort the dataframe based on ECCOLA_Code
                self.userStories_data = self.userStories_data.sort_values(by='ECCOLA_Code')

                # Extract distinct values of cleaned ECCOLA_Code and store in self.eccolatype_list dictionary
                self.eccolatype_list = {'ECCOLA_Code': self.userStories_data['ECCOLA_Code'].unique().tolist()}
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load the file: {str(e)}")

    def run_digitalcard_thread(self):
        self.thread = threading.Thread(target=self.run_digitalcard)
        self.thread.start()

    def run_digitalcard(self):
        try:
            messagebox.showinfo("Notifications", f"You might skip irrelevant questions.")
            self.disable_all_elements()

            # Clear existing content
            self.clear_text()

            # Initialize the ECCOLA code list and index
            self.eccola_type_list = self.eccolatype_list['ECCOLA_Code']
            self.current_index = 0

            # Enable the Next Question button
            self.next_question_button.config(state=tk.NORMAL)

            # Show the first question
            self.show_next_question()
        except Exception as e:
            self.enable_all_elements()
            messagebox.showerror("Error", f"Failed to process: {str(e)}")

        
    def show_next_question(self):
        if self.current_index < len(self.eccola_type_list):
            ECCOLA_Type = self.eccola_type_list[self.current_index]

            # Update the label
            self.update_label(self.eccolacardsnumber_label, ECCOLA_Type)

            # Clear existing text
            self.clear_text()

            # Filter and format ECCOLA questions
            filtered_eccola_questions = self.eccolaQuestions_data[self.eccolaQuestions_data["ECCOLA_Code"].apply(clean_text.clean_text_delete_midSpace_and_pounds) == clean_text.clean_text_delete_midSpace_and_pounds(ECCOLA_Type)]

            eccola_questions_text = f"{ECCOLA_Type}:\n" + "\n".join([f"- {question}" for question in filtered_eccola_questions['Questions']])
            self.append_text(f"ECCOLA Questions Data for {ECCOLA_Type}:\n{eccola_questions_text}\n\n")

            # Filter and format user stories
            filtered_user_stories = self.userStories_data[self.userStories_data['ECCOLA_Code'] == ECCOLA_Type]
            
            user_stories_text = ""
            for index, row in filtered_user_stories.iterrows():
                issue_id = row['IssueID']
                issue_key = row['IssueKey']
                user_story = row['User_Story'] if pd.notnull(row['User_Story']) else 'No user story provided.'
                comments = row['Comments'] if pd.notnull(row['Comments']) else 'No comments provided.'
                user_stories_text += f"IssueID: {issue_id}\nIssueKey: {issue_key}\nUser Story:\n{user_story}\nComments:\n{comments}\n\n"

            self.append_text(f"User Stories Data for {ECCOLA_Type}:\n{user_stories_text}\n\n")

            # Increment the index for the next question
            self.current_index += 1
        else:
            messagebox.showinfo("Complete", "You have gone through all the ECCOLA questions.")
            self.next_question_button.config(state=tk.DISABLED)
            self.enable_all_elements()



    # GUI Functions
    def update_label(self, label, text):
        self.after(0, lambda: label.config(text=text))

    def append_text(self, text):
        self.after(0, lambda: self.eccolacards_text.config(state=tk.NORMAL))
        self.after(0, lambda: self.eccolacards_text.insert(tk.END, text))
        self.after(0, lambda: self.eccolacards_text.config(state=tk.DISABLED))
        self.after(0, lambda: self.eccolacards_text.see(tk.END))

    def clear_text(self):
        self.after(0, lambda: self.eccolacards_text.config(state=tk.NORMAL))
        self.after(0, lambda: self.eccolacards_text.delete(1.0, tk.END))
        self.after(0, lambda: self.eccolacards_text.config(state=tk.DISABLED))

    def disable_all_elements(self):
        self.upload_questions_button.config(state=tk.DISABLED)
        self.upload_jira_button.config(state=tk.DISABLED)
        self.run_eccola_button.config(state=tk.DISABLED)
        self.eccolacards_text.config(state=tk.DISABLED)
        self.clear_text() # Clear existing content of scrollable announce box

    def enable_all_elements(self):
        self.upload_questions_button.config(state=tk.NORMAL)
        self.upload_jira_button.config(state=tk.NORMAL)
        self.run_eccola_button.config(state=tk.NORMAL)
        self.eccolacards_text.config(state=tk.DISABLED)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Eccola Digital Cards")
    app = EccolaDigitalCards(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
