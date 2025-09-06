API Forge
Generate API Specifications & Documentation from Code Instantly

API Forge is a web-based tool designed to automatically analyze source code and generate OpenAPI 3.0 specifications. It features a sleek, modern interface that allows users to fetch code from public GitHub repositories, view generated API documentation via Swagger UI, and test endpoints in an interactive playground.

✨ Key Features
Automatic Spec Generation: Converts source code from Python, JavaScript (Node.js/React), HTML, and CSS into OpenAPI 3.0 YAML specifications.

GitHub Integration:

Fetch and browse the file structure of any public GitHub repository.

Generate specifications for a single file or an entire repository.

Repository Summarization: Get a quick overview of a repository's file types and its likely purpose.

Interactive Documentation: Renders the generated specification using Swagger UI for a rich, user-friendly documentation experience.

API Playground: A mock environment to test the generated API endpoints with a settable authorization token.

Secure Viewing: An OTP-based authentication gate protects access to the API documentation and playground.

Modern UI: A dynamic and visually appealing interface built with TailwindCSS, featuring GSAP animations, a particle network background, and 3D tilt effects.

Command Palette: A Ctrl+K command menu provides quick access to all major functions.

⚙️ Tech Stack
Backend: Python, Flask

Frontend: HTML, TailwindCSS, Vanilla JavaScript

Core Libraries:

PyYAML: For handling YAML data in Python.

requests: For making HTTP requests to the GitHub API.

GSAP: For advanced JavaScript animations.

Swagger UI: For rendering interactive API documentation.

js-yaml: For parsing YAML on the frontend.

Phosphor Icons: For modern, lightweight icons.

🚀 Getting Started
Follow these instructions to get a local copy up and running.

Prerequisites
Python 3.7+

pip package manager

Backend Setup
Clone the repository:

git clone <your-repository-url>
cd <repository-folder>

Create and activate a virtual environment:

# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install the required Python packages:

pip install Flask Flask-Cors PyYAML requests python-dotenv

Create an environment file:
Create a file named .env in the root of the project directory.

(Optional but Recommended) Add a GitHub API Token:
To avoid GitHub's strict rate limits for unauthenticated requests, create a personal access token.

Go to GitHub's token generation page.

Generate a new classic token with the public_repo scope.

Add the token to your .env file:

GITHUB_TOKEN="your_personal_access_token_here"

Run the Flask application:

python app.py

The backend server will start, typically on http://127.0.0.1:5000.

Frontend Usage
Once the backend is running, open your web browser and navigate to:
http://127.0.0.1:5000

📋 How to Use
API Forge provides several ways to generate API specifications:

1. From a GitHub Repository
Paste a public GitHub repository URL (e.g., https://github.com/user/repo) into the "Repository Loader" input field and click Fetch.

The file browser will populate with the repository's contents. You can click on folders to navigate.

For a single file: Click on a file to load its content, then click Generate Specification.

For the whole repository: After fetching the root of a repository, click Generate for Whole Repository.

To get a summary: Click Summarize Repository to see a modal with file type distribution and the project's potential purpose.

2. By Pasting Code
Paste your source code directly into the "Source Code" text area on the right panel.

Click the Generate Specification button.

Viewing the Output
After generation, you can navigate through the tabs on the right panel:

Generated Specification: View the raw OpenAPI 3.0 YAML output.

API Documentation: View the interactive Swagger UI documentation.

Interactive Playground: Test the API endpoints.

Unlocking Protected Content
The "API Documentation" and "Interactive Playground" tabs are protected by an OTP gate.

Click the Get OTP button in the top-right corner. A popup will display your 6-digit OTP.

Enter this OTP into the input field on the blurred panel and click Unlock.

You will now have access to the content. The OTP is valid for a single use.

🛠️ How It Works
Language Detection: The Flask backend uses regular expressions to determine the language of the input code (Python, JavaScript, HTML, etc.).

Code Analysis:

For Python, it uses the ast (Abstract Syntax Tree) module to reliably parse function definitions, arguments, and docstrings.

For JavaScript, HTML, and CSS, it uses regex-based parsers to identify functions, elements with IDs, and CSS selectors.

Specification Generation: The extracted code structures are mapped to OpenAPI 3.0 constructs.

Functions are converted into API paths (e.g., def my_func() becomes /my_func).

Functions with arguments are treated as POST endpoints with a request body.

Functions without arguments are treated as GET endpoints.

The result is formatted into a clean YAML string.

Frontend Rendering: The frontend receives the YAML specification and uses Swagger UI to render the interactive documentation and a custom-built interface for the mock playground.
