from flask import Flask, jsonify, request, abort, send_from_directory, make_response
from flask_cors import CORS
import ast
import re
import yaml
import requests
import os
from dotenv import load_dotenv
import random
import string

# Load environment variables from a .env file
load_dotenv()

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# In-memory store for OTP
current_otp = None


# --- Route to serve the frontend ---
@app.route('/')
def index():
    # This serves your index.html file as the main page
    return send_from_directory('.', 'index.html')


# --- Helper to get GitHub headers ---
def get_github_headers():
    token = os.getenv('GITHUB_TOKEN')
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f"token {token}"
    return headers


# --- Route to fetch from GitHub ---
@app.route('/fetch-github', methods=['POST'])
def fetch_github():
    data = request.get_json()
    if not data or 'url' not in data:
        abort(400, description="Missing 'url' in request body.")
    url = data['url']
    github_regex = r"https://github\.com\/([^/]+)\/([^/]+)(?:\/(?:blob|tree)\/([^/]+))?\/?(.*)"
    match = re.match(github_regex, url)
    if not match:
        abort(400, description="Invalid GitHub URL format.")
    user, repo, branch, path = match.groups()
    if repo.endswith('.git'):
        repo = repo[:-4]
    branch = branch or 'main'
    api_url = f"https://api.github.com/repos/{user}/{repo}/contents/{path}?ref={branch}"
    try:
        response = requests.get(api_url, headers=get_github_headers())
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        abort(500, description=f"Could not fetch data from GitHub: {e}")


# --- Recursive function to get all files in a repository ---
def fetch_repo_contents_recursive(user, repo, branch, path):
    api_url = f"https://api.github.com/repos/{user}/{repo}/contents/{path}?ref={branch}"
    response = requests.get(api_url, headers=get_github_headers())
    response.raise_for_status()
    contents = response.json()
    all_files = []
    for item in contents:
        if item['type'] == 'file':
            all_files.append(item)
        elif item['type'] == 'dir':
            all_files.extend(fetch_repo_contents_recursive(user, repo, branch, item['path']))
    return all_files


# --- Route to summarize a repository ---
@app.route('/summarize-repo', methods=['POST'])
def summarize_repo():
    data = request.get_json()
    if not data or 'user' not in data:
        abort(400, description="Missing repository info in request.")
    user, repo, branch = data['user'], data['repo'], data.get('branch', 'main')
    try:
        all_files = fetch_repo_contents_recursive(user, repo, branch, '')

        summary = {
            "repository": f"{user}/{repo}",
            "total_files": len(all_files),
            "file_types": {},
            "potential_purpose": "Unknown"
        }

        for file_info in all_files:
            ext = os.path.splitext(file_info['name'])[1]
            if ext:
                summary["file_types"][ext] = summary["file_types"].get(ext, 0) + 1

        filenames = [f['name'].lower() for f in all_files]
        if 'package.json' in filenames:
            summary['potential_purpose'] = 'JavaScript/Node.js Project'
        elif 'requirements.txt' in filenames or 'app.py' in filenames:
            summary['potential_purpose'] = 'Python Application'
        elif 'index.html' in filenames and '.css' in summary['file_types']:
            summary['potential_purpose'] = 'Web Frontend Project'
        elif 'pom.xml' in filenames or 'build.gradle' in filenames:
            summary['potential_purpose'] = 'Java Project'

        summary_text = f"Repository Summary for {summary['repository']}:\n\n"
        summary_text += f"- Potential Purpose: {summary['potential_purpose']}\n"
        summary_text += f"- Total Files Found: {summary['total_files']}\n\n"
        summary_text += "File Type Distribution:\n"
        sorted_file_types = sorted(summary['file_types'].items(), key=lambda item: item[1], reverse=True)
        for ext, count in sorted_file_types[:5]:
            summary_text += f"  - {ext}: {count} files\n"

        return jsonify({"summary": summary_text})

    except Exception as e:
        abort(500, description=f"An error occurred while summarizing the repository: {e}")


