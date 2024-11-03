# Multi-Agent Hybrid Assistant

## 1. Project Overview

### Project Name
**vPSE Assistant**

### Objective
To develop a multi-agent system that dynamically routes requests, leverages team-specific and shared knowledge bases, and provides secure access control over confidential data for multiple Intel teams.

### Key Components
1. **Operator Agent** - Routes and transfers requests, handles access control.
2. **Troubleshooting Agent** - Adapts dynamically to team contexts and leverages both public and confidential vector stores as needed.
3. **Document Processor Agent** - Manages various document creation and editing tasks, including knowledge articles, training materials, presentations, and white papers.

---

## 2. Project Goals and Requirements

### Primary Goals
- **Efficient Routing**: Direct incoming requests to the appropriate agent and vector store based on context.
- **Team-Specific Knowledge Adaptation**: Support knowledge bases for Intel teams (e.g., vPro, WiFi, Graphics) with access to both shared and team-specific resources.
- **Security and Confidentiality**: Ensure separation and controlled access to public and confidential data.
- **Comprehensive Document Processing**: Provide users with a flexible agent to create various document types using consistent formatting and templates.

### Functional Requirements
- Leverage asyncronous processing or multi-processing when it makes sense.
- Support for querying both team-specific and shared vector stores.
- Access control to distinguish between public and confidential resources.
- Dynamic loading of cross-team public vector stores when contextually required.
- Modular document creation methods tailored for knowledge articles, training materials, white papers, and presentations.
- Use progress indicators (like tqdm) to keep the user informed of progress for long running tasks.
- The user-facing prompt should clearly indicate which agent the user is interacting with, for example, '[vPRO Troubleshooting] Agent' or '[Operator] Agent'.

---

## 3. System Architecture

### High-Level Architecture Diagram
(*Note: Diagram to be created separately to visualize the interaction between the Operator, Troubleshooting Agent, Document Processor Agent, and vector stores.*)

### Components
- **Operator Agent**: Central entry point for routing requests, handles agent transfer and access verification.
- **Troubleshooting Agent**: Loads team-specific prompts, vector stores, and reference materials dynamically. Can request access to additional team vector stores, with permissions.
- **Document Processor Agent**: Consolidated agent with modular methods for creating various documents, such as knowledge articles, training materials, white papers, and presentations. Provides users with a streamlined interface for document-related tasks.

---

## 4. Directory and Data Structure

### Directory Layout
---
project-root/
├── agents/
│   ├── operator.py                   # Main Operator agent
│   ├── troubleshooting_agent.py      # Troubleshooting agent
│   └── document_processor_agent.py   # Document Processor agent
├── config/
│   ├── team_config.yaml              # Global configuration file
│   ├── constants.py                  # Constants and shared settings
├── core/
│   ├── core_tools.py                 # Shared utilities
│   ├── session_manager.py            # Manages session persistence
│   └── config_manager.py             # Loads and manages configurations
├── prompts/
│   ├── router_prompt.md
│   ├── initial_router_prompt.md
├── teams/
│   ├── intel_vpro/
│   │   ├── reference_materials/
│   │   │   ├── public/
│   │   │   └── confidential/
│   │   ├── vector_store/
│   │   │   ├── public/
│   │   │   └── confidential/
│   │   ├── prompts/
│   │   │   └── intel_vpro_prompt.md
│   │   └── config.yaml               # Team-specific configuration file
│   ├── intel_wifi/
│   │   ├── reference_materials/
│   │   │   ├── public/
│   │   │   └── confidential/
│   │   ├── vector_store/
│   │   │   ├── public/
│   │   │   └── confidential/
│   │   ├── prompts/
│   │   │   └── intel_wifi_prompt.md
│   │   └── config.yaml
│   └── intel_graphics/
│       ├── reference_materials/
│       │   ├── public/
│       │   └── confidential/
│       ├── vector_store/
│       │   ├── public/
│       │   └── confidential/
│       ├── prompts/
│       │   └── intel_graphics_prompt.md
│       └── config.yaml
├── shared/
│   ├── reference_materials/          # Shared documents for all teams
│   │   ├── public/
│   │   └── confidential/
│   └── vector_store/
│       ├── public/
│       └── confidential/
└── vpse_assistant.py                 # Entry point to initialize the Operator

---



### Rationale for Design
- **Consolidated Team Resources**: Each team now has its own directory under `./teams`, containing all team-specific resources: configuration, prompts, reference materials, and vector stores.
- **Multiple Prompts per Team**: Each team’s `prompts` subdirectory supports the potential need for multiple prompts. This ensures flexibility for different task contexts, such as troubleshooting and training, without requiring structural changes.

