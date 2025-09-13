# 📄 Smart Resume Analyzer

The **Smart Resume Analyzer** is a full-stack web application built with **React** and **FastAPI** that leverages the power of **Large Language Models (LLMs)** to provide instant, AI-powered feedback on resumes.  

---

## ✨ Features

- **Drag & Drop PDF Upload**: A modern, user-friendly interface to upload resumes in PDF format.  
- **AI-Powered Analysis**:  
  - Extracts structured data like contact information, skills, and work experience.  
  - Provides a quantitative rating for the resume.  
  - Offers actionable advice for improvement.  
  - Suggests relevant skills to enhance the user's profile.  
- **Submission History**: Browse previously analyzed resumes and view their detailed reports.  

---

## 🛠️ Tech Stack

- **Frontend**: React.js  
- **Backend**: FastAPI (Python)  
- **Database**: SQLite  
- **LLM**: Gemini  
- **Deployment**:  
  - Frontend → [Vercel](https://resume-analyzer-using-fast-api.vercel.app/)  
  - Backend → [Render](https://resume-analyzer-backend-9v7v.onrender.com)  

---

## 🚀 Local Setup and Installation

### ✅ Prerequisites
- Python **3.9+**  
- Node.js **v16+**  
- A valid **`GEMINI_API_KEY`**

---

### 🔧 Backend Setup

```bash
# Navigate to backend folder
cd backend

# Create a virtual environment and activate it
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Run the backend server
uvicorn app.main:app --reload
```

---

### 🎨 Frontend Setup

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Start the frontend app
npm start
```

---

## 🔑 Environment Variables

### Backend (`backend/.env`)
```env
GEMINI_API_KEY=your_api_key_here
```

### Frontend (`frontend/.env`)
```env
REACT_APP_API_BASE_URL=http://127.0.0.1:8000/api
```

---

## 📖 API Endpoints

- `POST /api/upload` → Uploads and analyzes a resume.  
- `GET /api/resumes` → Retrieves a list of all analyzed resumes.  
- `GET /api/resumes/{resume_id}` → Fetches the detailed analysis for a specific resume.  
- `DELETE /api/resumes/{resume_id}` → Deletes a resume from the history.  

---

## 🌐 Live Demo

- **Frontend** → [Smart Resume Analyzer (Vercel)](https://resume-analyzer-using-fast-api.vercel.app/)  
- **Backend API** → [Smart Resume Analyzer API (Render)](https://resume-analyzer-backend-9v7v.onrender.com)  

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repo and submit pull requests.  

---

## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.  
