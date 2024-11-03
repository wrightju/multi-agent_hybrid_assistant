# Creating the DocumentProcessorAgent class structure for placement in `agents/document_processor_agent.py`.

class DocumentProcessorAgent:
    def __init__(self, templates=None):
        """
        Initialize the DocumentProcessorAgent with optional templates.
        
        Parameters:
        - templates (dict): A dictionary of document templates with placeholders.
        """
        self.templates = templates if templates else {}

    def add_template(self, name, template):
        """
        Add a new document template.
        
        Parameters:
        - name (str): The name of the template.
        - template (str): The template string with placeholders (e.g., '{title}', '{content}').
        """
        self.templates[name] = template

    def handle_request(self, request):
        """
        Processes a document creation request using a specified template.
        
        Parameters:
        - request (dict): Contains request details with keys 'template', 'title', and 'content'.
        
        Returns:
        - str: The generated document as a string.
        """
        template_name = request.get('template')
        title = request.get('title', 'Untitled')
        content = request.get('content', 'No content provided.')

        # Check if the requested template exists
        template = self.templates.get(template_name)
        if not template:
            return f"Error: Template '{template_name}' not found."

        # Fill in the template placeholders with provided data
        document = template.format(title=title, content=content)
        return document


# This would be placed in `agents/document_processor_agent.py`.
# Initial testing of this class can be done once registered with OperatorAgent.

DocumentProcessorAgent  # Display the class for review and verification.
