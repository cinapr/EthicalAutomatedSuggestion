import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox

class DownloadECCOLAQuestions:
    def __init__(self, parent):
        self.parent = parent

    def download_questions_1(self):
        data = {
            "ECCOLA_Code": ["0 Stakeholder Analysis", "2 Explainability", "3 Communication", "4 Documenting Trade-offs", "5 Traceability", "6 System Reliability", "7 Privacy and Data", "8 Data Quality", "9 Access to Data", "10 Human Agency", "11 Human Oversight", "12 System Security", "13 System Safety", "14 Accessibility", "15 Stakeholder Participation", "16 Environmental Impact", "17 Societal Effects", "18 Auditability", "19 Ability to Redress", "1 Typesof Transparency", "1 Typesof Transparency", "1 Typesof Transparency", "1 Typesof Transparency"],
            "Questions_Reasoning": [
                "Autonomous cars don’t just affect their passengers. Anyone nearby is affected; some even change the way they drive. If at one point half of the traffic consists of self-driving cars, what are the societal impacts of such systems? E.g., how are the people who can’t afford one affected? Regulations arising from such systems also affect everyone.",
                "When interacting with a robot, users could ideally ask the robot “why did you do that?” and receive an understandable response. This would make it much easier for them to trust a system.",
                "Clearly stating what data you collect and why can make you seem much more trustworthy. Compare this to a cellphone application that just states it needs to access your camera and storage.",
                "Documenting trade-offs can improve your customer relationship, allowing you to better explain why certain decisions were made over others. Moreover, it can reduce the responsibility placed on the individual developer(s) from an ethical point of view.",
                "When the system starts making mistakes, by aiming for traceability, it will be easier to find out the cause. Consequently, it will also be faster and possibly easier to start fixing the underlying issue.",
                "An autonomous coffee machine successfully brews coffee 8 times out of 10. While this is a decent success rate, we are left wondering what happened the 2 times it failed to do so, and why. Errors are inevitable, but we must understand the causes behind them and be able to replicate them to fix them.",
                "Rather than collecting and selling data, appealing to privacy can also be profitable. Regulations are making it increasingly difficult to collect lots of personal data for profit. Privacy can be an alternate selling point in today’s climate.",
                "In 2017, Amazon scrapped its recruitment AI because of bad data. They used past recruitment data to teach the AI. As they had mostly hired men, the AI began to consider women undesirable based on the data.",
                "Third parties you give access to the data can misuse it. A prominent example of this is the case of Cambridge Analytica and Facebook, in which data from Facebook was used questionably. However, such incidents can also paint your organization in a bad light even if you were not the ones misusing the data.",
                "A medical system recommends diagnoses. How does the system communicate to doctors why it made a recommendation? How should the doctors know when to challenge the system? Does the system somehow change how patients and doctors interact?",
                "Assuming control is especially related to cyber-physical systems such as drones or other vehicles. For purely digital systems, the focus should be on supporting human decision-making instead of directing it.",
                "The autonomous nature of AI systems makes new vectors of attack possible. A white line drawn across a road can confuse a self-driving vehicle. What happened to Microsoft’s TayTwitter bot is another example of a new type of attack.",
                "AI systems can aid automating various organizational tasks, making it possible to reduce personnel. However, if a customer organization becomes reliant on your AI system to handle a portion of its operations, what happens if that AI stops functioning for even a few days? What could you do to alleviate the impact?",
                "AI tends to benefit those who are already technologically capable, resulting in increased inequality. E.g., most of the images used in machine learning have been labeled by young white men.",
                "Often the people an AI system is used on are individuals who are simply objects for the system. For example, a medical system is developed for hospitals, used by doctors, but ultimately used on patients. Why not talk to the patients too?",
                "If you are hosting on a third party cloud, try to ascertain the sustainability of the service provider’s services. If you are using hardware, are you processing the data in each physical device of your own or are you processing it in the cloud?",
                "Surveillance technology utilizing facial recognition AI has long-reaching impacts. People may wish to avoid areas that utilize such surveillance, negatively affecting businesses in said area. People may become stressed at the mere thought of such surveillance. Some may even emigrate as a result.",
                "In heavily regulated fields such as medicine, audits are typically required before a system can be utilized in the first place.",
                "AI systems can inconvenience users in unforeseen, unpredictable ways. Depending on the situation, the company may or may not be legally responsible for the inconvenience. Nonetheless, by offering a digital platform for seeking redress, your company can seem more trustworthy while also offering additional value to your users.",
                "As an IT support staff, I want to have access to a real-time monitoring dashboard of our system's operations so that I can quickly understand the current status and performance metrics, ensuring prompt troubleshooting and maintenance.",
                "As a Customer Support Manager, I want a detailed FAQ section available on our platform that explains our system's features and services so that customers can easily find answers to their questions, reducing the volume of basic inquiry calls to our support team.",
                "As a Data Analyst, I want to access a detailed log of all data inputs and algorithm changes that affect customer recommendations, so that I can ensure accuracy and fairness in the outputs provided by our recommendation system.",
                "As a new developer on the team, I want to access a comprehensive version history and development documentation of our system, so I can understand the evolution of its architecture and the reasons behind past design decisions."
            ]
        }
        df = pd.DataFrame(data)
        self.save_csv(df, "ECCOLA_QuestionsCorrelations.csv")

    def download_questions_2(self):
        data = {
            "ECCOLA_Code": ["0 Stakeholder Analysis", "0 Stakeholder Analysis", "0 Stakeholder Analysis", "0 Stakeholder Analysis", "1 Typesof Transparency", "1 Typesof Transparency", "1 Typesof Transparency", "1 Typesof Transparency", "2 Explainability", "2 Explainability", "2 Explainability", "2 Explainability", "2 Explainability", "2 Explainability", "3 Communication", "3 Communication", "3 Communication", "3 Communication", "3 Communication", "4 Documenting Trade-offs", "4 Documenting Trade-offs", "5 Traceability", "5 Traceability", "5 Traceability", "6 System Reliability", "6 System Reliability", "6 System Reliability", "6 System Reliability", "7 Privacy and Data", "7 Privacy and Data", "7 Privacy and Data", "7 Privacy and Data", "7 Privacy and Data", "8 Data Quality", "8 Data Quality", "8 Data Quality", "8 Data Quality", "8 Data Quality", "8 Data Quality", "9 Access to Data", "9 Access to Data", "9 Access to Data", "9 Access to Data", "10 Human Agency", "10 Human Agency", "10 Human Agency", "10 Human Agency", "11 Human Oversight", "11 Human Oversight", "11 Human Oversight", "12 System Security", "12 System Security", "12 System Security", "12 System Security", "13 System Safety", "13 System Safety", "13 System Safety", "13 System Safety", "13 System Safety", "13 System Safety", "14 Accessibility", "14 Accessibility", "14 Accessibility", "14 Accessibility", "14 Accessibility", "14 Accessibility", "15 Stakeholder Participation", "15 Stakeholder Participation", "15 Stakeholder Participation", "16 Environmental Impact", "16 Environmental Impact", "16 Environmental Impact", "17 Societal Effects", "17 Societal Effects", "17 Societal Effects", "18 Auditability", "18 Auditability", "18 Auditability", "18 Auditability", "19 Ability to Redress", "19 Ability to Redress", "19 Ability to Redress", "20 Minimizing Negative Impacts", "20 Minimizing Negative Impacts", "20 Minimizing Negative Impacts", "20 Minimizing Negative Impacts"],
            "Questions": [
                "Who does the system affect, and how? Stakeholders are not simply users, developers and customers.",
                "How are the various stakeholders linked together?",
                "Can these different stakeholders influence the development of the system? How?",
                "Remember that a user is often an organization and the end-user is an individual. Similarly, AI systems can treat people as objects for data collection.",
                "Are you trying to understand something? (Internal transparency)",
                "Are you trying to explain something? (External transparency)",
                "Are you trying to understand or explain how the system works? (Transparency of algorithms and data)",
                "Are you trying to understand or explain why the system was made to be the way it now is? (Transparency of system development)",
                "Is explainability a goal for your system? How do you plan to ensure it?",
                "How well can each decision of the system be understood? By both developers and (end-)users.",
                "Did you try to use the simplest and most interpretable model possible for the context?",
                "Did you make trade-offs between explainability and accuracy? What kind of? Why?",
                "How familiar are you with your training or testing data? Can you change it when needed?",
                "If you utilize third party components in the system, how well do you understand them?",
                "What is the goal of the system? Why is this particular system deployed in this specific area?",
                "What do you communicate about the system to its users and end-users? Is it enough for them to understand how the system works?",
                "If relevant to your system, do you somehow tell your (end-)users that they are interacting with an AI system and not with another human being?",
                "Do you collect user feedback? How is it used to change/improve the system?",
                "Are communication and transparency towards other audiences, such as the general public, relevant?",
                "Are relevant interests and values implicated by the system and potential trade-offs between them identified and documented?",
                "Who decides on such trade-offs (e.g. between two competing solutions) and how? Did you ensure that the trade-off decision and the reasons behind it were documented?",
                "How have you documented the development of the system, both in terms of code and decision-making? How was the model built or the AI trained?",
                "How have you documented the testing and validation process? In terms of data and scenarios used etc.",
                "How do you document the actions of the system? What about alternate actions (e.g. if the user was different but the situation otherwise the same)?",
                "How do you test if the system fulfills its goals?",
                "Have you tested the system comprehensively, including unlikely scenarios? Have the tests been documented?",
                "When the system fails in a certain scenario, will you be able to tell why? Can you replicate the failure?",
                "How do you assure the (end-)user of the system’s reliability?",
                "What data are used by the system?",
                "Does the system use or collect personal data? Why? How is the personal data used?",
                "Do you clearly inform your (end-)users about any personal data collection? E.g., ask for consent, provide an opportunity to revoke it etc.",
                "Have you taken measures to enhance (end-user) privacy, such as encryption or anonymization?",
                "Who makes the decisions regarding data use and collection? Do you have organizational policies for it?",
                "What are good or poor quality data in the context of your system?",
                "How do you evaluate the quality and integrity of your own data? Are there alternative ways?",
                "If you utilize data from external sources, how do you control their quality?",
                "Did you align your system with relevant standards (for example ISO, IEEE) or widely adopted protocols for daily data management and governance?",
                "How can you tell if your data sets have been hacked or otherwise compromised?",
                "Who handles the data collection, storage, and use?",
                "Who can access the users’ data, and under what circumstances?",
                "How do you ensure that the people who access the data: 1) have a valid reason to do so; and 2) adhere to the regulations and policies related to the data?",
                "Do you keep logs of who accesses the data and when? Do the logs also tell why?",
                "Do you use existing data governance frameworks or protocols? Does your organization have its own?",
                "Does the system interact with decisions by human actors, i.e. end users (e.g. recommending users actions or decisions, or presenting options)?",
                "Does the system communicate to its (end) users that a decision, content or outcome is the result of an algorithmic decision? Into how much detail does it go?",
                "In the system’s use context, what tasks are done by the system and what tasks are done by humans?",
                "Have you taken measures to prevent overconfidence or overreliance on the system?",
                "Who can control the system and how? In what situations?",
                "What would be the appropriate level of human control for this particular system and its use cases?",
                "Related to the Safety and Security cards: how do you detect and respond if something goes wrong? Does the system then stop entirely, partially, or would control be delegated to a human? Why?",
                "Did you assess potential forms of attacks to which the system could be vulnerable? Did you consider ones that are unique or more relevant to AI systems?",
                "Did you consider different types of vulnerabilities, such as data pollution and physical infrastructure?",
                "Have you verified how your system behaves in unexpected situations and environments?",
                "Does your organization have cybersecurity personnel? Are they involved in this system?",
                "What kind of risks does the system involve? What kind of damage could it cause?",
                "How do you measure and assess risks and safety?",
                "What fallback plans does your system have? Have they been tested?",
                "In what conditions do the fallback plans trigger? Are they automatic or do they require human input?",
                "Is there a plan to mitigate or manage technological errors, accidents, or malicious misuse? What if the systems provide wrong results, become unavailable, or provide societally unacceptable results?",
                "What liability and consumer protection laws apply to your system? Have you taken them into account?",
                "Does the system consider a wide range of individual preferences and abilities? If not, why?",
                "Is the system usable by those with special needs or disabilities, those at risk of exclusion, or those using assistive technologies?",
                "Were people representing various groups somehow involved in the development of the system?",
                "How is the potential user audience taken into account?",
                "Is the team involved in building the system representative of your target user audience? Is it representative of the general population?",
                "Did you assess whether there could be (groups of) people who might be disproportionately affected by the negative implications of the system?",
                "Which stakeholders are stakeholders in system development?",
                "How are the different stakeholders of the system involved in the development of the system? If they aren’t, why?",
                "How do you inform your external and internal stakeholders of the system’s development?",
                "Did you assess the environmental impact of the system’s development, deployment, and use? E.g., the type of energy used by the data centers.",
                "Did you consider the environmental impact when selecting specific technical solutions?",
                "Did you ensure measures to reduce the environmental impact of your system’s life cycle?",
                "Did you assess the broader societal impact of the AI system’s use beyond the individual (end-)users? Consider stakeholders who might be indirectly affected by the system.",
                "How will the systems affect society when in use?",
                "What kind of systemic effects could the system have?",
                "Is the system auditable?",
                "Can an audit be conducted independently?",
                "Is the system available for inspection?",
                "What mechanisms facilitate the system's auditability? How is traceability and logging of the system's processes and outcomes ensured?",
                "What is your (developer organization) responsibility if the system causes damage or otherwise has a negative impact?",
                "In the event of a negative impact, can the ones affected seek redress?",
                "How do you inform users and other third parties about opportunities for redress?",
                "Are the people involved with the development of the system also involved with it during its operational life? If not, they may not feel as accountable.",
                "Are you aware of laws related to the system?",
                "Can users of the system somehow report vulnerabilities, risks, and other issues in the system?",
                "With whom have you discussed accountability and other ethical issues related to the system, including grey areas?"
            ]
        }
        df = pd.DataFrame(data)
        self.save_csv(df, "ECCOLA_Questions.csv")

    def save_csv(self, dataframe, default_filename):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=default_filename, filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                dataframe.to_csv(file_path, index=False)
                messagebox.showinfo("Success", f"{os.path.basename(file_path)} has been saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

