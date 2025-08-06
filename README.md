# ML Experiments Tracker - Campus Assessment

A full-stack web application for tracking machine learning experiments, built as part of a campus assessment to demonstrate programming, reasoning, and documentation skills.

## 🎯 Project Overview

**CRUD Object:** ML Experiment  
**Tech Stack:** Python Flask + SQLite + HTML/CSS/JavaScript  
**Deployment:** Vercel-ready  

## 📋 Features

### ✅ Core Functionality
- **User Authentication:** Simple login system
- **CRUD Operations:** Create, Read, Update, Delete ML experiments
- **Advanced Filtering:** Filter by model type, status, and public/private
- **Pagination:** 5 experiments per page
- **Search:** Real-time search across experiment titles and descriptions

### 🧪 ML Experiment Schema
- **Experiment ID** (auto-generated)
- **Title** (text input) - Required
- **Description** (text area) - Required
- **Model Type** (dropdown) - CNN, RNN, Transformer, LSTM, BERT, Custom
- **Status** (dropdown) - Planning, Running, Completed, Failed
- **Accuracy** (number input, 0-100) - Optional
- **Is Public** (boolean checkbox)
- **Created Date** (auto-generated)
- **Last Updated** (auto-generated)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd Shipsy

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run the application
python app.py
```

### Access the Application
- **Local:** http://localhost:5000
- **Default Login:** admin / password123

## 📁 Project Structure

```
Shipsy/
├── app.py                 # Main Flask application
├── init_db.py            # Database initialization
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── static/              # Static files (CSS, JS)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/           # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── experiment_form.html
│   └── experiment_detail.html
├── tests/              # Test files
│   ├── test_app.py
│   └── test_models.py
├── docs/               # Documentation
│   ├── schema_design.md
│   ├── module_structure.md
│   ├── ai_prompts.md
│   ├── test_plan.md
│   └── reflection.md
└── vercel.json         # Vercel deployment config
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

## 📊 Database Schema

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    model_type TEXT NOT NULL,
    status TEXT NOT NULL,
    accuracy REAL,
    is_public BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 Deployment

### Vercel Deployment
1. Push code to GitHub
2. Connect repository to Vercel
3. Deploy automatically

### Environment Variables
- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: Database connection string

## 📝 Documentation

- [Schema Design](docs/schema_design.md)
- [Module Structure](docs/module_structure.md)
- [AI Prompts Used](docs/ai_prompts.md)
- [Test Plan](docs/test_plan.md)
- [Reflection](docs/reflection.md)

## 🎨 UI/UX Features

- **Responsive Design:** Works on desktop and mobile
- **Modern Interface:** Clean, professional look
- **User Feedback:** Success/error messages
- **Loading States:** Smooth user experience
- **Form Validation:** Client and server-side validation

## 🔒 Security Features

- **Password Hashing:** Secure password storage
- **Session Management:** Flask sessions
- **Input Validation:** SQL injection prevention
- **CSRF Protection:** Form security

## 📈 Performance

- **Database Indexing:** Optimized queries
- **Pagination:** Efficient data loading
- **Caching:** Static asset optimization
- **Minimal Dependencies:** Lightweight application

---

**Built with ❤️ for Campus Assessment** 


# Submission Appendix: Campus Assessment

