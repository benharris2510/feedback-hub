# CLAUDE.md - Feedback Hub Project Documentation

This file contains essential information for future Claude Code instances working on this project. It focuses on high-level architecture and patterns requiring multiple files to understand.

## Project Overview

The Feedback Hub is a full-stack MVP for user feedback management with forums and developer integration. Built with Nuxt 4 frontend and Flask-RESTX backend, featuring JWT authentication, real-time forum discussions, and modern Linear-inspired UI design.

## Architecture Overview

### Backend Structure (Flask-RESTX)
- **Framework**: Flask with Flask-RESTX for auto API documentation
- **Database**: SQLite with SQLAlchemy ORM (production can use PostgreSQL)
- **Authentication**: JWT tokens using Flask-JWT-Extended
- **API Design**: RESTful endpoints with automatic Swagger documentation

Key backend files:
- `backend/app/api/auth.py` - Authentication endpoints (login/register/refresh)
- `backend/app/models/` - SQLAlchemy models for User, Forum, Post, Feedback
- `backend/app/config.py` - Environment-based configuration
- `backend/dummy_data.py` - Sample data generation script

### Frontend Structure (Nuxt 4)
- **Framework**: Nuxt 4 with Vue 3 Composition API
- **State Management**: Pinia stores for auth and API data
- **Styling**: Tailwind CSS with custom design system
- **Testing**: Vitest for unit tests, ESLint for code quality

Key frontend patterns:
- `frontend/composables/useApi.js` - Centralized API client with JWT handling
- `frontend/stores/auth.js` - Authentication state management
- `frontend/middleware/auth.js` - Route protection
- `frontend/layouts/default.vue` - Main application layout with sidebar navigation

## Development Commands

### Backend (from backend/ directory)
```bash
# Start development server
python run.py

# Generate dummy data
python dummy_data.py

# Run tests
python -m pytest tests/ -v

# Install dependencies
pip install -r requirements.txt
```

### Frontend (from frontend/ directory)
```bash
# Development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Linting (must pass with 0 errors)
npm run lint

# Type checking
npm run typecheck

# Install dependencies (use legacy peer deps for Nuxt 4)
npm install --legacy-peer-deps
```

## Key Architectural Decisions

### Authentication Flow
- JWT access/refresh token pattern implemented across both frontend and backend
- Frontend stores tokens in Pinia store (not localStorage for security)
- API composable automatically handles token refresh and request retries
- Protected routes use middleware to check authentication status

### API Communication
- Centralized API client in `useApi()` composable handles all HTTP requests
- Automatic JWT token attachment and refresh logic
- Error handling with user-friendly messages
- Base URL configuration in `nuxt.config.ts` for environment flexibility

### Database Design
- Users table with bcrypt password hashing
- Forums contain multiple Posts, Posts have Replies
- Feedback items separate from forum system
- Timestamps and soft deletes implemented consistently

### UI Design System
- Linear-inspired dark theme with glassmorphism effects
- Custom CSS variables for consistent gradients and shadows
- Tailwind configuration extends colors with primary/secondary palettes
- Component classes for buttons, inputs, cards with hover animations

## Critical Technical Context

### Port Configuration
- Backend runs on port 5001 (not 5000 due to macOS AirPlay conflicts)
- Frontend development server on port 3000
- Update both `backend/run.py` and `frontend/nuxt.config.ts` if changing ports

### Database Switching
- Currently uses SQLite for development simplicity
- PostgreSQL configuration available in `backend/app/config.py`
- Update `DATABASE_URL` environment variable to switch databases

### ESLint Configuration
- Uses flat config system (`.cjs` file) for ESLint 8.57
- Configured for Nuxt 4 with TypeScript and Vue support
- Must maintain 0 errors policy (warnings acceptable)
- Ignores `.nuxt/` and `.output/` generated directories

### Known Issues & Fixes
- **JWT Login Error**: Never use `get_jwt_identity()` in login endpoints before token creation
- **CSS Import Errors**: Always place `@import` statements at top of CSS files
- **Vue Composition Errors**: Use computed properties instead of functions for reactive template values
- **Dependency Conflicts**: Use `--legacy-peer-deps` flag for npm install with Nuxt 4

## Security Considerations

### Authentication Security
- Passwords hashed with bcrypt (12 rounds)
- JWT tokens have short expiration times with refresh mechanism
- No sensitive data stored in frontend localStorage
- CORS properly configured for cross-origin requests

### API Security
- All endpoints require authentication except public forum viewing
- Input validation on all forms and API endpoints
- No secrets or keys committed to repository
- Environment variables for all sensitive configuration

## Testing Strategy

### Backend Testing
- Unit tests for all API endpoints using pytest
- Database fixtures for consistent test data
- Authentication flow testing with JWT tokens
- Error handling verification

### Frontend Testing
- Component testing with Vue Test Utils
- Store testing for Pinia state management
- Integration tests for authentication flow
- ESLint enforcement for code quality

## Deployment Notes

### Environment Variables Required
```
# Backend
DATABASE_URL=sqlite:///feedback_hub.db  # or PostgreSQL URL
JWT_SECRET_KEY=your-secret-key-here
FLASK_ENV=development  # or production

# Frontend (in .env)
NUXT_API_BASE_URL=http://localhost:5001  # Backend URL
```

### Production Considerations
- Switch to PostgreSQL for production database
- Use proper JWT secret key (not hardcoded)
- Enable HTTPS for all communications
- Configure proper CORS origins for production domains
- Build frontend with `npm run build` and serve static files

## Common Development Patterns

### Adding New API Endpoints
1. Create route in appropriate `backend/app/api/` file
2. Add corresponding model in `backend/app/models/` if needed
3. Update frontend API calls in components or stores
4. Add tests for both backend endpoint and frontend integration

### Adding New Frontend Pages
1. Create page component in `frontend/pages/` directory
2. Add to navigation in `frontend/layouts/default.vue` if needed
3. Implement API calls using `useApi()` composable
4. Add appropriate authentication middleware if required
5. Update page titles and meta tags using `useHead()`

### Authentication Pattern
Always use the established pattern for protected operations:
```typescript
// Frontend component
const authStore = useAuthStore()
const api = useApi()

// Check authentication
if (!authStore.isAuthenticated) {
  // Handle unauthenticated state
}

// Make authenticated API call
const data = await api('/protected-endpoint', {
  method: 'POST',
  body: payload
})
```

This documentation should provide sufficient context for future Claude instances to understand the project architecture and continue development effectively.