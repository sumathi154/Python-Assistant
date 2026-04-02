🐍 PyGuide: Interactive Python Assistant
PyGuide is an end-to-end interactive learning dashboard designed to help users master Python programming. It combines AI-powered explanations with a real-time code execution playground, specifically tailored for fields like AI/ML, Data Science, Backend Development, and DevOps.

🌟 Key Features
AI Logic Lab: Get instant, Python-specific explanations for any query using the Groq LPU (Llama 3.3 70B model) for ultra-low latency responses.

Interactive Playground: Don't just read—execute! A built-in code editor allows you to run Python snippets and see the terminal output immediately.

Smart Guardrails: The assistant is strictly focused on Python. It politely declines non-programming queries to keep the learning environment clean.

Dynamic Learning: The interface provides randomized example queries (e.g., "What is a Tuple?", "How to use Lambda?") to inspire exploration.

One-Click Reset: A "Clear All" feature resets the session state, clearing both the query and the code playground for a fresh start.

🛠️ Tech Stack
Frontend: Streamlit (Python-based web framework)

LLM Engine: Groq Cloud (Llama-3.3-70b-versatile)

Environment Management: python-dotenv for API security.

Execution Core: Python exec() with io.StringIO for output capturing.

🚀 Getting Started
1. Prerequisites
Ensure you have Python installed on your system. You will also need a Groq API Key.

2. Installation
Clone this repository or copy the project files, then install the dependencies globally:

Bash
pip install streamlit groq python-dotenv
3. Configuration
Create a .env file in the root directory and add your Groq API key:

Plaintext
GROQ_API_KEY=your_gsk_key_here
4. Running the Project
You can run the project via VS Code terminal:

Bash
streamlit run app.py
OR use the Desktop Icon (.bat file) if you have configured the shortcut.

📂 Project Structure
Plaintext
python_assistant_project/
├── app.py              # Main Streamlit application logic
├── .env                # Secret API keys (Keep this private!)
├── .gitignore          # Prevents sensitive files from being uploaded
├── README.md           # Project documentation
└── Run_PyGuide.bat     # Desktop shortcut for easy execution
🛡️ Security Note
The .gitignore file is configured to exclude the .env file. Never share your .env file or upload it to public repositories like GitHub.
A professional README.md is essential for showcasing your work on GitHub or LinkedIn. Since your project features a "Judge-LLM" architecture and a real-time execution sandbox, the README should highlight these advanced engineering choices.

Here is the complete content for your README.md file:

🐍 PyGuide: Interactive AI Learning Lab
PyGuide is an end-to-end, AI-powered Python Integrated Development Environment (IDE) and tutor. It goes beyond simple code execution by implementing a "Judge-LLM" architecture to provide real-time tutoring, automated quality audits of AI explanations, and performance analytics for executed code.

🌟 Key Features
🤖 Generative & Agentic AI
AI Python Tutor: Uses the Llama-3.3-70b-versatile model via Groq to provide instant, deep-dive explanations for any Python concept.

LLM-as-a-Judge Audit: An automated agentic workflow where a second AI instance critiques the tutor's response for accuracy and clarity, providing a score out of 10.

Smart Prompting: Dynamic placeholder system that suggests high-value Python topics to guide user learning.

🚀 Interactive Code Playground
Real-time Execution: A built-in code editor that executes Python scripts locally using exec() within a controlled scope.

Live Visualizations: Native support for Matplotlib; generate and view plots directly within the web interface.

Performance Analytics: Automatically calculates execution time and code complexity (line count) for every run.

Terminal Redirection: Captures sys.stdout to display print statements in a formatted "Terminal Output" window.

📂 Developer Tools
Script Uploader: Load existing .py files directly into the editor.

Session Management: Clean state handling to wipe playground data or exit the session securely.

Comprehensive Roadmap: A categorized sidebar covering everything from Core Syntax to DevOps and Cybersecurity.

🛠️ Tech Stack
Frontend: Streamlit

LLM Inference: Groq Cloud API (Llama 3.3 70B)

Data Science: Matplotlib, NumPy, Pandas

Environment: Python-dotenv, OS, Sys, IO

🚀 Getting Started
1. Prerequisites
Python 3.9+

A Groq API Key (Get it at console.groq.com)

2. Installation
Bash
# Clone the repository
git clone https://github.com/your-username/pyguide-assistant.git
cd pyguide-assistant

# Install dependencies
pip install -r requirements.txt
3. Environment Setup
Create a .env file in the root directory and add your API key:

Code snippet
GROQ_API_KEY=your_actual_key_here
4. Run the Application
Bash
streamlit run app.py
📊 System Architecture
User Input: User asks a question or writes code.

Tutor Agent: Llama 3.3 generates a response.

Judge Agent: A separate LLM call evaluates the Tutor's response for quality.

Execution Engine: Python code is run through a buffer to capture output and plots.

UI Feedback: Metrics, explanations, and visual results are rendered in Streamlit.

🤝 Contributing
This project is designed for researchers and students. If you have suggestions for new "Focus Areas" or UI improvements, feel free to modify the system_msg in app.py.