# --- Route to generate spec for the whole repo ---
@app.route('/generate-repo', methods=['POST'])
def generate_repo_spec():
    data = request.get_json()
    if not data or 'user' not in data:
        abort(400, description="Missing repository info in request.")
    user, repo, branch, path = data['user'], data['repo'], data['branch'], data['path']
    if repo.endswith('.git'):
        repo = repo[:-4]
    try:
        all_files = fetch_repo_contents_recursive(user, repo, branch, path)
        all_items = []
        parsable_extensions = ['.py', '.js', '.html', '.css', '.jsx', '.ts']
        for file_info in all_files:
            if not any(file_info['name'].endswith(ext) for ext in parsable_extensions):
                continue
            try:
                file_response = requests.get(file_info['download_url'], headers=get_github_headers())
                file_response.raise_for_status()
                code = file_response.text
                lang = detect_language(code)
                if lang != 'unknown':
                    items = analyze_code(code, lang)
                    all_items.extend(items)
            except Exception as e:
                print(f"Could not process file {file_info['path']}: {e}")
        title = f"{repo} - API Specification"
        description = f"An auto-generated API specification for the {repo} repository."
        spec = generate_openapi_spec(all_items, title, description)
        spec_yaml = yaml.dump(spec, sort_keys=False)
        return jsonify({"specification": spec_yaml})
    except Exception as e:
        abort(500, description=f"An error occurred while generating the repository spec: {e}")


# --- Language Detection and Parsers ---
def detect_language(code):
    trimmed_code = code.strip()
    if re.search(r"^\s*<!DOCTYPE html>|^\s*<html", trimmed_code, re.IGNORECASE): return 'html'
    if re.search(r"\bimport\s+React\b", trimmed_code) or re.search(r"<[A-Z]", trimmed_code): return 'react'
    if re.search(r"\b(def|class)\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(.*\)\s*:", trimmed_code) or re.search(
            r"^\s*from\s+[\w.]+\s+import\s+[\w*]+", trimmed_code): return 'python'
    if re.search(r"\b(require|exports|module\.exports)\b", trimmed_code): return 'nodejs'
    if re.search(r"^\s*([#.]?[\w-]+)\s*\{[^{}]*:[^;]+;\s*\}", trimmed_code, re.MULTILINE): return 'css'
    if re.search(r"\b(function|const|let|var|=>|for|if)\b", trimmed_code): return 'javascript'
    return 'unknown'


def parse_js_like(code):
    functions = []
    regex = r"(?:function\s+([a-zA-Z0-9_]+)\s*\((.*?)\)|(?:const|let|var)\s+([a-zA-Z0-9_]+)\s*=\s*\((.*?)\)\s*=>|exports\.([a-zA-Z0-9_]+)\s*=|module\.exports\.([a-zA-Z0-9_]+)\s*=)"
    matches = re.finditer(regex, code)
    for match in matches:
        name = next((g for g in [match.group(1), match.group(3), match.group(5), match.group(6)] if g is not None),
                    None)
        args_str = next((g for g in [match.group(2), match.group(4)] if g is not None), '')
        args = [arg.strip() for arg in args_str.split(',') if arg.strip()] if args_str else []
        if name:
            functions.append({"type": "function", "name": name, "args": [{"name": arg, "type": "any"} for arg in args],
                              "docstring": ""})
    return functions


def parse_html(code):
    elements = []
    regex = r"<([a-zA-Z0-9_]+)\s+[^>]*id\s*=\s*[\"']([^\"']+)[\"'][^>]*>"
    matches = re.finditer(regex, code)
    for match in matches:
        elements.append({"type": "html_element", "name": match.group(2), "tag": match.group(1).lower()})
    return elements


def parse_css(code):
    selectors = []
    regex = r"([^{]+)\s*\{"
    matches = re.finditer(regex, code)
    for match in matches:
        raw_selectors = [s.strip() for s in match.group(1).split(',') if s.strip()]
        for selector in raw_selectors:
            if not any(s['name'] == selector for s in selectors):
                selectors.append({"type": "css_selector", "name": selector})
    return selectors


