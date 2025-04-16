# Team TicTech

## Project: Feature Development Backend - Create CRUD APIs for Clients + ML Prediction API

### User Story
As a user of the backend APIs, I want to call APIs that can retrieve, update, and delete information of clients who have already registered with the CaseManagement service so that I can more efficiently help previous clients make better decisions on how to be gainfully employed.

---

### Acceptance Criteria
- Provide REST API endpoints so that the frontend can use them to interact with client data.
- Document how to use the REST API.
- Create a database schema and connect to it.
- Add automated tests.
- Implement a machine learning prediction API based on client data.

---

### Machine Learning Model Description
This backend includes machine learning models that predict a client’s baseline success score and the effectiveness of different interventions on their employability.

The models use dummy training data and return predictions based on user-inputted client attributes. The system can:
- Predict baseline success likelihood.
- Simulate success scores after interventions.
- Identify which interventions have the highest potential benefit.

Models include:
- Logistic Regression
- Random Forest
- Neural Network

---

## 🚀 How to Run the Backend

### 1. 🔧 Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload

# Load initial dummy data into the database
python initialize_data.py
```

### 2. 🔗 Access API
- Visit Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Login with:
  - Username: `admin`
  - Password: `admin123`

---

## 🔌 API Endpoints
### 👤 User & Authentication
- `POST /users`: Create user (admin only, role = "admin" or "case_worker")
- `POST /auth/token`: Login to get access token

### 📁 Client Operations
- `GET /clients`: List all clients
- `GET /clients/{client_id}`: Get a single client by ID
- `PUT /clients/{client_id}`: Update client information
- `DELETE /clients/{client_id}`: Delete a client by ID

### 🔍 Filtering Clients
- `GET /clients/search/by-criteria`: Filter clients by demographic/work/education data
- `GET /clients/search/by-services`: Filter by service statuses
- `GET /clients/search/success-rate`: Filter by success rate thresholds

### 📋 Client Services
- `GET /clients/{client_id}/services`: View service statuses for a client
- `PUT /clients/{client_id}/services/{user_id}`: Update services assigned to a client
- `POST /clients/{client_id}/case-assignment`: Assign a case worker to a client
- `GET /clients/case-worker/{case_worker_id}`: Get clients assigned to a case worker

### 🧠 Machine Learning Prediction
- `GET /ml/models`: List all available ML models
- `GET /ml/model/current`: View currently selected model
- `POST /ml/model/switch`: Switch current ML model
- `POST /clients/predictions`: Predict client success score and intervention outcomes

---

## 🐳 Running with Docker (Recommended)

### Requirements:
- Docker
- Docker Compose (optional but recommended)

### Option 1: Docker Only
```bash
docker build -t case-management-api .
docker run -p 8000:8000 case-management-api
```

### Option 2: Docker Compose
```bash
docker-compose up --build
```

> Swagger UI will be available at [http://localhost:8000/docs](http://localhost:8000/docs)

To stop:
```bash
docker-compose down
```

---

## 🔄 CI/CD Pipeline
GitHub Actions (`.github/workflows/ci.yml`) runs on:
- Push to `main`
- Pull Requests to `main`

### Pipeline Tasks:
1. **Lint & Code Style Checks** – Black, Flake8, isort, MyPy
2. **Testing** – Runs pytest
3. **Docker Build & Smoke Test** – Validates Docker image and runs it

### ☁️ Public Cloud Deployment

The backend is also deployed on an AWS EC2 instance:

🔗 **Swagger UI:** [http://ec2-54-202-247-139.us-west-2.compute.amazonaws.com:8000/docs](http://ec2-54-202-247-139.us-west-2.compute.amazonaws.com:8000/docs)

🧪 Test Credentials:
- Username: `admin`
- Password: `admin123`

## 🔄 CI/CD Pipeline

Our GitHub Actions workflow is defined in `.github/workflows/ci-cd.yml`.

### Triggers:
- Push to `main`
- Pull Requests to `main`
- **GitHub Release**: When a release is published from `main`, the app is auto-deployed to the cloud server.

### Pipeline Tasks:
1. ✅ **Lint & Code Style Checks** – Black, Flake8, MyPy
2. ✅ **Testing** – Runs all unit tests with Pytest
3. ✅ **Docker Build & Smoke Test** – Validates Docker image and runs a local container
4. ✅ **Deployment to AWS EC2** – Executes `deploy.sh` to copy code and restart container on the cloud

> Deployment is secured via SSH key stored in GitHub Secrets.
---