---

## 5. Vector Store and Retrieval

### Vector Store Solution
- **FAISS** is preferred for on-prem deployments due to its high performance in similarity searches, especially with GPU acceleration.
- **Chroma** can be considered if persistence becomes a primary requirement, as it includes built-in data management alongside vector storage.
- We’ll start with FAISS for its speed and flexibility on the local Ubuntu server, with the option to add a persistence layer (e.g., MariaDB) if needed.

### Update Frequency
- **Public Stores**: Refreshed periodically (weekly or monthly) to ensure relevance.
- **Confidential Stores**: Updated more frequently based on the sensitivity of the data. Automated triggers can be implemented to refresh the store following major updates.

---

## 6. Cross-Team Knowledge Sharing

### Access Control
- **Public Information**: No restrictions on access to public vector stores across teams, allowing all teams to freely share and access this data.
- **Confidential Information**: Access to other teams’ confidential vector stores requires explicit authorization from the Operator.

### Auditing Requirements
- **Detailed Tracking**: All access to confidential vectors will be logged, including cross-team requests, to ensure compliance and transparency. Both successful and denied access attempts will be recorded.

---

## 7. Swarm API Integration

### Long-Term Context Persistence
- For future implementations, **MariaDB** will serve as the database for long-term context persistence, enabling session continuity across interactions.
- For short-term caching, an in-memory solution (e.g., Redis) can improve performance in maintaining session state across interactions.

### Tools and Context Variables
- **Operator**: Uses session tracking tools and access control checks, with context variables for session ID, user preferences, and permissions.
- **Troubleshooting Agent**: Will access tools for database and log queries, as well as support documentation APIs.
- **Document Processor Agent**: Integrates with templates and style guides, with context variables specifying document type, user specifications, and formatting requirements.

---

## 8. Deployment and Monitoring

### Deployment Environment
- Initially deployed on a local **Ubuntu server** in a lab setting, supporting on-prem FAISS usage and local network access.
- This deployment will use open-source monitoring tools (e.g., Prometheus and Grafana) to track performance and availability.

### Monitoring and Administration
- A local **admin dashboard** will provide visibility into agent interactions, response times, and error tracking.
- **Alerts** for critical issues, such as unauthorized access attempts or high latency, will be configured to enable prompt response and system stability.

---

## 9. Future Extensions

### Potential Enhancements
- **Advanced Auditing** and **role-based access control** should be prioritized to enhance security and transparency.
- **Query Forwarding** can be introduced in a later phase to facilitate knowledge sharing across teams as the system scales.

---

## 10. Technical Requirements

### Python Version
- **Python 3.12+**: The project requires Python 3.12 or higher to ensure compatibility with the latest features in dependencies like FAISS, LangChain, and OpenAI’s API.

### Core Libraries and Dependencies
The following libraries are essential for implementing vector storage, document processing, and language model integration:

1. **FAISS**: High-performance library for similarity search. Used for local vector storage and retrieval.
2. **LangChain**: Enables chaining of prompts and structured workflows around LLMs. Key for integrating OpenAI’s API with custom prompts and vector-based retrieval.
3. **OpenAI API**: Provides the LLM capabilities for the system. Specific endpoints and models will be configured based on task requirements.

### Data Ingestion and Processing Libraries
To handle a variety of document formats, we’ll include libraries that can read and process these file types:

1. **PDFs**: `pdfplumber` or `PyMuPDF` to extract text from PDF documents.
2. **Text Files**: Standard Python file handling to read `.txt` files.
3. **Markdown**: `markdown` library to parse `.md` files.
4. **Word Documents**: `python-docx` to handle `.docx` files.
5. **CSV and Excel Files**: `pandas` for reading `.csv` and `.xlsx` files.
6. **PowerPoint**: `python-pptx` to process `.pptx` files.
7. **HTML**: `BeautifulSoup` (from `bs4`) to parse and extract content from HTML files.

### Data Ingestion from URLs
- **URL Content Ingestion**: `url_resources.csv` and `Report.csv` files will contain URLs whose HTML content must be scraped and ingested into the vector store. The **BeautifulSoup** library will facilitate HTML parsing, allowing us to extract meaningful text from webpages.
- These files will reside in `project-root/teams/<team_id>/reference_materials/(public/private)` and contain URLs related to each team’s public and confidential resources.

### Environment Configuration and Package Management
To ensure consistent environment setup, we’ll create a `requirements.txt` or `pyproject.toml` file specifying all necessary dependencies with their versions. This file will include the libraries mentioned above, along with any supporting packages (e.g., `requests` for web scraping, `numpy` for FAISS, `regex` for text processing).

