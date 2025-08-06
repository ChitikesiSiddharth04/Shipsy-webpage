import sqlite3
import hashlib
from datetime import datetime
from typing import List, Optional, Dict, Any

class DatabaseManager:
    def __init__(self, db_path: str = "experiments.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = 1")
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create experiments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                model_type TEXT NOT NULL,
                status TEXT NOT NULL,
                accuracy REAL,
                is_public BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_experiments_status ON experiments(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_experiments_model_type ON experiments(model_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_experiments_is_public ON experiments(is_public)')
        
        conn.commit()
        conn.close()

class User:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def create_user(self, username: str, password: str) -> bool:
        """Create a new user with hashed password"""
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user with username and password"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id FROM users WHERE username = ? AND password_hash = ?',
            (username, password_hash)
        )
        user = cursor.fetchone()
        conn.close()
        return user is not None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user details by username"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None

class Experiment:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def create_experiment(self, data: Dict[str, Any]) -> int:
        """Create a new experiment and return its ID"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO experiments (title, description, model_type, status, accuracy, is_public)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['title'],
            data['description'],
            data['model_type'],
            data['status'],
            data.get('accuracy'),
            data.get('is_public', False)
        ))
        
        experiment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return experiment_id
    
    def get_experiment(self, experiment_id: int) -> Optional[Dict[str, Any]]:
        """Get experiment by ID"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM experiments WHERE id = ?', (experiment_id,))
        experiment = cursor.fetchone()
        conn.close()
        return dict(experiment) if experiment else None
    
    def update_experiment(self, experiment_id: int, data: Dict[str, Any]) -> bool:
        """Update an existing experiment"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE experiments 
            SET title = ?, description = ?, model_type = ?, status = ?, 
                accuracy = ?, is_public = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data['title'],
            data['description'],
            data['model_type'],
            data['status'],
            data.get('accuracy'),
            data.get('is_public', False),
            experiment_id
        ))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0
    
    def delete_experiment(self, experiment_id: int) -> bool:
        """Delete an experiment"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM experiments WHERE id = ?', (experiment_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0
    
    def get_experiments(self, page: int = 1, per_page: int = 5, 
                       filters: Optional[Dict[str, Any]] = None,
                       search: Optional[str] = None) -> Dict[str, Any]:
        """Get paginated experiments with optional filtering and search"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        # Build query with filters
        query = 'SELECT * FROM experiments WHERE 1=1'
        params = []
        
        if filters:
            if filters.get('status'):
                query += ' AND status = ?'
                params.append(filters['status'])
            if filters.get('model_type'):
                query += ' AND model_type = ?'
                params.append(filters['model_type'])
            if filters.get('is_public') is not None:
                query += ' AND is_public = ?'
                params.append(filters['is_public'])
        
        if search:
            query += ' AND (title LIKE ? OR description LIKE ?)'
            search_term = f'%{search}%'
            params.extend([search_term, search_term])
        
        # Get total count
        count_query = query.replace('SELECT *', 'SELECT COUNT(*)')
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()[0]
        
        # Add pagination
        query += ' ORDER BY created_at DESC LIMIT ? OFFSET ?'
        offset = (page - 1) * per_page
        params.extend([per_page, offset])
        
        cursor.execute(query, params)
        experiments = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'experiments': experiments,
            'total_count': total_count,
            'page': page,
            'per_page': per_page,
            'total_pages': (total_count + per_page - 1) // per_page
        }
    
    def get_model_types(self) -> List[str]:
        """Get available model types"""
        return ['CNN', 'RNN', 'Transformer', 'LSTM', 'BERT', 'Custom']
    
    def get_statuses(self) -> List[str]:
        """Get available statuses"""
        return ['Planning', 'Running', 'Completed', 'Failed']
    
    def validate_experiment_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate experiment data and return cleaned data"""
        errors = []
        
        # Required fields
        if not data.get('title', '').strip():
            errors.append('Title is required')
        
        if not data.get('description', '').strip():
            errors.append('Description is required')
        
        if not data.get('model_type'):
            errors.append('Model type is required')
        elif data['model_type'] not in self.get_model_types():
            errors.append('Invalid model type')
        
        if not data.get('status'):
            errors.append('Status is required')
        elif data['status'] not in self.get_statuses():
            errors.append('Invalid status')
        
        # Optional fields validation
        accuracy = data.get('accuracy')
        if accuracy is not None:
            try:
                accuracy = float(accuracy)
                if not (0 <= accuracy <= 100):
                    errors.append('Accuracy must be between 0 and 100')
            except (ValueError, TypeError):
                errors.append('Accuracy must be a valid number')
        
        # Clean data
        cleaned_data = {
            'title': data.get('title', '').strip(),
            'description': data.get('description', '').strip(),
            'model_type': data.get('model_type'),
            'status': data.get('status'),
            'accuracy': accuracy,
            'is_public': bool(data.get('is_public'))
        }
        
        return {'data': cleaned_data, 'errors': errors} 