## Table of Contents
1. [Deployed App Link](#1-deployed-app-link)
2. [Schema Design](#2-schema-design)
3. [Module & Class Structure](#3-module--class-structure)
4. [AI Prompts Used](#4-ai-prompts-used)
5. [Test Plan](#5-test-plan)
6. [Reflection](#6-reflection)

---

## 1. Deployed App Link

**Live App:** [https://shipsy-webpage.vercel.app/](https://shipsy-webpage.vercel.app/)

---

## 2. Schema Design

### Database Schema Design

#### Overview

The ML Experiments Tracker uses SQLite as its database with two main tables: `users` and `experiments`. The schema is designed to be simple yet comprehensive, supporting all CRUD operations with proper relationships and constraints.

#### Database Schema

**Users Table**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
- `id`: Primary key, auto-incrementing integer
- `username`: Unique username for login (max 50 characters)
- `password_hash`: SHA-256 hashed password for security
- `created_at`: Timestamp when user was created

**Constraints:**
- Username must be unique
- Username and password cannot be null
- Password is stored as hash, never plain text

**Experiments Table**
```sql
CREATE TABLE experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    model_type TEXT NOT NULL,
    status TEXT NOT NULL,
    accuracy REAL,
    is_public BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
- `id`: Primary key, auto-incrementing integer
- `title`: Experiment title (required, max 200 characters)
- `description`: Detailed experiment description (required, unlimited text)
- `model_type`: Type of ML model (required, enum values)
- `status`: Current experiment status (required, enum values)
- `accuracy`: Model accuracy percentage (optional, 0-100)
- `is_public`: Visibility flag (default: private)
- `created_at`: Timestamp when experiment was created
- `updated_at`: Timestamp when experiment was last updated

**Constraints:**
- Title and description cannot be null
- Model type must be from predefined list
- Status must be from predefined list
- Accuracy must be between 0 and 100 (if provided)
- Updated timestamp is automatically managed

#### Enumerated Values

**Model Types**
- `CNN` - Convolutional Neural Network
- `RNN` - Recurrent Neural Network
- `Transformer` - Transformer Architecture
- `LSTM` - Long Short-Term Memory
- `BERT` - Bidirectional Encoder Representations from Transformers
- `Custom` - Custom/Other model types

**Status Values**
- `Planning` - Experiment is in planning phase
- `Running` - Experiment is currently running
- `Completed` - Experiment has finished successfully
- `Failed` - Experiment failed or was cancelled

#### Indexes

```sql
CREATE INDEX idx_experiments_status ON experiments(status);
CREATE INDEX idx_experiments_model_type ON experiments(model_type);
CREATE INDEX idx_experiments_is_public ON experiments(is_public);
```
- Fast filtering by experiment status, model type, and visibility

#### Data Relationships

- One user can have many experiments
- Each experiment belongs to one user (implied through session management)
- User authentication is handled through Flask sessions (no foreign key constraints needed)

#### Data Validation Rules

- Username: 3-50 characters, alphanumeric and underscores only
- Password: Minimum 8 characters, stored as SHA-256 hash
- Title: 1-200 characters, required
- Description: 1-unlimited characters, required
- Model Type: Must be from predefined list
- Status: Must be from predefined list
- Accuracy: 0-100, optional, numeric only
- Is Public: Boolean (0 or 1)

#### Security Considerations

- Passwords are hashed using SHA-256
- No plain text passwords stored
- All user inputs are parameterized
- No direct string concatenation in SQL queries
- Input validation on both client and server side
- HTML entities are escaped in templates
- XSS prevention through proper output encoding
- Input length limits to prevent DoS attacks

#### Performance Considerations

- Indexes on frequently filtered columns
- Pagination to limit result sets
- Efficient WHERE clauses
- Appropriate field types (INTEGER vs TEXT)
- Indexes only on necessary columns
- Regular database maintenance

#### Migration Strategy

- Database schema is versioned
- Migration scripts for future updates
- Backward compatibility maintained
- Regular database backups recommended
- Export functionality for data portability

#### Future Enhancements

- User roles and permissions
- Experiment categories/tags
- File attachments for experiment data
- Experiment sharing and collaboration
- Audit trail for changes
- Advanced search and filtering
- Database connection pooling
- Caching layer for frequently accessed data
- Horizontal scaling with read replicas
- Microservices architecture for large scale

---

## 3. Module & Class Structure

### Overview

The ML Experiments Tracker follows a modular architecture with clear separation of concerns. The application is structured into logical modules that handle specific functionality while maintaining loose coupling.

### Project Structure

```
Shipsy/
├── app.py                 # Main Flask application
├── models.py              # Database models and business logic
├── requirements.txt       # Python dependencies
├── static/                # Static assets
│   ├── css/style.css      # Custom styles
│   └── js/main.js         # Client-side JavaScript
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── login.html         # Login page
│   ├── dashboard.html     # Dashboard page
│   ├── experiment_form.html  # Create/Edit form
│   └── experiment_detail.html # Experiment detail view
├── tests/                 # Test files
│   └── test_app.py        # Application tests
└── docs/                  # Documentation
    ├── schema_design.md
    ├── module_structure.md
    ├── ai_prompts.md
    ├── test_plan.md
    └── reflection.md
```

### Core Modules

#### 1. Main Application (`app.py`)
- Flask app initialization
- Route definitions for all endpoints
- Authentication middleware
- Error handlers

#### 2. Database Models (`models.py`)
- Database connection management
- User authentication logic
- Experiment CRUD operations
- Data validation

#### Main Classes (Pseudocode)
```python
class DatabaseManager:
    def __init__(self, db_path: str = "experiments.db"):
        ...
    def get_connection(self):
        ...
    def init_database(self):
        ...

class User:
    def __init__(self, db_manager: DatabaseManager):
        ...
    def create_user(self, username: str, password: str) -> bool:
        ...
    def authenticate(self, username: str, password: str) -> bool:
        ...
    def get_user_by_username(self, username: str):
        ...

class Experiment:
    def __init__(self, db_manager: DatabaseManager):
        ...
    def create_experiment(self, data):
        ...
    def get_experiment(self, experiment_id):
        ...
    def update_experiment(self, experiment_id, data):
        ...
    def delete_experiment(self, experiment_id):
        ...
    def get_experiments(self, page=1, per_page=5, filters=None, search=None):
        ...
    def get_model_types(self):
        ...
    def get_statuses(self):
        ...
    def validate_experiment_data(self, data):
        ...
```

### Template Structure

- **base.html**: Common HTML structure, navigation bar, flash message handling, CSS/JS includes, responsive design
- **login.html**: Authentication page
- **dashboard.html**: Main experiments listing with filters
- **experiment_form.html**: Create/Edit experiment form
- **experiment_detail.html**: Detailed experiment view

### Static Assets

- **CSS**: Custom Bootstrap overrides, responsive design, component-specific styling, animation/transition effects
- **JavaScript**: Utility functions, form handlers, dashboard interactions, API communication

### Class Relationships (Mermaid Diagram)
```
graph TD
    A[Flask App] --> B[DatabaseManager]
    A --> C[User Model]
    A --> D[Experiment Model]
    B --> E[SQLite Database]
    C --> B
    D --> B
    F[Templates] --> A
    G[Static Files] --> A
    H[Tests] --> A
```

### Design Patterns

- **MVC**: models.py (Model), templates/ (View), app.py (Controller)
- **Repository Pattern**: Database operations abstracted in model classes
- **Decorator Pattern**: `@login_required` for authentication
- **Factory Pattern**: Database connection factory in `DatabaseManager`

### Error Handling

- Application-level: 404 and 500 error handlers
- Model-level: Data validation with error reporting

### Security Architecture

- Session-based authentication
- Password hashing with SHA-256
- Protected routes with decorators
- Server-side and client-side validation
- SQL injection prevention with parameterized queries
- HTML entity escaping in templates

### Performance Optimizations

- Indexes on frequently queried columns
- Pagination to limit result sets
- Minified CSS/JS, optimized assets, caching strategies

### Testing Structure

- Unit, integration, and end-to-end tests
- Coverage: authentication, CRUD, error handling, edge cases, security

### Future Extensibility

- Plugin architecture, RESTful API, scalability considerations

---

## 4. AI Prompts Used

### Overview

This section documents all AI prompts used during development, their purpose, reasoning, and outcomes.

#### Project Planning
- **Prompt:** "I have a Campus Assessment assignment that involves building and deploying a simple full-stack web application to demonstrate my programming, reasoning, and documentation skills. I need your help to design and implement this project step by step."
  - **Purpose:** Establish project requirements and scope
  - **Outcome:** Defined objectives, features, tech stack, and timeline

- **Prompt:** "Help me decide what CRUD object to build based on simplicity and relevance (I'm from an AI & Data Science background)."
  - **Purpose:** Choose a relevant CRUD object
  - **Outcome:** Selected "ML Experiment" as the object

#### Architecture Design
- **Prompt:** "Create a comprehensive database schema for an ML Experiments Tracker with proper relationships, constraints, and indexes."
  - **Purpose:** Design robust schema
  - **Outcome:** Users and experiments tables, constraints, indexes, security

- **Prompt:** "Design a Flask application architecture with proper separation of concerns, following MVC pattern and best practices."
  - **Purpose:** Maintainable, scalable structure
  - **Outcome:** MVC, modular design, error handling, security

#### Implementation
- **Prompt:** "Implement Flask routes for user authentication, experiment CRUD operations, and dashboard functionality with proper error handling."
  - **Purpose:** Core logic
  - **Outcome:** All required routes, authentication, error handling, validation

- **Prompt:** "Create Python classes for database operations with proper connection management, CRUD operations, and data validation."
  - **Purpose:** Data access layer
  - **Outcome:** DatabaseManager, User, Experiment classes, parameterized queries

- **Prompt:** "Create responsive HTML templates using Bootstrap with modern design, proper form handling, and user-friendly interface."
  - **Purpose:** UI/UX
  - **Outcome:** Responsive templates, validation, interactive features

- **Prompt:** "Create custom CSS styles to enhance Bootstrap design with modern touches, better visual hierarchy, and smooth animations."
  - **Purpose:** Visual appeal
  - **Outcome:** Custom theming, transitions, accessibility

- **Prompt:** "Implement client-side JavaScript for form validation, auto-save functionality, and interactive features."
  - **Purpose:** Dynamic UX
  - **Outcome:** Form validation, auto-save, confirmations, loading states

#### Testing
- **Prompt:** "Create comprehensive test cases including positive tests, negative tests, edge cases, and security tests for the Flask application."
  - **Purpose:** Reliability and security
  - **Outcome:** Test classes for auth, CRUD, API, edge cases, security

- **Prompt:** "Implement pytest test cases for the Flask application with proper fixtures, mocking, and comprehensive coverage."
  - **Purpose:** Test code
  - **Outcome:** Fixtures, coverage, cleanup, security/edge tests

#### Documentation & Deployment
- **Prompt:** "Create detailed database schema documentation with field descriptions, constraints, relationships, and security considerations."
- **Prompt:** "Create comprehensive module structure documentation explaining the architecture, design patterns, and class relationships."
- **Prompt:** "Create detailed test plan documentation with test categories, coverage analysis, and testing strategies."
- **Prompt:** "Create deployment configuration for Vercel with proper environment variables and build settings."
- **Prompt:** "Create comprehensive README documentation with setup instructions, feature descriptions, and usage examples."

#### AI Usage Analysis
- Used Claude (Anthropic), Cursor AI, and Git with AI-assisted commit messages
- High success rate, iterative refinement, context preservation
- Learned better prompt engineering, iterative development, documentation quality, and code quality
- Development, documentation, and testing were significantly faster

#### Best Practices Learned
- Be specific, provide context, iterate, validate
- Review everything, test thoroughly, document decisions, maintain consistency
- Plan ahead, document process, validate outputs, learn continuously

---

## 5. Test Plan

### Overview

This document outlines the comprehensive testing strategy for the ML Experiments Tracker application. The test plan covers unit testing, integration testing, security testing, and edge case testing to ensure application reliability and quality.

### Testing Strategy

- **Unit Tests (70%)**: Individual function and class testing
- **Integration Tests (20%)**: Component interaction testing
- **End-to-End Tests (10%)**: Full workflow testing

**Tools:** pytest, pytest-cov, unittest.mock, SQLite in-memory

### Test Categories

#### 1. Authentication Tests
- Positive: Registration, login, session, logout, password hashing
- Negative: Invalid login, empty fields, duplicate registration, session timeout
- Edge: Long/special/unicode credentials, SQL injection

#### 2. Dashboard Tests
- Positive: Loads for auth users, experiment list, pagination, search, filtering
- Negative: Unauth access, invalid pagination, empty search, invalid filters
- Edge: Large datasets, special/unicode/long search terms

#### 3. CRUD Operation Tests
- Create, Read, Update, Delete: Valid/invalid data, form validation, sanitization, error handling

#### 4. Data Validation Tests
- Field validation, edge cases (long, special, unicode, boundary values)

#### 5. Security Tests
- SQL injection, XSS, authentication, authorization, CSRF

#### 6. API Endpoint Tests
- Positive/negative tests for /api/experiments

#### 7. Error Handling Tests
- 404, 500, form validation errors

#### 8. Performance & Usability Tests
- Database and frontend performance, responsive design, accessibility, UX

### Test Implementation

- Test structure: tests/test_app.py, test_models.py, test_auth.py, test_crud.py, test_security.py, conftest.py
- Fixtures for client, auth_client, sample_experiment
- Coverage goals: >90% overall, 100% critical paths

### Test Execution

- Run with `python -m pytest`, coverage, specific categories, verbose, parallel
- Continuous integration: automated tests, coverage, notifications, quality gates

### Test Data Management

- Fresh DB for each test, isolated data, cleanup, realistic scenarios

### Security & Performance Checklists

- Password hashing, session management, brute force, account lockout, SQLi, XSS, CSRF, access control, privilege escalation, data isolation, session hijacking, query optimization, connection pooling, response time, scalability

### Reporting & Maintenance

- Coverage, results, quality metrics, regular updates, documentation

---

## 6. Reflection

### Project Overview

The ML Experiments Tracker was developed as a Campus Assessment assignment to demonstrate full-stack web development skills. The project successfully delivered a functional application with comprehensive documentation and testing, showcasing modern development practices and AI-assisted development techniques.

### What Went Well

- **AI-Assisted Development:** Rapid prototyping, improved code quality, efficient documentation, learning new techniques
- **Architecture:** Clean MVC, modularity, scalability, security
- **User Experience:** Responsive, intuitive, modern UI, interactive features
- **Testing:** Comprehensive coverage, security, edge cases, quality assurance
- **Documentation:** Complete, clear, professional, future reference

### Challenges Faced

- **AI Integration:** Prompt engineering, validation, context management, iteration
- **Technical:** Database design, security, error handling, performance
- **Testing:** Coverage, edge cases, security, test data
- **Documentation:** Coverage, quality, clarity, completeness

### Lessons Learned

- **AI Development:** Specific prompts, validation, iteration, learning
- **Architecture:** Planning, modularity, documentation, testing
- **UX Design:** User-centric, consistency, feedback, accessibility
- **Security:** Input validation, authentication, sanitization, error handling

### Technical Achievements

- Full-stack development, security, performance, code quality, documentation, testing

### Areas for Improvement

- **Features:** User management, advanced search, file uploads, collaboration, notifications, export/import
- **Technical:** PostgreSQL, Redis, full REST API, real-time updates, mobile app, Docker/CI-CD
- **Security:** OAuth, 2FA, rate limiting, audit logging, encryption
- **Architecture:** Microservices, load balancing, sharding, CDN, caching, monitoring
- **Process:** Automated/performance/security/user testing, API/user/developer docs, code review, static analysis

### Personal Growth

- Technical skills, project management, problem solving, research, critical thinking, innovation

### Future Recommendations

- Start with planning, use AI effectively, focus on quality, document everything, demonstrate skills, maintain professional quality, comprehensive documentation, testing, portfolio building, continuous learning, networking

### Conclusion

The ML Experiments Tracker project was a successful demonstration of modern full-stack web development practices. The combination of traditional development skills with AI-assisted techniques resulted in a high-quality application that meets all requirements while showcasing professional development practices. 