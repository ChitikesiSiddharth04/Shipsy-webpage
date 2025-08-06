#!/usr/bin/env python3
"""
Populate ML Experiments Tracker with comprehensive sample data
covering multiple AI/ML domains and use cases.
"""

import sqlite3
from datetime import datetime, timedelta
import random

def populate_sample_experiments():
    """Add diverse, realistic ML experiments across multiple domains"""
    
    # Connect to database
    conn = sqlite3.connect('experiments.db')
    cursor = conn.cursor()
    
    # Clear existing experiments (optional - comment out to keep existing data)
    cursor.execute('DELETE FROM experiments')
    
    # Comprehensive sample experiments across ML domains
    sample_experiments = [
        # Computer Vision - Image Classification
        {
            'title': 'ResNet-50 Image Classification on CIFAR-100',
            'description': 'Fine-tuning ResNet-50 architecture for 100-class image classification. Using data augmentation, dropout 0.5, and Adam optimizer with learning rate scheduling.',
            'model_type': 'CNN',
            'status': 'Completed',
            'accuracy': 87.3,
            'is_public': True
        },
        {
            'title': 'Vision Transformer (ViT) vs CNN Comparison',
            'description': 'Comparing Vision Transformer Base-16 against traditional CNNs on ImageNet subset. Analyzing attention maps and computational efficiency.',
            'model_type': 'Transformer',
            'status': 'Running',
            'accuracy': 82.1,
            'is_public': True
        },
        {
            'title': 'Medical X-Ray Pneumonia Detection',
            'description': 'Custom CNN architecture for detecting pneumonia in chest X-rays. Dataset: 5,863 X-ray images. Using transfer learning from ImageNet.',
            'model_type': 'CNN',
            'status': 'Completed',
            'accuracy': 94.2,
            'is_public': False
        },
        {
            'title': 'Real-time Object Detection with YOLO v8',
            'description': 'Implementing YOLOv8 for real-time object detection in autonomous driving scenarios. Custom dataset with 50,000 annotated images.',
            'model_type': 'CNN',
            'status': 'Running',
            'accuracy': 76.8,
            'is_public': True
        },
        
        # Natural Language Processing
        {
            'title': 'BERT Fine-tuning for Sentiment Analysis',
            'description': 'Fine-tuning BERT-base-uncased on movie review sentiment classification. Dataset: IMDB 50k reviews. Batch size 16, learning rate 2e-5.',
            'model_type': 'BERT',
            'status': 'Completed',
            'accuracy': 93.7,
            'is_public': True
        },
        {
            'title': 'GPT-3.5 vs Custom LSTM for Text Generation',
            'description': 'Comparing GPT-3.5 fine-tuning with custom LSTM for creative writing generation. Evaluating coherence, creativity, and computational cost.',
            'model_type': 'LSTM',
            'status': 'Planning',
            'accuracy': None,
            'is_public': True
        },
        {
            'title': 'Multilingual Named Entity Recognition',
            'description': 'Training multilingual BERT for NER across English, Spanish, French, and German. Using CoNLL-2003 and custom datasets.',
            'model_type': 'BERT',
            'status': 'Running',
            'accuracy': 89.4,
            'is_public': False
        },
        {
            'title': 'Question Answering with RoBERTa',
            'description': 'Fine-tuning RoBERTa-large on SQuAD 2.0 dataset for extractive question answering. Implementing answer span prediction.',
            'model_type': 'Transformer',
            'status': 'Completed',
            'accuracy': 91.2,
            'is_public': True
        },
        
        # Time Series & Forecasting
        {
            'title': 'Stock Price Prediction with LSTM',
            'description': 'Multi-layer LSTM for predicting S&P 500 stock prices. Features: technical indicators, volume, sentiment analysis from news.',
            'model_type': 'LSTM',
            'status': 'Failed',
            'accuracy': 67.3,
            'is_public': False
        },
        {
            'title': 'Energy Consumption Forecasting',
            'description': 'Transformer-based model for predicting hourly energy consumption. Dataset: 4 years of smart meter data from 1000+ households.',
            'model_type': 'Transformer',
            'status': 'Completed',
            'accuracy': 85.6,
            'is_public': True
        },
        {
            'title': 'Weather Pattern Analysis with RNN',
            'description': 'Recurrent neural network for weather pattern recognition and 7-day forecasting. Multi-variate time series with temperature, humidity, pressure.',
            'model_type': 'RNN',
            'status': 'Running',
            'accuracy': 78.9,
            'is_public': True
        },
        
        # Reinforcement Learning & Gaming
        {
            'title': 'Deep Q-Network for Atari Games',
            'description': 'Implementing DQN with experience replay for Atari 2600 games. Testing on Breakout, Space Invaders, and Pong.',
            'model_type': 'Custom',
            'status': 'Completed',
            'accuracy': 92.1,
            'is_public': True
        },
        {
            'title': 'AlphaZero-style Chess Engine',
            'description': 'Monte Carlo Tree Search with neural network evaluation for chess position assessment. Training against Stockfish engine.',
            'model_type': 'Custom',
            'status': 'Planning',
            'accuracy': None,
            'is_public': False
        },
        
        # Audio & Speech Processing
        {
            'title': 'Speech Recognition with Wav2Vec 2.0',
            'description': 'Fine-tuning Wav2Vec 2.0 for automatic speech recognition on LibriSpeech dataset. Comparing with traditional LSTM approaches.',
            'model_type': 'Transformer',
            'status': 'Running',
            'accuracy': 88.7,
            'is_public': True
        },
        {
            'title': 'Music Genre Classification',
            'description': 'CNN-based model for classifying music genres from mel-spectrograms. Dataset: GTZAN with 10 genres, 1000 tracks each.',
            'model_type': 'CNN',
            'status': 'Completed',
            'accuracy': 84.3,
            'is_public': True
        },
        
        # Recommendation Systems
        {
            'title': 'Netflix Movie Recommendation System',
            'description': 'Collaborative filtering with deep neural networks. Matrix factorization + user/item embeddings. Dataset: MovieLens 25M ratings.',
            'model_type': 'Custom',
            'status': 'Completed',
            'accuracy': 79.8,
            'is_public': False
        },
        {
            'title': 'E-commerce Product Recommendations',
            'description': 'Hybrid recommendation system combining collaborative filtering, content-based filtering, and deep learning embeddings.',
            'model_type': 'Custom',
            'status': 'Running',
            'accuracy': 73.2,
            'is_public': True
        },
        
        # Healthcare & Biomedical
        {
            'title': 'Drug Discovery Molecular Property Prediction',
            'description': 'Graph Neural Network for predicting molecular properties in drug discovery. Dataset: 100k+ chemical compounds with bioactivity data.',
            'model_type': 'Custom',
            'status': 'Planning',
            'accuracy': None,
            'is_public': False
        },
        {
            'title': 'ECG Arrhythmia Detection',
            'description': '1D CNN for detecting cardiac arrhythmias from ECG signals. MIT-BIH Arrhythmia Database with 47 patient records.',
            'model_type': 'CNN',
            'status': 'Completed',
            'accuracy': 96.7,
            'is_public': True
        },
        
        # Autonomous Systems
        {
            'title': 'Self-Driving Car Lane Detection',
            'description': 'Computer vision pipeline for lane detection using CNN + traditional CV techniques. Real-world driving footage dataset.',
            'model_type': 'CNN',
            'status': 'Running',
            'accuracy': 91.4,
            'is_public': True
        },
        {
            'title': 'Drone Navigation with Deep RL',
            'description': 'Deep reinforcement learning for autonomous drone navigation in complex environments. Simulation-to-real transfer learning.',
            'model_type': 'Custom',
            'status': 'Failed',
            'accuracy': 62.8,
            'is_public': False
        },
        
        # Fraud Detection & Security
        {
            'title': 'Credit Card Fraud Detection',
            'description': 'Ensemble model combining Random Forest, XGBoost, and Neural Networks for real-time fraud detection. Highly imbalanced dataset.',
            'model_type': 'Custom',
            'status': 'Completed',
            'accuracy': 99.2,
            'is_public': False
        },
        {
            'title': 'Network Intrusion Detection System',
            'description': 'LSTM-based model for detecting network intrusions and cyber attacks. NSL-KDD dataset with 41 features.',
            'model_type': 'LSTM',
            'status': 'Running',
            'accuracy': 87.9,
            'is_public': True
        },
        
        # Generative AI
        {
            'title': 'StyleGAN Face Generation',
            'description': 'Training StyleGAN2 for high-quality face generation. Dataset: CelebA-HQ 30k images. Exploring latent space interpolation.',
            'model_type': 'Custom',
            'status': 'Planning',
            'accuracy': None,
            'is_public': True
        },
        {
            'title': 'Text-to-Image Generation with Diffusion',
            'description': 'Implementing Stable Diffusion for text-to-image generation. Fine-tuning on custom art dataset for specific style transfer.',
            'model_type': 'Custom',
            'status': 'Running',
            'accuracy': 74.6,
            'is_public': False
        },
        
        # Edge AI & Mobile
        {
            'title': 'MobileNet Optimization for Edge Devices',
            'description': 'Optimizing MobileNetV3 for real-time inference on mobile devices. Quantization and pruning techniques for 10x speedup.',
            'model_type': 'CNN',
            'status': 'Completed',
            'accuracy': 81.7,
            'is_public': True
        },
        {
            'title': 'TinyML Gesture Recognition',
            'description': 'Ultra-lightweight CNN for gesture recognition on microcontrollers. Model size <100KB, inference <10ms on Arduino.',
            'model_type': 'CNN',
            'status': 'Running',
            'accuracy': 89.3,
            'is_public': True
        }
    ]
    
    # Insert sample experiments with realistic timestamps
    base_date = datetime.now() - timedelta(days=90)  # Start 90 days ago
    
    for i, exp in enumerate(sample_experiments):
        # Create realistic timestamps
        created_at = base_date + timedelta(days=random.randint(0, 85))
        updated_at = created_at + timedelta(days=random.randint(0, 5))
        
        cursor.execute('''
            INSERT INTO experiments (title, description, model_type, status, accuracy, is_public, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            exp['title'],
            exp['description'],
            exp['model_type'],
            exp['status'],
            exp['accuracy'],
            exp['is_public'],
            created_at.strftime('%Y-%m-%d %H:%M:%S'),
            updated_at.strftime('%Y-%m-%d %H:%M:%S')
        ))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Successfully added {len(sample_experiments)} diverse ML experiments!")
    print("\n📊 Experiment Distribution:")
    
    # Count by model type
    model_counts = {}
    status_counts = {}
    
    for exp in sample_experiments:
        model_type = exp['model_type']
        status = exp['status']
        
        model_counts[model_type] = model_counts.get(model_type, 0) + 1
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("\n🤖 By Model Type:")
    for model, count in sorted(model_counts.items()):
        print(f"  {model}: {count} experiments")
    
    print("\n📈 By Status:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count} experiments")
    
    print("\n🎯 Domains Covered:")
    domains = [
        "Computer Vision", "Natural Language Processing", "Time Series Forecasting",
        "Reinforcement Learning", "Audio Processing", "Recommendation Systems",
        "Healthcare AI", "Autonomous Systems", "Fraud Detection", "Generative AI",
        "Edge AI & Mobile", "Drug Discovery"
    ]
    for domain in domains:
        print(f"  ✓ {domain}")

if __name__ == "__main__":
    populate_sample_experiments()
