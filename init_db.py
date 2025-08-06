#!/usr/bin/env python3
"""
Database initialization script for ML Experiments Tracker
Creates database tables and default admin user
"""

from models import DatabaseManager, User, Experiment
import random

def init_database():
    """Initialize database with tables and default data"""
    print("🚀 Initializing ML Experiments Tracker Database...")
    
    # Initialize database manager
    db_manager = DatabaseManager()
    user_model = User(db_manager)
    experiment_model = Experiment(db_manager)
    
    # Create default admin user if it doesn't exist
    if not user_model.get_user_by_username('admin'):
        success = user_model.create_user('admin', 'password123')
        if success:
            print("✅ Default admin user created:")
            print("   Username: admin")
            print("   Password: password123")
        else:
            print("❌ Failed to create admin user")
    else:
        print("ℹ️  Admin user already exists")
    
    # Create sample experiments for demonstration
    sample_experiments = []
    model_types = ['CNN', 'RNN', 'Transformer', 'LSTM', 'BERT', 'Custom', 'Random Forest', 'XGBoost', 'SVM']
    statuses = ['Completed', 'Running', 'Planning', 'Failed']
    domains = ['Finance', 'Healthcare', 'E-commerce', 'Security', 'IoT', 'NLP', 'Computer Vision', 'Education']
    tasks = ['Classification', 'Regression', 'Detection', 'Forecasting', 'Analysis', 'Recognition', 'Translation']

    for i in range(100):
        domain = random.choice(domains)
        task = random.choice(tasks)
        model = random.choice(model_types)
        status = random.choice(statuses)
        accuracy = round(random.uniform(60, 99.5), 2) if status == 'Completed' else None

        sample_experiments.append({
            'title': f'{domain} {task} with {model} - Exp #{i+1}',
            'description': f'A sample experiment for {task.lower()} in the {domain.lower()} domain using a {model} model. This is experiment number {i+1} in the dataset.',
            'model_type': model,
            'status': status,
            'accuracy': accuracy,
            'is_public': random.choice([True, False])
        })
    
    # Create sample experiments
    created_count = 0
    existing_titles = {exp['title'] for exp in experiment_model.get_experiments()['experiments']}

    for experiment_data in sample_experiments:
        if experiment_data['title'] not in existing_titles:
            experiment_id = experiment_model.create_experiment(experiment_data)
            if experiment_id:
                created_count += 1
                print(f"✅ Created sample experiment: {experiment_data['title']}")
    
    if created_count > 0:
        print(f"✅ Created {created_count} sample experiments")
    else:
        print("ℹ️  All sample experiments already exist")
    
    print("\n🎉 Database initialization complete!")
    print("\n📋 Next steps:")
    print("1. Run the application: python app.py")
    print("2. Open your browser to: http://localhost:5000")
    print("3. Login with: admin / password123")
    print("4. Start creating your own ML experiments!")

if __name__ == '__main__':
    init_database() 