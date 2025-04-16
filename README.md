# sprint-CS5500

## Project: Backend Public Access Deployment + CI/CD Automation via GitHub Actions & Docker

### User Story
As a user, I want to access the backend application from a publicly available endpoint so that I can test the various features of the application using Swagger UI.  
As a developer, I want to automate the deployment of the backend application to the public endpoint so that my team can easily and quickly make new releases.

---

### Acceptance Criteria
- Backend is deployed to a cloud platform (e.g. AWS EC2).
- Public access to the API documentation via Swagger UI.
- README includes step-by-step instructions for accessing the API and running the application.
- Authentication and special access requirements are clearly documented.
- Deployment process is automated using GitHub Actions and Docker.

---

## 🔗 Public Endpoint

The backend API is live and accessible via Swagger UI:

- **Swagger UI:**  
  [http://ec2-54-202-247-139.us-west-2.compute.amazonaws.com:8000/docs](http://ec2-54-202-247-139.us-west-2.compute.amazonaws.com:8000/docs)

> This page allows you to explore and test all available API endpoints interactively.

---

## 📘 How to Use Swagger

1. Open the link above in your browser.
2. Expand an endpoint group (e.g. `/authentication`, `/user`) to view individual APIs.
3. Click **"Try it out"** on any endpoint.
4. Fill in any required parameters (if applicable), then click **"Execute"**.
5. View the real-time response from the server directly below the endpoint.

> 🔐 For endpoints requiring authorization:
> - Use the `/auth/token` endpoint to retrieve a token.
> - Click the 🔒 "Authorize" button at the top right of Swagger UI.
> - Enter your token as: `Bearer <your_token>`

---

## ☁️ Step-by-Step AWS Deployment Instructions

This guide explains how to deploy the backend to an AWS EC2 instance manually.

### ✅ Prerequisites
- An AWS account and an EC2 instance (Amazon Linux 2 or Ubuntu recommended)
- Security group allows inbound traffic on **port 8000**
- A `.pem` SSH key file (e.g., `cs5500.pem`)
- Git installed locally

### 🔧 Deployment Steps

#### 1. Connect to your EC2 instance
```bash
chmod 400 cs5500.pem
ssh -i cs5500.pem ec2-user@54.202.247.139
```

#### 2. Install necessary packages
```bash
sudo yum update -y
sudo yum install git python3 -y
```

#### 3. Clone the GitHub repository
```bash
git clone https://github.com/YukkiXu213/sprint-CS5500.git
cd sprint-CS5500/CommonAssessmentTool
```

#### 4. (Optional) Create a Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 5. Install dependencies
```bash
pip install -r requirements.txt
```

#### 6. Run the FastAPI app
```bash
uvicorn CommonAssessmentTool.main:app --host 0.0.0.0 --port 8000
```

> 🎯 You should now be able to access the API at  
> [http://<your-ec2-ip>:8000/docs](http://<your-ec2-ip>:8000/docs)

---

## 🔐 Authentication

Some endpoints are protected and require a Bearer Token:

1. Use the `/auth/token` endpoint to login with a valid username and password.
2. Copy the access token from the response.
3. In Swagger, click the **Authorize** button and paste:
   ```
   Bearer <your_access_token>
   ```

---

## 🔄 CI/CD Pipeline (GitHub Actions)

### 🚀 What It Does

The deployment is automated via GitHub Actions when a new Release is published from the `main` branch:

- ✅ Build Docker image
- ✅ Push to Docker Hub
- ✅ SSH into EC2 server using `appleboy/ssh-action`
- ✅ Pull latest image and restart container

### 📁 File Used
- `.github/workflows/release.yml`

### 🔐 Required GitHub Secrets
| Name              | Description                          |
|-------------------|--------------------------------------|
| `DOCKER_USERNAME` | Your Docker Hub username             |
| `DOCKER_PASSWORD` | Your Docker Hub password/token       |
| `REMOTE_HOST`     | EC2 public IP                        |
| `REMOTE_USER`     | Usually `ec2-user`                   |
| `REMOTE_KEY`      | SSH private key content (`.pem`)     |

---

## 🐳 Running with Docker Locally

### 1. Build and run manually:
```bash
docker build -t sprint3-backend .
docker run -p 8000:8000 sprint3-backend
```

### 2. Or use Docker Compose:
```bash
docker-compose up --build
```

> Access Swagger UI at: [http://localhost:8000/docs](http://localhost:8000/docs)

To stop:
```bash
docker-compose down
```

---

## ✅ Definition of Done

- [x] Public Swagger endpoint documented
- [x] Usage instructions provided
- [x] AWS deployment steps clearly explained
- [x] Authentication requirements covered
- [x] Docker + GitHub Actions-based CI/CD setup documented