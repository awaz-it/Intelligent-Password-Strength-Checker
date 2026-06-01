"""
Intelligent Password Strength Checker - Main Entry Point

This is the main entry point for the password strength checker application.
It allows users to check their password strength using a trained ML model
and receive personalized suggestions for improvement.
"""

import sys
import os
from getpass import getpass
from model import train_model_if_needed, PasswordStrengthClassifier
from suggestions import generate_suggestions, print_suggestions
from features import extract_features


def print_banner():
    """Print application banner."""
    print("\n" + "="*60)
    print("🔐 INTELLIGENT PASSWORD STRENGTH CHECKER")
    print("="*60)
    print("   Powered by Machine Learning (Random Forest)")
    print("="*60 + "\n")


def print_password_analysis(password, predicted_strength, confidence_scores, features):
    """
    Print detailed password analysis results.
    
    Args:
        password (str): The password analyzed
        predicted_strength (str): Predicted strength label
        confidence_scores (dict): Confidence scores for each class
        features (dict): Extracted features
    """
    print("\n" + "="*60)
    print("📊 PASSWORD ANALYSIS RESULTS")
    print("="*60)
    
    # Display password (masked)
    masked_password = '*' * len(password)
    print(f"\n🔑 Password: {masked_password} (Length: {len(password)})")
    
    # Display prediction
    strength_colors = {
        'Weak': '🔴',
        'Medium': '🟡',
        'Strong': '🟢'
    }
    color = strength_colors.get(predicted_strength, '⚪')
    print(f"\n{color} Predicted Strength: {predicted_strength.upper()}")
    
    # Display confidence scores
    print("\n📈 Confidence Scores:")
    for label in ['Weak', 'Medium', 'Strong']:
        bar_length = int(confidence_scores[label] * 30)
        bar = '█' * bar_length + '░' * (30 - bar_length)
        percentage = confidence_scores[label] * 100
        print(f"   {label:8s} [{bar}] {percentage:5.1f}%")
    
    # Display key features
    print("\n🔍 Password Features:")
    print(f"   • Length: {features['length']}")
    print(f"   • Uppercase letters: {features['uppercase_count']}")
    print(f"   • Lowercase letters: {features['lowercase_count']}")
    print(f"   • Digits: {features['digit_count']}")
    print(f"   • Special characters: {features['special_count']}")
    print(f"   • Character variety: {features['char_variety']:.2%}")
    
    print("="*60)


def check_password_strength(classifier):
    """
    Interactive password strength checking.
    
    Args:
        classifier: Trained PasswordStrengthClassifier instance
    """
    while True:
        print("\nOptions:")
        print("  1. Check a password")
        print("  2. Show example passwords")
        print("  3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            # Get password input (hidden for security)
            print("\n" + "-"*60)
            password = getpass("Enter password to check (input will be hidden): ")
            
            if not password:
                print("⚠ Password cannot be empty!")
                continue
            
            # Extract features
            features = extract_features(password)
            
            # Predict strength
            predicted_strength, confidence_scores = classifier.predict(password)
            
            # Display analysis
            print_password_analysis(password, predicted_strength, confidence_scores, features)
            
            # Generate and display suggestions
            suggestions = generate_suggestions(password, predicted_strength)
            print_suggestions(suggestions)
            
        elif choice == '2':
            show_example_passwords(classifier)
            
        elif choice == '3':
            print("\n👋 Thank you for using Password Strength Checker!")
            print("💡 Remember: Use strong, unique passwords for each account.\n")
            break
            
        else:
            print("⚠ Invalid choice. Please enter 1, 2, or 3.")


def show_example_passwords(classifier):
    """
    Show example passwords and their strength predictions.
    
    Args:
        classifier: Trained PasswordStrengthClassifier instance
    """
    print("\n" + "="*60)
    print("📝 EXAMPLE PASSWORDS")
    print("="*60)
    
    examples = [
        ("12345", "Very weak - only digits, too short"),
        ("password", "Very weak - common word, no variety"),
        ("Password123", "Medium - has mixed case and digits"),
        ("P@ssw0rd!", "Medium-Strong - good variety but predictable"),
        ("Tr0ub4dor&3", "Strong - good length, mixed characters"),
        ("xK9#mP2$vL5@nQ", "Very strong - high entropy, variety"),
    ]
    
    for pwd, description in examples:
        predicted_strength, confidence_scores = classifier.predict(pwd)
        strength_icons = {'Weak': '🔴', 'Medium': '🟡', 'Strong': '🟢'}
        icon = strength_icons.get(predicted_strength, '⚪')
        
        masked = pwd[:2] + '*' * (len(pwd) - 4) + pwd[-2:] if len(pwd) > 4 else '*' * len(pwd)
        print(f"\n{icon} Password: {masked}")
        print(f"   Description: {description}")
        print(f"   Prediction: {predicted_strength} ({confidence_scores[predicted_strength]*100:.1f}% confidence)")
    
    print("="*60)


def main():
    """Main application entry point."""
    print_banner()
    
    try:
        # Load or train the model
        print("🔄 Initializing classifier...")
        classifier = train_model_if_needed()
        print()
        
        # Start interactive session
        check_password_strength(classifier)
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("💡 Please ensure all required files are present.")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
