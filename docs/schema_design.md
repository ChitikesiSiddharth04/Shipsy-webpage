# Database Schema Design

## Overview

The ML Experiments Tracker uses SQLite as its database with two main tables: `users` and `experiments`. The schema is designed to be simple yet comprehensive, supporting all CRUD operations with proper relationships and constraints.

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Field Descriptions:**
- `id`: Primary key, auto-incrementing integer
- `username`: Unique username for login (max 50 characters)
- `password_hash`: SHA-256 hashed password for security
- `created_at`: Timestamp when user was created

**Constraints:**
- Username must be unique
- Username and password cannot be null
- Password is stored as hash, never plain text

### Experiments Table

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

**Field Descriptions:**
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

## Enumerated Values

### Model Types
- `CNN` - Convolutional Neural Network
- `RNN` - Recurrent Neural Network
- `Transformer` - Transformer Architecture
- `LSTM` - Long Short-Term Memory
- `BERT` - Bidirectional Encoder Representations from Transformers
- `Custom` - Custom/Other model types

### Status Values
- `Planning` - Experiment is in planning phase
- `Running` - Experiment is currently running
- `Completed` - Experiment has finished successfully
- `Failed` - Experiment failed or was cancelled

## Indexes

For optimal performance, the following indexes are created:

```sql
CREATE INDEX idx_experiments_status ON experiments(status);
CREATE INDEX idx_experiments_model_type ON experiments(model_type);
CREATE INDEX idx_experiments_is_public ON experiments(is_public);
```

**Index Purposes:**
- `idx_experiments_status`: Fast filtering by experiment status
- `idx_experiments_model_type`: Fast filtering by model type
- `idx_experiments_is_public`: Fast filtering by visibility

## Data Relationships

### One-to-Many Relationship
- One user can have many experiments
- Each experiment belongs to one user (implied through session management)

### Referential Integrity
- User authentication is handled through Flask sessions
- No foreign key constraints needed due to session-based authentication

## Data Validation Rules

### User Data
- Username: 3-50 characters, alphanumeric and underscores only
- Password: Minimum 8 characters, stored as SHA-256 hash

### Experiment Data
- Title: 1-200 characters, required
- Description: 1-unlimited characters, required
- Model Type: Must be from predefined list
- Status: Must be from predefined list
- Accuracy: 0-100, optional, numeric only
- Is Public: Boolean (0 or 1)

## Security Considerations

### Password Security
- Passwords are hashed using SHA-256
- No plain text passwords stored
- Salt could be added for additional security

### SQL Injection Prevention
- All user inputs are parameterized
- No direct string concatenation in SQL queries
- Input validation on both client and server side

### Data Sanitization
- HTML entities are escaped in templates
- XSS prevention through proper output encoding
- Input length limits to prevent DoS attacks

## Performance Considerations

### Query Optimization
- Indexes on frequently filtered columns
- Pagination to limit result sets
- Efficient WHERE clauses

### Storage Optimization
- Appropriate field types (INTEGER vs TEXT)
- Indexes only on necessary columns
- Regular database maintenance

## Migration Strategy

### Version Control
- Database schema is versioned
- Migration scripts for future updates
- Backward compatibility maintained

### Data Backup
- Regular database backups recommended
- Export functionality for data portability
- Version control for schema changes

## Future Enhancements

### Potential Additions
- User roles and permissions
- Experiment categories/tags
- File attachments for experiment data
- Experiment sharing and collaboration
- Audit trail for changes
- Advanced search and filtering

### Scalability Considerations
- Database connection pooling
- Caching layer for frequently accessed data
- Horizontal scaling with read replicas
- Microservices architecture for large scale 