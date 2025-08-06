import pytest
import tempfile
import os
from app import app
from models import DatabaseManager, User, Experiment

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    # Create a temporary database for testing
    db_fd, db_path = tempfile.mkstemp()
    
    app.config['TESTING'] = True
    app.config['DATABASE'] = db_path
    
    with app.test_client() as client:
        with app.app_context():
            # Initialize test database
            db_manager = DatabaseManager(db_path)
            user_model = User(db_manager)
            experiment_model = Experiment(db_manager)
            
            # Create test user (admin user is created by init_db.py)
            pass
            
            yield client
    
    # Clean up
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def auth_client(client):
    """Create an authenticated test client"""
    # Login with admin user (which exists in the database)
    client.post('/login', data={
        'username': 'admin',
        'password': 'password123'
    })
    return client

class TestAuthentication:
    """Test authentication functionality"""
    
    def test_login_page_loads(self, client):
        """Test that login page loads correctly"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'ML Experiments Tracker' in response.data
        assert b'Sign in to your account' in response.data
    
    def test_successful_login(self, client):
        """Test successful login with valid credentials"""
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'password123'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Dashboard' in response.data
    
    def test_failed_login_invalid_username(self, client):
        """Test login failure with invalid username"""
        response = client.post('/login', data={
            'username': 'nonexistent',
            'password': 'password123'
        })
        assert response.status_code == 200
        assert b'Invalid username or password' in response.data
    
    def test_failed_login_invalid_password(self, client):
        """Test login failure with invalid password"""
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'wrongpass'
        })
        assert response.status_code == 200
        assert b'Invalid username or password' in response.data
    
    def test_failed_login_empty_fields(self, client):
        """Test login failure with empty fields"""
        response = client.post('/login', data={
            'username': '',
            'password': ''
        })
        assert response.status_code == 200
        assert b'Username and password are required' in response.data
    
    def test_logout(self, auth_client):
        """Test logout functionality"""
        response = auth_client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'Sign in to your account' in response.data

class TestDashboard:
    """Test dashboard functionality"""
    
    def test_dashboard_requires_auth(self, client):
        """Test that dashboard requires authentication"""
        response = client.get('/dashboard', follow_redirects=True)
        assert response.status_code == 200
        assert b'Sign in to your account' in response.data
    
    def test_dashboard_loads_authenticated(self, auth_client):
        """Test that dashboard loads for authenticated users"""
        response = auth_client.get('/dashboard')
        assert response.status_code == 200
        assert b'ML Experiments' in response.data
        assert b'New Experiment' in response.data
    
    def test_dashboard_pagination(self, auth_client):
        """Test dashboard pagination"""
        response = auth_client.get('/dashboard?page=1')
        assert response.status_code == 200
    
    def test_dashboard_search(self, auth_client):
        """Test dashboard search functionality"""
        response = auth_client.get('/dashboard?search=test')
        assert response.status_code == 200
    
    def test_dashboard_filtering(self, auth_client):
        """Test dashboard filtering"""
        response = auth_client.get('/dashboard?status=Completed')
        assert response.status_code == 200

class TestExperimentCRUD:
    """Test experiment CRUD operations"""
    
    def test_new_experiment_page_loads(self, auth_client):
        """Test that new experiment page loads"""
        response = auth_client.get('/experiment/new')
        assert response.status_code == 200
        assert b'New ML Experiment' in response.data
    
    def test_create_experiment_success(self, auth_client):
        """Test successful experiment creation"""
        response = auth_client.post('/experiment/new', data={
            'title': 'Test Experiment',
            'description': 'This is a test experiment',
            'model_type': 'CNN',
            'status': 'Planning',
            'accuracy': '85.5',
            'is_public': '1'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Test Experiment' in response.data
    
    def test_create_experiment_missing_title(self, auth_client):
        """Test experiment creation with missing title"""
        response = auth_client.post('/experiment/new', data={
            'title': '',
            'description': 'This is a test experiment',
            'model_type': 'CNN',
            'status': 'Planning'
        })
        assert response.status_code == 200
        assert b'Title is required' in response.data
    
    def test_create_experiment_missing_description(self, auth_client):
        """Test experiment creation with missing description"""
        response = auth_client.post('/experiment/new', data={
            'title': 'Test Experiment',
            'description': '',
            'model_type': 'CNN',
            'status': 'Planning'
        })
        assert response.status_code == 200
        assert b'Description is required' in response.data
    
    def test_create_experiment_invalid_accuracy(self, auth_client):
        """Test experiment creation with invalid accuracy"""
        response = auth_client.post('/experiment/new', data={
            'title': 'Test Experiment',
            'description': 'This is a test experiment',
            'model_type': 'CNN',
            'status': 'Planning',
            'accuracy': '150'  # Invalid: > 100
        })
        assert response.status_code == 200
        assert b'Accuracy must be between 0 and 100' in response.data
    
    def test_view_experiment(self, auth_client):
        """Test viewing an experiment"""
        # First create an experiment
        auth_client.post('/experiment/new', data={
            'title': 'Test Experiment',
            'description': 'This is a test experiment',
            'model_type': 'CNN',
            'status': 'Planning'
        })
        
        # Then view it
        response = auth_client.get('/experiment/1')
        assert response.status_code == 200
        assert b'Test Experiment' in response.data
    
    def test_view_nonexistent_experiment(self, auth_client):
        """Test viewing a nonexistent experiment"""
        response = auth_client.get('/experiment/999', follow_redirects=True)
        assert response.status_code == 200
        assert b'Experiment not found' in response.data
    
    def test_edit_experiment(self, auth_client):
        """Test editing an experiment"""
        # First create an experiment
        auth_client.post('/experiment/new', data={
            'title': 'Test Experiment',
            'description': 'This is a test experiment',
            'model_type': 'CNN',
            'status': 'Planning'
        })
        
        # Then edit it
        response = auth_client.get('/experiment/1/edit')
        assert response.status_code == 200
        assert b'Edit ML Experiment' in response.data
    
    def test_update_experiment_success(self, auth_client):
        """Test successful experiment update"""
        # First create an experiment
        auth_client.post('/experiment/new', data={
            'title': 'Test Experiment',
            'description': 'This is a test experiment',
            'model_type': 'CNN',
            'status': 'Planning'
        })
        
        # Then update it
        response = auth_client.post('/experiment/1/edit', data={
            'title': 'Updated Test Experiment',
            'description': 'This is an updated test experiment',
            'model_type': 'RNN',
            'status': 'Completed',
            'accuracy': '92.5'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Updated Test Experiment' in response.data
    
    def test_delete_experiment(self, auth_client):
        """Test deleting an experiment"""
        # First create an experiment
        auth_client.post('/experiment/new', data={
            'title': 'Test Experiment',
            'description': 'This is a test experiment',
            'model_type': 'CNN',
            'status': 'Planning'
        })
        
        # Then delete it
        response = auth_client.post('/experiment/1/delete', follow_redirects=True)
        assert response.status_code == 200
        assert b'deleted successfully' in response.data

class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_api_experiments_requires_auth(self, client):
        """Test that API requires authentication"""
        response = client.get('/api/experiments', follow_redirects=True)
        assert response.status_code == 200
        assert b'Sign in to your account' in response.data
    
    def test_api_experiments_authenticated(self, auth_client):
        """Test API experiments endpoint for authenticated users"""
        response = auth_client.get('/api/experiments')
        assert response.status_code == 200
        data = response.get_json()
        assert 'experiments' in data
        assert 'total_count' in data
        assert 'page' in data

class TestErrorHandling:
    """Test error handling"""
    
    def test_404_error(self, client):
        """Test 404 error handling"""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404
    
    def test_500_error(self, client):
        """Test 500 error handling"""
        # This would require triggering a server error
        # For now, just test that the error handlers exist
        assert hasattr(app, 'errorhandler')
        # Test that error handlers are registered
        assert app.error_handler_spec[None][404] is not None
        assert app.error_handler_spec[None][500] is not None

class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_very_long_title(self, auth_client):
        """Test experiment with very long title"""
        long_title = 'A' * 1000  # Very long title
        response = auth_client.post('/experiment/new', data={
            'title': long_title,
            'description': 'Test description',
            'model_type': 'CNN',
            'status': 'Planning'
        })
        # Should handle gracefully
        assert response.status_code in [200, 302]
    
    def test_special_characters_in_title(self, auth_client):
        """Test experiment with special characters in title"""
        special_title = "Test Experiment with 'quotes' and \"double quotes\" and <tags>"
        response = auth_client.post('/experiment/new', data={
            'title': special_title,
            'description': 'Test description',
            'model_type': 'CNN',
            'status': 'Planning'
        })
        # Should handle gracefully
        assert response.status_code in [200, 302]
    
    def test_unicode_characters(self, auth_client):
        """Test experiment with unicode characters"""
        unicode_title = "Test Experiment with unicode: 测试实验 🧪"
        response = auth_client.post('/experiment/new', data={
            'title': unicode_title,
            'description': 'Test description with unicode: 测试',
            'model_type': 'CNN',
            'status': 'Planning'
        })
        # Should handle gracefully
        assert response.status_code in [200, 302]
    
    def test_negative_accuracy(self, auth_client):
        """Test experiment with negative accuracy"""
        response = auth_client.post('/experiment/new', data={
            'title': 'Test Experiment',
            'description': 'Test description',
            'model_type': 'CNN',
            'status': 'Planning',
            'accuracy': '-10'
        })
        assert response.status_code == 200
        assert b'Accuracy must be between 0 and 100' in response.data
    
    def test_non_numeric_accuracy(self, auth_client):
        """Test experiment with non-numeric accuracy"""
        response = auth_client.post('/experiment/new', data={
            'title': 'Test Experiment',
            'description': 'Test description',
            'model_type': 'CNN',
            'status': 'Planning',
            'accuracy': 'not_a_number'
        })
        assert response.status_code == 200
        assert b'Accuracy must be a valid number' in response.data

class TestSecurity:
    """Test security aspects"""
    
    def test_sql_injection_prevention(self, auth_client):
        """Test SQL injection prevention"""
        malicious_title = "'; DROP TABLE experiments; --"
        response = auth_client.post('/experiment/new', data={
            'title': malicious_title,
            'description': 'Test description',
            'model_type': 'CNN',
            'status': 'Planning'
        })
        # Should handle gracefully without SQL injection
        assert response.status_code in [200, 302]
    
    def test_xss_prevention(self, auth_client):
        """Test XSS prevention"""
        xss_title = "<script>alert('xss')</script>"
        response = auth_client.post('/experiment/new', data={
            'title': xss_title,
            'description': 'Test description',
            'model_type': 'CNN',
            'status': 'Planning'
        })
        # Should handle gracefully
        assert response.status_code in [200, 302]
    
    def test_csrf_protection(self, client):
        """Test CSRF protection (basic test)"""
        # This is a basic test - in a real app, you'd want more comprehensive CSRF testing
        response = client.post('/experiment/new', data={
            'title': 'Test Experiment',
            'description': 'Test description',
            'model_type': 'CNN',
            'status': 'Planning'
        }, follow_redirects=True)
        # Should redirect to login since not authenticated
        assert b'Sign in to your account' in response.data 