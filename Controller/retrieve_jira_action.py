import requests
import json
import re  # Import the regular expression module
import csv

class retrieve_jira_action:
    def __init__(self, jira_domain, jira_api_token, jira_email, project_key = "SCRUM", project_id = None):#, parent):
        self.jira_domain=jira_domain
        self.jira_api_token=jira_api_token
        self.jira_email=jira_email
        self.project_key = project_key
        self.project_id = project_id, 

    #CONNECT TO JIRA API
    def connect(self, API_route, params=None):
        # API Endpoint
        url = f'https://{self.jira_domain}{API_route}' 
        print(url)

        auth = (self.jira_email, self.jira_api_token)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        # JQL Query
        if (params is not None):
            # Send the request
            response = requests.get(url, auth=auth, headers=headers, params=params)
        else:
            # Send the request
            response = requests.get(url, auth=auth, headers=headers)


        # Check for errors and print the project keys
        if response.status_code == 200:
            return response
        else:
            ErrorMessage = f"Failed to retrieve response: {response.status_code} - {response.text}"
            print(ErrorMessage)
            return None


    #RETRIEVE JIRA-ID
    def main_retrieve(self, printIDs=False):
        try:
            jql_query = {
                'jql': f'project = {self.project_key}',
                'fields': 'id,key'
            }
            response = self.connect(API_route=f'/rest/api/3/search', params=jql_query)
            if response is not None:
                issues_dict = {}  # Initialize an empty dictionary to store issues
                issues = response.json().get('issues', [])
                issue_amount = 0
                for issue in reversed(issues):
                    issue_id = issue['id']
                    issue_key = issue['key']
                    issues_dict[issue_id] = issue_key
                    issue_amount += 1
                
                # Print the issues from the dictionary
                if(printIDs == True):
                    for issue_id, issue_key in issues_dict.items():
                        print(f"Issue ID: {issue_id}, Key: {issue_key}")

                return True, issues_dict, str(issue_amount)

        except Exception as e:
            failure_msg = f"Fail to retrieve JIRA IDs: {e}"
            print(failure_msg)
            return False, None, failure_msg
        


    #RETRIEVE DETAILS OF JIRA-ID
    def extract_comments(self, comments_json):
        comments_list = []
        
        # Traverse through each comment's body content
        for comment in comments_json:
            body = comment['body']
            for content_block in body['content']:  # Access the outer content block which is the ordered list or bullet list
                if content_block['type'] == 'orderedList' or content_block['type'] == 'bulletList':
                    for item in content_block['content']:  # Iterate through each list item in the content
                        paragraph_content = []
                        for paragraph in item['content']:  # Access content within each list item
                            for text_block in paragraph['content']:  # Each text block within a paragraph
                                if text_block['type'] == 'text':
                                    paragraph_content.append(text_block['text'])
                                elif text_block['type'] == 'hardBreak':
                                    paragraph_content.append('\n')  # Add a new line for hard breaks
                        # Join all parts of the list item into a single string and add it to the list
                        comments_list.append(' '.join(paragraph_content))
        
        return comments_list
    
    def get_description_text(self,data):
        """
        Extracts and concatenates the text from the description content of the given data dictionary.
        
        Args:
        - data (dict): The input dictionary containing JIRA issue data.
        
        Returns:
        - str: The concatenated description text.
        """
        # Retrieve 'fields' from the data dictionary safely
        fields = data.get('fields')
        if not isinstance(fields, dict):
            return ''

        # Retrieve 'description' from the fields dictionary safely
        description = fields.get('description')
        if not isinstance(description, dict):
            return ''

        # Retrieve 'content' from the description dictionary safely
        description_content = description.get('content')
        if not isinstance(description_content, list):
            return ''

        # Initialize an empty list to collect text segments
        description_text_list = []

        # Iterate over the content safely
        for paragraph in description_content:
            # Ensure 'content' exists and is a list before accessing [0]
            if isinstance(paragraph.get('content'), list) and len(paragraph['content']) > 0:
                first_content = paragraph['content'][0]
                # Check if 'text' exists in the first content dictionary
                if 'text' in first_content:
                    description_text_list.append(first_content['text'])

        # Join the collected text segments into a single string
        description_text = ' '.join(description_text_list)
        return description_text
    
    def details_retrieve(self, issue_key, params=None, getComments=False, getAttachments=False, printDetails=False):
        try:
            # Send the request
            response = self.connect(API_route=f'/rest/api/3/issue/{issue_key}', params=params)

            if (response is None):
                failure_msg = "The details of " + str(issue_key) + " are not found"
                print(failure_msg)
                return False, None, failure_msg
                
            else:
                data = response.json()

                #GET COMMENTS
                comments = ""
                if(getComments):
                    # Assuming 'data' is your JSON object loaded from the response
                    comment_data = data['fields']['comment']['comments']
                    extractcomments = self.extract_comments(comment_data)

                    # Print each comment retrieved
                    for i, comment in enumerate(extractcomments, 1):
                        comments += str(i) + " : " + str(comment) + "\n" 

                #GET ATTACHMENTS
                relevant_attachments = []
                relevant_attachments_links = None
                attachment_list = None
                if(getAttachments):
                    attachment_list = [attachment['filename'] for attachment in data['fields']['attachment']]
                    attachments = data['fields'].get('Attachments', [])
                    
                    # Extract relevant attachments
                    pattern = re.compile(r'CR_.+\.(pdf|docx?|DOCX?)$')
                    for attachment in attachments:
                        if pattern.match(attachment['filename']):
                            relevant_attachments.append(attachment['content']['href'])
                    relevant_attachments_links = ' | '.join(relevant_attachments)  # Join all relevant attachment links with a separator

                description_text = self.get_description_text(data)

                issue_details = {
                    'JIRAID': data['id'],
                    'IssueKey': issue_key,
                    'IssueTitle': data['fields']['summary'],
                    'OpenDate': data['fields']['created'],
                    'State': data['fields']['status']['name'],
                    'Close Date': data['fields'].get('resolutiondate', 'Not closed'),
                    'Description': description_text,
                    'Attachments': attachment_list,
                    'Comments':comments,
                    'RelevantAttachments':relevant_attachments,
                    'RelevantAttachmentsLinks':relevant_attachments_links
                }

                # Print all issue details
                if(printDetails):
                    for key, value in issue_details.items():
                        print(f"{key}: {value}")

                return True, issue_details, None

        except Exception as e:
            failure_msg = f"Fail to retrieve details of " + str(issue_key) + " : {e}"
            print(failure_msg)
            return False, None, failure_msg


        


    