"""
Machine Learning model module for password strength classification.
This module handles training and prediction using a Random Forest classifier.
"""

import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from features import get_feature_vector, get_feature_names


class PasswordStrengthClassifier:
    """
    Random Forest classifier for password strength prediction.
    """
    
    def __init__(self, model_path='password_model.pkl'):
        """
        Initialize the classifier.
        
        Args:
            model_path (str): Path to save/load the trained model
        """
        self.model_path = model_path
        self.model = None
        self.label_mapping = {'Weak': 0, 'Medium': 1, 'Strong': 2}
        self.reverse_label_mapping = {0: 'Weak', 1: 'Medium', 2: 'Strong'}
    
    def load_dataset(self, csv_path='dataset.csv'):
        """
        Load dataset from CSV file.
        
        Args:
            csv_path (str): Path to the dataset CSV file
        
        Returns:
            tuple: (X, y) features and labels
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Dataset not found: {csv_path}. Please run generate_dataset.py first.")
        
        df = pd.read_csv(csv_path)
        
        # Separate features and labels
        X = df.drop('strength', axis=1).values
        y = df['strength'].map(self.label_mapping).values
        
        print(f"✅ Dataset loaded: {len(df)} samples")
        print(f"📊 Class distribution:")
        for label, count in df['strength'].value_counts().items():
            print(f"   - {label}: {count}")
        
        return X, y
    
    def train(self, csv_path='dataset.csv', test_size=0.2, random_state=42):
        """
        Train the Random Forest classifier on the dataset.
        
        Args:
            csv_path (str): Path to the dataset CSV file
            test_size (float): Proportion of dataset for testing
            random_state (int): Random seed for reproducibility
        """
        print("\n" + "="*60)
        print("🤖 TRAINING PASSWORD STRENGTH CLASSIFIER")
        print("="*60)
        
        # Load dataset
        X, y = self.load_dataset(csv_path)
        
        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        print(f"\n📈 Training samples: {len(X_train)}")
        print(f"📉 Testing samples: {len(X_test)}")
        
        # Initialize and train Random Forest classifier
        print("\n🌲 Training Random Forest Classifier...")
        self.model = RandomForestClassifier(
            n_estimators=100,          # Number of trees in the forest
            max_depth=10,               # Maximum depth of trees
            min_samples_split=5,        # Minimum samples to split a node
            min_samples_leaf=2,         # Minimum samples in leaf node
            random_state=random_state,
            n_jobs=-1                   # Use all CPU cores
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate on test set
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n✅ Model trained successfully!")
        print(f"🎯 Test Accuracy: {accuracy:.2%}")
        
        # Show detailed classification report
        print("\n📊 Classification Report:")
        print("-" * 60)
        target_names = ['Weak', 'Medium', 'Strong']
        print(classification_report(y_test, y_pred, target_names=target_names))
        
        # Feature importance
        self._print_feature_importance()
        
        # Save the model
        self.save_model()
        
        print("="*60)
    
    def _print_feature_importance(self):
        """Print feature importance scores."""
        if self.model is None:
            return
        
        feature_names = get_feature_names()
        importances = self.model.feature_importances_
        
        # Sort by importance
        indices = np.argsort(importances)[::-1]
        
        print("\n🔍 Feature Importance:")
        print("-" * 60)
        for i, idx in enumerate(indices[:5], 1):  # Top 5 features
            print(f"{i}. {feature_names[idx]}: {importances[idx]:.4f}")
    
    def save_model(self):
        """Save the trained model to disk."""
        if self.model is None:
            print("⚠ No model to save.")
            return
        
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"\n💾 Model saved to: {self.model_path}")
    
    def load_model(self):
        """Load a trained model from disk."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model not found: {self.model_path}. Please train the model first.")
        
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)
        print(f"✅ Model loaded from: {self.model_path}")
    
    def predict(self, password):
        """
        Predict the strength of a password.
        
        Args:
            password (str): The password to classify
        
        Returns:
            tuple: (predicted_label, confidence_scores)
        """
        if self.model is None:
            raise ValueError("Model not trained or loaded. Please train or load a model first.")
        
        # Extract features
        features = get_feature_vector(password)
        features_array = np.array(features).reshape(1, -1)
        
        # Predict
        prediction = self.model.predict(features_array)[0]
        predicted_label = self.reverse_label_mapping[prediction]
        
        # Get confidence scores for all classes
        probabilities = self.model.predict_proba(features_array)[0]
        confidence_scores = {
            'Weak': probabilities[0],
            'Medium': probabilities[1],
            'Strong': probabilities[2]
        }
        
        return predicted_label, confidence_scores


def train_model_if_needed():
    """
    Check if model exists, if not, train a new one.
    """
    model_path = 'password_model.pkl'
    dataset_path = 'dataset.csv'
    
    # Check if dataset exists, if not generate it
    if not os.path.exists(dataset_path):
        print("⚠ Dataset not found. Generating synthetic dataset...")
        from generate_dataset import save_dataset_to_csv
        save_dataset_to_csv(dataset_path, num_samples=300)
        print()
    
    # Check if model exists, if not train it
    if not os.path.exists(model_path):
        print("⚠ Model not found. Training new model...")
        classifier = PasswordStrengthClassifier(model_path)
        classifier.train(dataset_path)
        return classifier
    else:
        classifier = PasswordStrengthClassifier(model_path)
        classifier.load_model()
        return classifier


if __name__ == '__main__':
    # Train the model
    classifier = PasswordStrengthClassifier()
    
    # Generate dataset if it doesn't exist
    if not os.path.exists('dataset.csv'):
        print("Generating dataset...")
        from generate_dataset import save_dataset_to_csv
        save_dataset_to_csv('dataset.csv', num_samples=300)
    
    # Train the model
    classifier.train('dataset.csv')
