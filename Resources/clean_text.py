class clean_text:
    #Cleaning for training - Have space for better view
    def clean_text(text):
        """Basic text cleaning to standardize the dataset."""
        text = text.lower()  # Convert text to lowercase
        text = ' '.join(text.split())  # Replace multiple spaces with a single space
        return text

    #Cleaning for evaluation of result, no space to prevent error due to space available
    def clean_text_delete_midSpace(text):
        """Basic text cleaning to standardize the dataset."""
        text = text.lower()  # Convert text to lowercase
        text = ' '.join(text.split())  # Replace multiple spaces with a single space
        text = text.strip().replace(" ", "") 
        return text

    #Cleaning for evaluation of result, no space to prevent error due to space available
    def clean_text_delete_midSpace_and_pounds(text):
        """Basic text cleaning to standardize the dataset."""
        text = text.lower()  # Convert text to lowercase
        text = ' '.join(text.split())  # Replace multiple spaces with a single space
        text = text.strip().replace(" ", "")  # Remove all spaces
        text = text.replace("#", "")  # Remove all '#' characters
        return text