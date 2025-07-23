# Feedback Hub - Claude Code Documentation

## Project Overview
Feedback Hub is a comprehensive user feedback and forum platform that enables businesses to collect, manage, and respond to customer feedback. It combines public forums for community discussions with structured feedback collection, all in one paid SaaS platform.

## Architecture
- **Frontend**: Nuxt 3 + Vue 3 + TypeScript in `/frontend/` folder
- **Backend**: Python Flask-RESTX + SQLAlchemy in `/backend/` folder
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT-based authentication with Flask-JWT-Extended
- **Testing**: Vitest for frontend, pytest for backend

## Key Features
1. **Public Forums**: Community-driven discussion boards
2. **User Feedback**: Structured feedback collection and management
3. **Authentication**: Secure login and registration system
4. **Developer Integration**: API access for programmatic feedback submission
5. **Multi-tenant**: Support for multiple organizations/products

## Common Commands

### Frontend Development (from `/frontend/`)
```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Lint code
npm run lint

# Type check
npm run typecheck
```

### Backend Development (from `/backend/`)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python run.py

# Run tests
pytest

# Run tests with coverage
pytest --cov=app

# Database migrations
flask db init
flask db migrate -m "Migration message"
flask db upgrade

# Generate dummy data
python scripts/generate_dummy_data.py

# Run linting
flake8 app/
black app/
```

## API Structure

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh JWT token
- `GET /api/auth/profile` - Get current user profile

### Forum Endpoints
- `GET /api/forums` - List all forums (public)
- `GET /api/forums/:id` - Get specific forum (public)
- `GET /api/forums/:id/posts` - List posts in forum (public)
- `POST /api/forums/:id/posts` - Create new post (authenticated)
- `GET /api/posts/:id` - Get specific post with replies (public)
- `POST /api/posts/:id/replies` - Reply to post (authenticated)

### Feedback Endpoints
- `GET /api/feedback` - List feedback (public with filters)
- `GET /api/feedback/:id` - Get specific feedback (public)
- `POST /api/feedback` - Submit feedback (authenticated or API key)
- `PUT /api/feedback/:id/status` - Update feedback status (admin)

### Developer API
- `POST /api/developer/api-keys` - Generate API key
- `GET /api/developer/api-keys` - List API keys
- `DELETE /api/developer/api-keys/:id` - Revoke API key

## Database Schema

### Core Models
- **User**: id, email, username, password_hash, created_at, is_admin
- **Forum**: id, name, description, slug, is_public, created_at
- **ForumPost**: id, forum_id, user_id, title, content, created_at, updated_at
- **PostReply**: id, post_id, user_id, content, created_at
- **Feedback**: id, user_id, title, description, status, type, priority, created_at
- **ApiKey**: id, user_id, key, name, is_active, created_at

## Frontend Architecture

### Pages Structure
- `/` - Landing page showcasing platform features
- `/forums` - Public forum listing
- `/forums/:slug` - Individual forum with posts
- `/forums/:slug/:postId` - Individual post with replies
- `/feedback` - Public feedback listing
- `/feedback/:id` - Individual feedback detail
- `/login` - User login page
- `/register` - User registration page
- `/dashboard` - Authenticated user dashboard
- `/dashboard/settings` - User settings and API keys

### State Management (Pinia)
- **auth.ts** - Authentication state and user session
- **forums.ts** - Forum and post data
- **feedback.ts** - Feedback data and filters
- **api.ts** - API client configuration

### Key Components
- **ForumCard.vue** - Forum listing item
- **PostCard.vue** - Post listing item
- **FeedbackCard.vue** - Feedback listing item
- **AuthForm.vue** - Reusable authentication form
- **Navigation.vue** - Main navigation with auth state
- **FeedbackForm.vue** - Feedback submission form

## Security Considerations

1. **Authentication**: JWT tokens with refresh mechanism
2. **Authorization**: Role-based access control (user/admin)
3. **API Keys**: For developer integration with rate limiting
4. **CORS**: Configured for frontend-backend communication
5. **Input Validation**: Both frontend and backend validation
6. **SQL Injection**: Protected via SQLAlchemy ORM
7. **Password Security**: Bcrypt hashing with salt

## Testing Strategy

### Frontend Tests
- Component unit tests with Vue Test Utils
- Page integration tests
- Store tests for Pinia stores
- E2E tests for critical user flows

### Backend Tests
- Unit tests for all services
- Integration tests for API endpoints
- Database tests with test fixtures
- Authentication flow tests

## Development Workflow

1. **Backend First**: Implement API endpoints and test
2. **Frontend Integration**: Connect UI to APIs
3. **Test Coverage**: Maintain >80% test coverage
4. **Documentation**: Update API docs with Flask-RESTX

## Environment Variables

### Frontend (.env)
```
NUXT_PUBLIC_API_URL=http://localhost:5000/api
```

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost/feedback_hub
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
FLASK_ENV=development
```

## Deployment Considerations

1. **Frontend**: Can be deployed to Vercel, Netlify, or any static host
2. **Backend**: Deployable to Heroku, AWS, or any Python host
3. **Database**: PostgreSQL on AWS RDS, Heroku Postgres, etc.
4. **Environment**: Separate staging and production environments

## Future Enhancements

1. **Real-time Updates**: WebSocket support for live notifications
2. **Email Notifications**: Email alerts for feedback responses
3. **Analytics Dashboard**: Insights on feedback trends
4. **Webhook Integration**: Allow developers to receive feedback via webhooks
5. **Multi-language Support**: i18n for global usage
6. **Mobile Apps**: React Native companion apps