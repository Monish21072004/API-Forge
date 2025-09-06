
# API Forge  
**Generate API Specifications & Documentation from Code Instantly**

API Forge is a web-based tool designed to automatically analyze source code and generate **OpenAPI 3.0 specifications**.  
It features a **sleek, modern interface** that allows users to fetch code from public GitHub repositories, view generated API documentation via Swagger UI, and test endpoints in an **interactive playground**.

---

## ✨ Key Features

- **Automatic Spec Generation**  
  Converts source code from **Python**, **JavaScript (Node.js/React)**, **HTML**, and **CSS** into **OpenAPI 3.0 YAML specifications**.

- **GitHub Integration**  
  - Fetch and browse the file structure of any public GitHub repository.  
  - Generate specifications for a **single file** or an **entire repository**.

- **Repository Summarization**  
  Get a quick overview of a repository's **file types** and its **likely purpose**.

- **Interactive Documentation**  
  Renders the generated specification using **Swagger UI** for a rich, user-friendly documentation experience.

- **API Playground**  
  A **mock environment** to test the generated API endpoints with a settable **authorization token**.

- **Secure Viewing**  
  An **OTP-based authentication gate** protects access to the API documentation and playground.

- **Modern UI**  
  Built with **TailwindCSS**, featuring:
  - **GSAP animations**
  - **Particle network background**
  - **3D tilt effects**

- **Command Palette**  
  A `Ctrl + K` command menu provides quick access to all major functions.

---

## ⚙️ Tech Stack

- **Backend**: Python, Flask  
- **Frontend**: HTML, TailwindCSS, Vanilla JavaScript  

**Core Libraries:**
- [PyYAML](https://pyyaml.org/) – Handling YAML data in Python.  
- [requests](https://pypi.org/project/requests/) – For making HTTP requests to the GitHub API.  
- [GSAP](https://greensock.com/gsap/) – Advanced JavaScript animations.  
- [Swagger UI](https://swagger.io/tools/swagger-ui/) – Interactive API documentation.  
- [js-yaml](https://github.com/nodeca/js-yaml) – YAML parsing on the frontend.  
- [Phosphor Icons](https://phosphoricons.com/) – Lightweight modern icons.

---

## 🚀 Getting Started

Follow these instructions to get a local copy up and running.

### **Prerequisites**
- Python **3.7+**
- `pip` package manager

---

### **Backend Setup**

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd <repository-folder>
````

2. **Create and activate a virtual environment:**

   **Windows:**

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

   **macOS/Linux:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required Python packages:**

   ```bash
   pip install Flask Flask-Cors PyYAML requests python-dotenv
   ```

4. **Create an environment file:**

   * Create a file named `.env` in the root of the project directory.

5. **(Optional but Recommended) Add a GitHub API Token:**

   * To avoid GitHub's strict rate limits for unauthenticated requests, create a **personal access token**:

     * Go to [GitHub Token Generation](https://github.com/settings/tokens).
     * Generate a new classic token with the `public_repo` scope.
     * Add the token to your `.env` file:

       ```
       GITHUB_TOKEN="your_personal_access_token_here"
       ```

6. **Run the Flask application:**

   ```bash
   python app.py
   ```

   The backend server will typically start at:

   ```
   http://127.0.0.1:5000
   ```

---

### **Frontend Usage**

Once the backend is running, open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

## 📋 How to Use

### **1. From a GitHub Repository**

1. Paste a **public GitHub repository URL** (e.g., `https://github.com/user/repo`) into the **Repository Loader** input field and click **Fetch**.
2. The **file browser** will populate with the repository's contents.

   * Click on folders to navigate deeper.
3. **For a single file**:

   * Click on a file to load its content, then click **Generate Specification**.
4. **For the whole repository**:

   * After fetching the root of a repository, click **Generate for Whole Repository**.
5. **To get a summary**:

   * Click **Summarize Repository** to view a modal showing:

     * File type distribution.
     * Project's potential purpose.

---

### **2. By Pasting Code**

1. Paste your source code directly into the **Source Code** text area on the right panel.
2. Click **Generate Specification**.

---

## 📄 Viewing the Output

After generation, you can navigate through the right-side tabs:

* **Generated Specification**
  View the **raw OpenAPI 3.0 YAML output**.

* **API Documentation**
  View the **interactive Swagger UI documentation**.

* **Interactive Playground**
  Test the generated API endpoints.

---

## 🔐 Unlocking Protected Content

The **API Documentation** and **Interactive Playground** tabs are **protected by an OTP gate**.

1. Click **Get OTP** in the top-right corner.
   A popup will display your **6-digit OTP**.
2. Enter this OTP into the input field on the blurred panel.
3. Click **Unlock**.

   * The OTP is valid for **a single use**.

---

## 🛠️ How It Works

1. **Language Detection**

   * The Flask backend uses **regular expressions** to determine the language of the input code:

     * Python
     * JavaScript
     * HTML
     * CSS

2. **Code Analysis**

   * **Python**: Uses the `ast` (Abstract Syntax Tree) module to parse:

     * Function definitions
     * Arguments
     * Docstrings
   * **JavaScript, HTML, CSS**: Uses regex-based parsers to identify:

     * Functions
     * HTML elements with IDs
     * CSS selectors

3. **Specification Generation**

   * Extracted code structures are mapped to **OpenAPI 3.0 constructs**.
   * Rules:

     * Functions → API paths (e.g., `def my_func()` → `/my_func`).
     * Functions **with arguments** → **POST endpoints** with a request body.
     * Functions **without arguments** → **GET endpoints**.
   * Final result is output as a **clean YAML string**.

4. **Frontend Rendering**

   * The frontend receives the YAML specification and uses **Swagger UI** to render:

     * Interactive documentation.
     * A **custom-built playground** for mock testing.

---

## 📜 License

This project is licensed under the MIT License.
See the LICENSE file for details.

---

## 🌟 Summary

API Forge simplifies API documentation by automatically converting source code into **OpenAPI 3.0 specs**, with **interactive Swagger UI**, **GitHub integration**, and a **modern, animated interface**.

```

This `.md` file is fully structured for a GitHub **README.md** with proper headings, code blocks, and formatting.
```
