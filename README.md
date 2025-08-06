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