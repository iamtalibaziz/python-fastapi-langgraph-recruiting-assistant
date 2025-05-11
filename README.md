# AI Agent: Build a Recruiting Assistant (LangGraph)

Build an autonomous AI recruiting assistant using LangGraph that, given a candidate’s name,
resume, and a job description, performs the following:

* Gathers additional data from the web (e.g., GitHub, blog posts, public mentions)
* Parses and analyzes the candidate's resume.
* Compares candidate qualifications to the job description.
* Returns a structured fit assessment and reasoning

---

## Requirements

Make sure you have Python 3.13 or later installed.

## 🛠️ Setup Instructions

### 1. Clone the repository

git clone https://github.com/iamtalibaziz/python-fastapi-langgraph-recruiting-assistant.git
cd python-fastapi-langgraph-recruiting-assistant

### 2. Create a virtual environment

python -m venv venv

source venv/bin/activate    # For Linux/macOS
venv\Scripts\activate       # For Windows

### 3. Install dependencies

pip install -r requirements.txt

### 4. Environment Variables

Copy the example environment file and rename it to .env:

cp .env.example .env  # For Linux/macOS
copy .env.example .env  # For Windows

Open .env and update the values as needed (e.g., OPENAI_API_KEY, etc.).


### 5. Run the app
uvicorn app.main:app --reload


Access the app at: http://127.0.0.1:8000
Swagger UI: http://127.0.0.1:8000/docs


