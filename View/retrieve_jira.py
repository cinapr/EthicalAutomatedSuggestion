#function for UI
import tkinter as tk
from tkinter import messagebox

#function for access JIRA
import requests
import json
import re  # Import the regular expression module
import csv

#UDF
from Controller.retrieve_jira_action import retrieve_jira_action


class RetrieveJiraPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#FFDD44")
        title_label = tk.Label(self, text="RETRIEVE JIRA USER STORIES TO CSV", font=("Helvetica", 18, "bold"), bg="#FFDD44")
        title_label.pack(pady=20)

        credentials_label = tk.Label(self, text="CREDENTIALS\nEnter your JIRA API Keys", font=("Helvetica", 14), bg="#FFDD44")
        credentials_label.pack(pady=10)

        project_name_label = tk.Label(self, text="Project Name", font=("Helvetica", 12), bg="#FFDD44")
        project_name_label.pack()
        self.project_name_entry = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.project_name_entry.pack(pady=5)

        project_id_label = tk.Label(self, text="Project ID", font=("Helvetica", 12), bg="#FFDD44")
        project_id_label.pack()
        self.project_id_entry = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.project_id_entry.pack(pady=5)

        jira_email_label = tk.Label(self, text="Email used in JIRA", font=("Helvetica", 12), bg="#FFDD44")
        jira_email_label.pack()
        self.jira_email_entry = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.jira_email_entry.pack(pady=5)

        jira_domain_label = tk.Label(self, text="JIRA Domain (NAME.atlassian.net)", font=("Helvetica", 12), bg="#FFDD44")
        jira_domain_label.pack()
        self.jira_domain_entry = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.jira_domain_entry.pack(pady=5)

        api_key_label = tk.Label(self, text="API Key", font=("Helvetica", 12), bg="#FFDD44")
        api_key_label.pack()
        self.api_key_entry = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.api_key_entry.pack(pady=5)

        retrieve_csv_button = tk.Button(self, text="RETRIEVE TO CSV", bg="#FFA500", fg="white", font=("Helvetica", 14), command=self.retrieve_to_csv)
        retrieve_csv_button.pack(pady=20)

    def retrieve_to_csv(self):
        #GET SET UP JIRA SETTING FROM INPUT
        project_key = self.project_name_entry.get()
        project_id = self.project_id_entry.get()
        api_key = self.api_key_entry.get()
        email = self.jira_email_entry.get()
        jira_domain = self.jira_domain_entry.get()


        #RETRIEVE JIRA ID
        app = retrieve_jira_action(jira_domain=jira_domain, jira_api_token=api_key, jira_email=email, project_key = project_key, project_id = project_id)
        success_main_retrieve, issues_dict, issue_error_or_amount = app.main_retrieve(printIDs=False)
        #app.mainloop()
        message = ""

        if(success_main_retrieve == False):
            message = issue_error_or_amount

        else:
            #RETRIEVE JIRA DETAILS
            fields = 'id,assignee,created,status,resolutiondate,description,summary,comment,attachment'
            params={'fields': fields}

            # Open a CSV file to write the issue details
            getComments = True
            export_csv_filename = 'jira_issues.csv'
            
            try:
                with open(export_csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
                    fieldnames = ['IssueID', 'IssueKey', 'User_Story', 'Comments', 'ECCOLA_Code']
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()

                    for issue_id, issue_key in issues_dict.items():
                        success_detail_retrieve, issue_details, failure_msg = app.details_retrieve(issue_key=issue_key, params=params, getComments=getComments, getAttachments=False, printDetails=True)
                        if success_detail_retrieve:
                            writer.writerow({
                                'IssueID': issue_id,
                                'IssueKey': issue_key,
                                'User_Story': ' '.join([issue_details.get('IssueTitle', ''), issue_details.get('Description', '')]),
                                'Comments': '' if not getComments else issue_details.get('Comments', ''),
                                'ECCOLA_Code': ''  # Empty column
                            })
                        else:
                            message += failure_msg + "\n"

                message += "\nFINISH RETRIEVING JIRA " + str(jira_domain) + " - " + str(project_key) + " to " + export_csv_filename
            
            except Exception as e:
                message += f"Fail to retrieve JIRA " + str(jira_domain) + " - " + str(project_key) + " : " + str(e)
                

        #PRINT RETURN
        # Construct the message
        #message = f"Project Name: {project_name}\nProject ID: {project_id}\nAPI Key: {api_key}"

        # Display the message in a messagebox
        messagebox.showinfo("Retrieved Information", message)