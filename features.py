"""
Feature extraction module for password strength analysis.
This module extracts various features from passwords that will be used by the ML model.
"""

import re
from collections import Counter


def extract_features(password):
    """
    Extract features from a password for ML model input.
    
    Args:
        password (str): The password to analyze
    
    Returns:
        dict: Dictionary containing extracted features
    """
    features = {}
    
    # Feature 1: Length of password
    features['length'] = len(password)
    
    # Feature 2: Number of uppercase letters
    features['uppercase_count'] = sum(1 for c in password if c.isupper())
    
    # Feature 3: Number of lowercase letters
    features['lowercase_count'] = sum(1 for c in password if c.islower())
    
    # Feature 4: Number of digits
    features['digit_count'] = sum(1 for c in password if c.isdigit())
    
    # Feature 5: Number of special characters
    special_chars = r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]'
    features['special_count'] = len(re.findall(special_chars, password))
    
    # Feature 6: Presence of repeated characters (consecutive)
    features['has_repeated_chars'] = int(bool(re.search(r'(.)\1', password)))
    
    # Feature 7: Count of repeated characters
    char_counts = Counter(password)
    features['repeated_chars_count'] = sum(1 for count in char_counts.values() if count > 1)
    
    # Feature 8: Presence of common dictionary words
    common_words = ['password', 'admin', 'user', 'login', 'welcome', 'test', 
                    '1234', '12345', '123456', 'qwerty', 'abc', 'letmein']
    features['has_common_words'] = int(any(word in password.lower() for word in common_words))
    
    # Feature 9: Character variety score (ratio of unique characters)
    features['char_variety'] = len(set(password)) / len(password) if len(password) > 0 else 0
    
    # Feature 10: Has both upper and lowercase
    features['has_mixed_case'] = int(features['uppercase_count'] > 0 and features['lowercase_count'] > 0)
    
    # Feature 11: Has letters and digits
    features['has_letters_and_digits'] = int(features['digit_count'] > 0 and 
                                             (features['uppercase_count'] > 0 or features['lowercase_count'] > 0))
    
    return features


def get_feature_vector(password):
    """
    Convert password features to a numerical vector for ML model.
    
    Args:
        password (str): The password to analyze
    
    Returns:
        list: List of feature values in consistent order
    """
    features = extract_features(password)
    
    # Return features in a consistent order
    return [
        features['length'],
        features['uppercase_count'],
        features['lowercase_count'],
        features['digit_count'],
        features['special_count'],
        features['has_repeated_chars'],
        features['repeated_chars_count'],
        features['has_common_words'],
        features['char_variety'],
        features['has_mixed_case'],
        features['has_letters_and_digits']
    ]


def get_feature_names():
    """
    Get the names of all features in the order they appear in the feature vector.
    
    Returns:
        list: List of feature names
    """
    return [
        'length',
        'uppercase_count',
        'lowercase_count',
        'digit_count',
        'special_count',
        'has_repeated_chars',
        'repeated_chars_count',
        'has_common_words',
        'char_variety',
        'has_mixed_case',
        'has_letters_and_digits'
    ]
