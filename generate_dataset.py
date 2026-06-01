"""
Dataset generation script for password strength classifier.
This script generates synthetic passwords with various characteristics and labels them.
"""

import random
import string
import csv
from features import get_feature_vector


def generate_weak_password():
    """Generate a weak password with poor characteristics."""
    patterns = [
        # Short passwords
        ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 6))),
        # Only digits
        ''.join(random.choices(string.digits, k=random.randint(4, 8))),
        # Common patterns
        random.choice(['password', 'admin123', 'user', 'test123', '123456', 'qwerty', 'abc123']),
        # Simple dictionary words
        random.choice(['hello', 'welcome', 'login', 'sample', 'simple']) + random.choice(['', '1', '123']),
        # Repeated characters
        random.choice(string.ascii_lowercase) * random.randint(4, 8),
    ]
    return random.choice(patterns)


def generate_medium_password():
    """Generate a medium strength password."""
    patterns = []
    
    # Length between 8-10, mix of letters and numbers
    pwd = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 7)))
    pwd += ''.join(random.choices(string.digits, k=random.randint(2, 3)))
    patterns.append(''.join(random.sample(pwd, len(pwd))))
    
    # Mix of upper, lower, and digits
    pwd = ''.join(random.choices(string.ascii_uppercase, k=random.randint(2, 3)))
    pwd += ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 5)))
    pwd += ''.join(random.choices(string.digits, k=random.randint(2, 3)))
    patterns.append(''.join(random.sample(pwd, len(pwd))))
    
    # Longer but missing special characters
    pwd = ''.join(random.choices(string.ascii_letters, k=random.randint(8, 10)))
    pwd += ''.join(random.choices(string.digits, k=random.randint(2, 3)))
    patterns.append(''.join(random.sample(pwd, len(pwd))))
    
    return random.choice(patterns)


def generate_strong_password():
    """Generate a strong password with good characteristics."""
    # Long passwords with mixed character types
    pwd = ''
    pwd += ''.join(random.choices(string.ascii_uppercase, k=random.randint(3, 5)))
    pwd += ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 6)))
    pwd += ''.join(random.choices(string.digits, k=random.randint(3, 4)))
    pwd += ''.join(random.choices('!@#$%^&*()_+-=[]{}', k=random.randint(2, 4)))
    
    # Shuffle to mix characters
    pwd_list = list(pwd)
    random.shuffle(pwd_list)
    return ''.join(pwd_list)


def generate_dataset(num_samples=300):
    """
    Generate a synthetic dataset of passwords with labels.
    
    Args:
        num_samples (int): Total number of samples to generate
    
    Returns:
        list: List of tuples (password, label)
    """
    dataset = []
    
    # Generate approximately equal distribution
    samples_per_class = num_samples // 3
    
    # Generate weak passwords
    for _ in range(samples_per_class):
        pwd = generate_weak_password()
        dataset.append((pwd, 'Weak'))
    
    # Generate medium passwords
    for _ in range(samples_per_class):
        pwd = generate_medium_password()
        dataset.append((pwd, 'Medium'))
    
    # Generate strong passwords
    for _ in range(samples_per_class):
        pwd = generate_strong_password()
        dataset.append((pwd, 'Strong'))
    
    # Shuffle dataset
    random.shuffle(dataset)
    
    return dataset


def save_dataset_to_csv(filename='dataset.csv', num_samples=300):
    """
    Generate dataset and save to CSV file with features.
    
    Args:
        filename (str): Output CSV filename
        num_samples (int): Number of samples to generate
    """
    dataset = generate_dataset(num_samples)
    
    # Feature names
    feature_names = [
        'length', 'uppercase_count', 'lowercase_count', 'digit_count',
        'special_count', 'has_repeated_chars', 'repeated_chars_count',
        'has_common_words', 'char_variety', 'has_mixed_case',
        'has_letters_and_digits', 'strength'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(feature_names)
        
        for password, label in dataset:
            features = get_feature_vector(password)
            row = features + [label]
            writer.writerow(row)
    
    print(f"✅ Dataset generated successfully: {filename}")
    print(f"📊 Total samples: {num_samples}")
    print(f"   - Weak: ~{num_samples // 3}")
    print(f"   - Medium: ~{num_samples // 3}")
    print(f"   - Strong: ~{num_samples // 3}")


if __name__ == '__main__':
    # Generate dataset with 300 samples
    save_dataset_to_csv('dataset.csv', num_samples=300)
