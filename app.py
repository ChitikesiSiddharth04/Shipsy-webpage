from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response, jsonify
from functools import wraps
import os
from datetime import timedelta
from models import DatabaseManager, User, Experiment

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_COOKIE_SECURE'] = False  # Allow HTTP for development
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Initialize database and models
db_manager = DatabaseManager()
user_model = User(db_manager)
experiment_model = Experiment(db_manager)

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Redirect to login if not authenticated, otherwise to dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            
            print(f"Login attempt - Username: {username}, Password provided: {'yes' if password else 'no'}")
            
            if not username or not password:
                flash('Username and password are required.', 'error')
                return render_template('login.html')
            
            if user_model.authenticate(username, password):
                session['user_id'] = username
                session.permanent = True  # Make session persistent
                print(f"Login successful for user: {username}")
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                print(f"Login failed for user: {username}")
                flash('Invalid username or password. Authentication failed.', 'error')
        except Exception as e:
            print(f"Login error: {str(e)}")
            flash('An error occurred during login. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    """Handle user logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    
    response = make_response(redirect(url_for('login')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with experiments list"""
    print("Session contents:", dict(session))  # Debug print
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    search = request.args.get('search', '').strip()
    
    # Get filters from query parameters
    filters = {}
    if request.args.get('status'):
        filters['status'] = request.args.get('status')
    if request.args.get('model_type'):
        filters['model_type'] = request.args.get('model_type')
    if request.args.get('is_public'):
        # Convert string '0'/'1' to boolean
        is_public_value = request.args.get('is_public')
        if is_public_value == '1':
            filters['is_public'] = True
        elif is_public_value == '0':
            filters['is_public'] = False
    
    # Get experiments with pagination and filters
    result = experiment_model.get_experiments(
        page=page, 
        per_page=per_page, 
        filters=filters if filters else None,
        search=search if search else None
    )
    
    return render_template('dashboard.html', 
                         experiments=result['experiments'],
                         pagination=result,
                         model_types=experiment_model.get_model_types(),
                         statuses=experiment_model.get_statuses(),
                         current_filters=request.args)


@app.route('/api/filter_experiments')
@login_required
def filter_experiments_api():
    """API endpoint to get filtered experiments as JSON"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    search = request.args.get('search', '').strip()
    
    # Get filters from query parameters
    filters = {}
    if request.args.get('status'):
        filters['status'] = request.args.get('status')
    if request.args.get('model_type'):
        filters['model_type'] = request.args.get('model_type')
    if request.args.get('is_public'):
        is_public_value = request.args.get('is_public')
        if is_public_value == '1':
            filters['is_public'] = True
        elif is_public_value == '0':
            filters['is_public'] = False
            
    # Get experiments with pagination and filters
    result = experiment_model.get_experiments(
        page=page, 
        per_page=per_page, 
        filters=filters if filters else None,
        search=search if search else None
    )
    
    return jsonify(result)


@app.route('/experiment/new', methods=['GET', 'POST'])
@login_required
def new_experiment():
    """Create a new experiment"""
    if request.method == 'POST':
        # Validate and create experiment
        validation = experiment_model.validate_experiment_data(request.form)
        
        if validation['errors']:
            for error in validation['errors']:
                flash(error, 'error')
            return render_template('experiment_form.html', 
                                experiment=request.form,
                                model_types=experiment_model.get_model_types(),
                                statuses=experiment_model.get_statuses())
        
        # Create the experiment
        experiment_id = experiment_model.create_experiment(validation['data'])
        flash(f'Experiment "{validation["data"]["title"]}" created successfully!', 'success')
        return redirect(url_for('view_experiment', experiment_id=experiment_id))
    
    return render_template('experiment_form.html',
                         experiment={},
                         model_types=experiment_model.get_model_types(),
                         statuses=experiment_model.get_statuses())

@app.route('/experiment/<int:experiment_id>')
@login_required
def view_experiment(experiment_id):
    """View a specific experiment"""
    experiment = experiment_model.get_experiment(experiment_id)
    if not experiment:
        flash('Experiment not found.', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('experiment_detail.html', experiment=experiment)

@app.route('/experiment/<int:experiment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_experiment(experiment_id):
    """Edit an existing experiment"""
    experiment = experiment_model.get_experiment(experiment_id)
    if not experiment:
        flash('Experiment not found.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Validate and update experiment
        validation = experiment_model.validate_experiment_data(request.form)
        
        if validation['errors']:
            for error in validation['errors']:
                flash(error, 'error')
            return render_template('experiment_form.html', 
                                experiment=request.form,
                                model_types=experiment_model.get_model_types(),
                                statuses=experiment_model.get_statuses())
        
        # Update the experiment
        if experiment_model.update_experiment(experiment_id, validation['data']):
            flash(f'Experiment "{validation["data"]["title"]}" updated successfully!', 'success')
            return redirect(url_for('view_experiment', experiment_id=experiment_id))
        else:
            flash('Failed to update experiment.', 'error')
    
    return render_template('experiment_form.html',
                         experiment=experiment,
                         model_types=experiment_model.get_model_types(),
                         statuses=experiment_model.get_statuses())

@app.route('/experiment/<int:experiment_id>/delete', methods=['DELETE'])
@login_required
def delete_experiment(experiment_id):
    """Delete an experiment"""
    experiment = experiment_model.get_experiment(experiment_id)
    if not experiment:
        return jsonify({'success': False, 'message': 'Experiment not found.'}), 404
    
    if experiment_model.delete_experiment(experiment_id):
        return jsonify({'success': True, 'message': f'Experiment "{experiment["title"]}" deleted successfully!'})
    else:
        return jsonify({'success': False, 'message': 'Failed to delete experiment.'}), 500

@app.route('/api/experiments')
@login_required
def api_experiments():
    """API endpoint for experiments (for AJAX requests)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    search = request.args.get('search', '').strip()
    
    filters = {}
    if request.args.get('status'):
        filters['status'] = request.args.get('status')
    if request.args.get('model_type'):
        filters['model_type'] = request.args.get('model_type')
    if request.args.get('is_public') is not None:
        filters['is_public'] = request.args.get('is_public', type=bool)
    
    result = experiment_model.get_experiments(
        page=page, 
        per_page=per_page, 
        filters=filters if filters else None,
        search=search if search else None
    )
    
    return jsonify(result)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/analytics')
@login_required
def analytics():
    # Placeholder: In a real app, you would compute stats here
    return render_template('analytics.html')

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create default admin user if it doesn't exist
    if not user_model.get_user_by_username('admin'):
        user_model.create_user('admin', 'password123')
        print("Default admin user created: admin/password123")
    
    app.run(debug=True, host='0.0.0.0', port=5001) 