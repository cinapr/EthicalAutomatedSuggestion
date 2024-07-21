# Automating Suggestion of Ethical Implementation Method on Agile Software Project Management

## Project Overview
**Automating Suggestion of Ethical Implementation Method on Agile Software Project Management** is a tool designed to facilitate the integration of ethical practices in agile software project management. The tool provides automated ethical suggestions based on the methodology outlined in the paper "ECCOLA—A Method for Implementing Ethically Aligned AI Systems" by Vakkuri, Ville, et al., published in the Journal of Systems and Software.

## Key Features
- Automated ethical suggestions tailored for agile software project management.
- Integration with ECCOLA methodology for ethical AI systems.
- User-friendly GUI for easy interaction and usability.
- Locally run application ensuring data privacy and security.

## Installation

### Prerequisites
- Operating System: Windows 11
- Python 3.8 or higher
- Git

### Step-by-Step Installation

1. **Clone the Repository**
   - Clone this repository to your local machine using:
     ```bash
     git clone [https://github.com/your-username/your-repository-name.git](https://github.com/cinapr/ECCOLA_AutomatedSuggestion_GUI.git)
     cd your-repository-name
     ```

2. **Install Required Libraries**
   - Install the necessary Python libraries by running:
     ```bash
     .\python.exe -m pip install tkinter
     ```

### Data Preparation

- Ensure the Vakkuri Dataset is placed in the main directory of the cloned repository.
- For each of the tokenizer and interface you need to ensure the model name and csv name is correct (Check directly on the code)

### Running the Scripts 
1. **Install depedencies**
   - Install python depedencies:
     ```bash
     pip install tkinter
     ```
     
2. **Run the system**
   - run the inference script:
     ```bash
     python main.py
     ```

### Usage
1. **Launch the Application**
   - After running the application, the GUI will appear.
     
2. **Navigating the GUI**
   - Use the main dashboard to input your project details.
   - Click on the 'Get Suggestions' button to receive ethical recommendations.
   - Review the suggestions and integrate them into your project management practices.


### Project Structure

```plaintext
├── main.py
├── CONTROLLER
│   ├── eccoladigital_action.py
│   ├── retrieve_jira_action.py
│   ├── suggestion_action.py
│   ├── training_action.py
├── MODEL
│   ├── LoggerMessage.py
│   ├── ECCOLA.py
├── VIEW
│   ├── DownloadECCOLAQuestions.py
│   ├── eccoladigital.py
│   ├── processing.py
│   ├── retrieve_jira.py
│   ├── training.py
├── RESOURCES
│   ├── clean_text.py
│   ├── profile.png
```


### Main Components
1. main.py: Entry point for the application.
2. CONTROLLER: Handles the application's logic and interaction between the model and view.
- eccoladigital_action.py: Manages actions related to ECCOLA digital operations.
- retrieve_jira_action.py: Handles actions to retrieve data from Jira.
- suggestion_action.py: Provides suggestions based on the retrieved data.
- training_action.py: Manages training actions for the model.
3. MODEL: Contains the application's core data and logic.
- LoggerMessage.py: Manages logging messages.
- ECCOLA.py: Core logic for the ECCOLA methodology.
4. VIEW: Manages the application's user interface.
- DownloadECCOLAQuestions.py: Interface for downloading ECCOLA questions.
- eccoladigital.py: Main ECCOLA digital interface.
- processing.py: Interface for processing user stories and suggestions.
- retrieve_jira.py: Interface for retrieving Jira user stories.
- training.py: Interface for training the model.
5. RESOURCES: Contains additional resources such as scripts and images.
- clean_text.py: Text cleaning utilities.
- profile.png: Profile image.
     

### License
1. LLM
[OpenAI Privacy Policy](https://privacy.openai.com/policies) 
[OpenAI Privacy Policy](https://openai.com/policies/privacy-policy/)
[OpenAI Security and Privacy](https://openai.com/security-and-privacy/)
[OpenAI Enterprise Privacy](https://openai.com/enterprise-privacy/)

2. Other Parts
Open-source according to GitHub.

3. Data
Data is run locally on the client machine and is owned privately by the users.