def analyze_python_code(code):
    try:
        tree = ast.parse(code)
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                func_info = {"type": "function", "name": node.name, "args": [], "docstring": ast.get_docstring(node)}
                args_to_process = [arg for arg in node.args.args if arg.arg not in ['self', 'cls']]
                for arg in args_to_process:
                    arg_info = {"name": arg.arg, "type": "any"}
                    if arg.annotation:
                        if isinstance(arg.annotation, ast.Name):
                            arg_info["type"] = arg.annotation.id
                        elif isinstance(arg.annotation, ast.Subscript) and hasattr(arg.annotation.value, 'id'):
                            arg_info["type"] = arg.annotation.value.id
                    func_info["args"].append(arg_info)
                functions.append(func_info)
        return functions
    except SyntaxError:
        return []


def analyze_code(code, language):
    parsers = {'python': analyze_python_code, 'javascript': parse_js_like, 'nodejs': parse_js_like,
               'react': parse_js_like, 'html': parse_html, 'css': parse_css}
    return parsers.get(language, lambda c: [])(code)


def to_openapi_type(lang_type):
    type_map = {"str": "string", "string": "string", "int": "integer", "number": "number", "float": "number",
                "bool": "boolean", "list": "array", "array": "array", "dict": "object", "object": "object"}
    return type_map.get(str(lang_type).lower(), "string")


def generate_openapi_spec(items, title, description):
    spec = {"openapi": "3.0.0", "info": {"title": title, "version": "1.0.0", "description": description},
            "components": {
                "securitySchemes": {"BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}}},
            "security": [{"BearerAuth": []}], "paths": {}}
    standard_responses = {"200": {"description": "Successful Response", "content": {
        "application/json": {"schema": {"type": "object", "example": {"status": "success"}}}}},
                          "404": {"description": "Resource Not Found"}, "500": {"description": "Internal Server Error"}}
    for item in items:
        item_type = item.get("type")
        if item_type == "function":
            path = f"/{item['name']}"
            summary = (item.get('docstring') or f"Endpoint for {item['name']}").split('\n')[0]
            desc = item.get('docstring', "")
            operation = {"summary": summary, "description": desc, "responses": standard_responses}
            if item.get('args'):
                properties = {
                    arg['name']: {"type": to_openapi_type(arg.get('type', 'any')), "example": f"Sample {arg['name']}"}
                    for arg in item['args']}
                required = [arg['name'] for arg in item['args']]
                request_body = {"required": True, "content": {
                    "application/json": {"schema": {"type": "object", "properties": properties, "required": required}}}}
                operation["requestBody"] = request_body
                spec["paths"][path] = {"post": operation}
            else:
                spec["paths"][path] = {"get": operation}
    return spec


# --- OTP Endpoints ---
@app.route('/generate-otp', methods=['GET'])
def generate_otp():
    global current_otp
    current_otp = "".join(random.choices(string.digits, k=6))
    return jsonify({"otp": current_otp})


@app.route('/validate-otp', methods=['POST'])
def validate_otp():
    global current_otp
    data = request.get_json()
    if not data or 'otp' not in data:
        abort(400, description="Missing 'otp' in request body.")
    is_valid = data['otp'] == current_otp
    if is_valid:
        current_otp = None  # Invalidate OTP after use
    return jsonify({"valid": is_valid})


# --- API Generation Endpoint ---
@app.route('/generate', methods=['POST', 'OPTIONS'])
def api_generator():
    if request.method == 'OPTIONS': return '', 204
    request_json = request.get_json()
    if not request_json or 'code' not in request_json: abort(400,
                                                             description="Invalid request: missing 'code' in JSON body.")
    source_code = request_json['code']
    try:
        language = detect_language(source_code)
        if language == 'unknown': abort(400, description="Could not determine the programming language.")
        items = analyze_code(source_code, language)
        spec = generate_openapi_spec(items, "Generated API Specification",
                                     f"API Spec generated from {language.capitalize()} code.")
        spec_yaml = yaml.dump(spec, sort_keys=False)
        return jsonify({"language": language, "specification": spec_yaml})
    except Exception as e:
        abort(500, description=f"An internal error occurred: {e}")


# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)
