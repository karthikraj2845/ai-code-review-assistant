# AI Code Review Assistant

A full-stack, responsive web application that provides AI-powered code analysis, bug detection, optimization suggestions, and step-by-step code explanations using the Gemini API.

---

## 🚀 Tech Stack

### **Frontend**
*   **React.js** (v18.2.0) - High-performance UI library.
*   **Vite** - High-speed frontend build and development tool.
*   **Tailwind CSS** - Modern utility-first CSS framework for responsive, dark-mode-ready styling.
*   **Axios** - Promise-based HTTP client for API integrations.

### **Backend**
*   **FastAPI** - High-performance, modern web framework for building APIs with Python.
*   **Uvicorn** - Lightning-fast ASGI web server implementation.
*   **Pydantic** (v2.8.0+) - Fast, standard data validation and settings management.
*   **Python Dotenv** - Easy environment configuration management.
*   **Google Generative AI** / **Custom Mock Service** - Live Gemini API integration with a simulated fallback engine.

---

## 🛠️ Our Rectification Approach

When taking over the project, we identified and resolved several critical errors preventing the application from compiling and running:

1.  **Vite Compatibility (ReferenceError Fix)**: The original code used `process.env.REACT_APP_` syntax, which Vite does not support at runtime, causing a complete crash. We migrated the environment configuration to standard Vite format (`import.meta.env.VITE_API_BASE_URL` and `VITE_` prefixes).
2.  **Broken CSS Import Resolution**: The compiler was throwing a build-blocking `import './App.css' Failed to resolve` error. Because all styling uses Tailwind CSS directly, we removed this broken import statement from `App.jsx`.
3.  **Missing Node dependencies**: Added `axios` directly to the `dependencies` block in `package.json` to enable robust backend API communication.
4.  **Modern Python 3.13 Compatibility**: The original pinned version of Pydantic (`2.5.0`) failed to install on Windows machines with Python 3.13 due to obsolete Rust dependencies trying to build from source. We relaxed these requirements to `>=2.8.0` and `>=0.109.0` to pull precompiled binary wheels directly.
5.  **Robust Demo/Mock Fallback Mode**: To ensure the project runs flawlessly even without an active Google AI Studio API key, we built a server-side **Demo/Mock Mode** directly inside `GeminiService`. It analyzes the code syntactically and generates highly realistic mock reports (catching Python default mutable parameters, loose JS comparisons, time/space complexities, etc.) and seamlessly transitions to live Gemini AI once a key is added.

---

## 💻 Setup and Run Instructions

### **Prerequisites**
*   **Node.js** (v16+)
*   **Python** (v3.8+)
*   **Gemini API Key** (Optional, get one from [Google AI Studio](https://makersuite.google.com/app/apikey))

---

### **Option 1: The 1-Second Automated Quick Launcher (Recommended)**

A PowerShell startup script is provided in the root folder that automatically initializes dependencies, boots both servers, and opens the browser for you.

1.  Open **PowerShell** and navigate to the project root:
    ```powershell
    cd c:\Projects\ai-code-review-assistant
    ```
2.  Launch the script:
    ```powershell
    .\start.ps1
    ```
    *This will boot everything automatically and launch the app in your browser!*

---

### **Option 2: Manual Startup**

If you prefer to run the components in separate terminal windows, follow these instructions:

#### **1. Backend Setup & Startup (FastAPI)**
1.  Open a terminal and go to the `backend` folder:
    ```bash
    cd backend
    ```
2.  Create and activate a virtual environment:
    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  *(Optional)* Add your Gemini API key in `.env`:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```
    *If left as placeholder, the server automatically starts in custom Demo/Mock mode.*
5.  Start the FastAPI server:
    ```bash
    python -m uvicorn main:app --host 127.0.0.1 --port 8000
    ```
    *Backend API live at `http://127.0.0.1:8000`*

#### **2. Frontend Setup & Startup (Vite / React)**
1.  Open a second terminal and go to the `frontend` folder:
    ```bash
    cd frontend
    ```
2.  Install packages:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
    *Frontend React application live at `http://localhost:5173` (or `5174` if `5173` is busy)*

---

## 🧪 Testing the API
To test if the backend API is working correctly without the frontend, you can run this quick PowerShell command:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/review -Method Post -Body '{"code": "def my_func(a):\n  for i in range(len(a)):\n    print(a[i])", "language": "python"}' -ContentType "application/json" | ConvertTo-Json -Depth 5
```