# Feedback Hub - Login Credentials

## Test Accounts

### Admin Account
- **Email**: `admin@feedbackhub.com`
- **Password**: `admin123`
- **Permissions**: Full admin access, can manage forums, moderate content, update feedback status

### Regular User Accounts
- **Email**: `user1@example.com` through `user5@example.com`
- **Password**: `password123`
- **Permissions**: Can create posts, reply to discussions, submit feedback

## Server Information

### Backend API
- **URL**: http://localhost:5001
- **API Documentation**: http://localhost:5001/api/docs
- **Database**: SQLite (`feedback_hub_dev.db`)

### Frontend Application
- **URL**: http://localhost:3000
- **Framework**: Nuxt 3 + Vue 3 + Tailwind CSS

## Setup Instructions

1. **Backend Setup**:
   ```bash
   cd backend
   python3 -m pip install -r requirements.txt
   python3 scripts/generate_dummy_data.py  # Run once to populate database
   python3 run.py  # Starts server on port 5001
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install --legacy-peer-deps
   npm run dev  # Starts server on port 3000
   ```

## Database Schema

The system includes:
- **6 Users** (1 admin + 5 regular users)
- **4 Forums** (General Discussion, Feature Requests, Bug Reports, Developer Corner)
- **10 Forum Posts** with various replies
- **8 Feedback Items** with different statuses and types

## API Endpoints

- `POST /api/auth/login` - User authentication
- `GET /api/forums` - List public forums
- `GET /api/feedback` - List public feedback
- `POST /api/feedback` - Submit new feedback
- And many more documented at `/api/docs`