---
## 11. Operator Agent Definition
#### **Operator Agent Overview**
The **Operator agent** is the first point of contact for users interacting with the hybrid multi-agent system. Its primary responsibility is to handle user requests and efficiently route them to the appropriate specialized agent. It plays a pivotal role in managing user expectations, gathering necessary initial inputs, and ensuring that each user's request is directed to the right place for optimal handling.

##### **Key Responsibilities**
1. **Initial User Interaction**: The Operator agent will initiate contact, understand the user's intent, and determine the next steps based on predefined categories of tasks. This may include clarifying ambiguities and obtaining more detailed information.
2. **Task Delegation**: Based on user input, the Operator agent will decide which specialized agent should handle the request. It may also provide initial context to facilitate a smooth transition.
3. **Input Validation**: Before delegating, the Operator agent will perform basic validation of user inputs to ensure that tasks are actionable. For example, it will check if all required information is provided, if values are in the expected format, etc.
4. **User Guidance and Updates**: If a user's request cannot be immediately fulfilled, the Operator agent will keep the user informed, providing updates or alternative options where available.

##### **Workflow**
1. **User Request Reception**: The Operator agent receives and analyzes the user's request to classify it.
2. **Validation Step**: Performs a validation of the provided inputs to ensure all required fields are filled, values are correct, and the task is feasible.
3. **Agent Assignment**: Based on the request classification, the Operator selects and hands over control to the appropriate agent.
4. **Feedback and Reiteration**: If the user needs to provide more information, the Operator will prompt the user and loop back to validate until the task is clear enough for processing.

##### **Technical Requirements**
The system architecture of the hybrid multi-agent program involves multiple components that the Operator agent will interact with:

1. **Vector Database (FAISS)**: The system will use FAISS to manage and query document embeddings, which will be utilized for retrieving context and knowledge necessary for certain user requests.
2. **OpenAI API**: The Operator agent will utilize the OpenAI API for natural language processing tasks, including understanding user queries and generating responses. A local LLM may be incorporated as a future failover solution if the system is offline.
3. **Data Ingestion and Processing Libraries**: The Operator agent will work with various data formats that users might provide, utilizing the following libraries for data ingestion:
   - **PDFs**: `pdfplumber` or `PyMuPDF` to extract text from PDF documents.
   - **Text Files**: Standard Python file handling to read `.txt` files.
   - **Markdown**: `markdown` library to parse `.md` files.
   - **Word Documents**: `python-docx` to handle `.docx` files.
   - **CSV and Excel Files**: `pandas` for reading `.csv` and `.xlsx` files.
   - **PowerPoint**: `python-pptx` to process `.pptx` files.
   - **HTML**: `BeautifulSoup` (from `bs4`) to parse and extract content from HTML files.
4. **URL Content Ingestion**: The Operator agent may need to retrieve information from URLs, utilizing tools like **BeautifulSoup** to parse webpage content.
5. **Environment Configuration**: The system will manage dependencies using `requirements.txt` or `pyproject.toml` to specify necessary packages for consistent environment setup.

## 12. Failure Recovery Details
##### **Failure Recovery Plan**
1. **Failed Agent Tasks**
   - When a task assigned to a specialized agent fails (e.g., an unexpected error or an incomplete result), the Operator agent will take control of the user interaction again. It will apologize for the inconvenience and explain the issue in layman's terms if possible.
   - The Operator will attempt **three retries** for the failed task if it seems recoverable. Each retry will be accompanied by a detailed check of failure logs to understand the problem.

2. **Switching Agents**
   - If retries fail, the Operator will assess whether a **different agent** could complete the task. For example, if a data extraction agent fails, a different method or agent could be used as a fallback strategy.
   - This switch may involve an adjustment in how the task is framed or modifying initial assumptions.

3. **Manual Escalation**
   - In the event that retries and switching agents both fail, the Operator will escalate the issue to a **manual support team** or a system administrator. It will ensure that a detailed log of all prior attempts, including any error messages and context, is sent along with the escalation.

4. **User Communication During Failures**
   - The Operator will be responsible for keeping the user informed throughout the failure recovery process. The Operator should provide **status updates** at each major step (e.g., "Attempting again," "Switching to a different approach"). If escalation is required, the user should be informed of a potential delay and be given an estimated response time.

##### **Considerations for Operator Agent Behavior**
- **User Patience Management**: Avoid overwhelming users with technical details during failure situations, but provide transparency about what is happening.
- **Retry and Backoff Strategy**: Implement an exponential backoff strategy for retries to avoid overwhelming the system if the error persists.
- **Fallback Scripts**: Consider having predefined scripts for common failures to handle these scenarios more gracefully and provide a consistent user experience.

