"""
Password improvement suggestions module.
This module provides specific recommendations to improve password strength.
"""

from features import extract_features


def generate_suggestions(password, predicted_strength):
    """
    Generate personalized suggestions to improve password strength.
    
    Args:
        password (str): The password to analyze
        predicted_strength (str): The predicted strength ('Weak', 'Medium', or 'Strong')
    
    Returns:
        list: List of suggestion strings
    """
    suggestions = []
    features = extract_features(password)
    
    # Check password length
    if features['length'] < 8:
        suggestions.append("⚠ Password is too short. Aim for at least 8-12 characters.")
    elif features['length'] < 12:
        suggestions.append("💡 Consider making your password longer (12+ characters) for better security.")
    
    # Check for uppercase letters
    if features['uppercase_count'] == 0:
        suggestions.append("⚠ Add uppercase letters (A-Z) to strengthen your password.")
    
    # Check for lowercase letters
    if features['lowercase_count'] == 0:
        suggestions.append("⚠ Add lowercase letters (a-z) to strengthen your password.")
    
    # Check for digits
    if features['digit_count'] == 0:
        suggestions.append("⚠ Add digits (0-9) to improve security.")
    elif features['digit_count'] < 2 and predicted_strength != 'Strong':
        suggestions.append("💡 Add more digits for better password complexity.")
    
    # Check for special characters
    if features['special_count'] == 0:
        suggestions.append("⚠ Add special characters (!@#$%^&*) to significantly boost password strength.")
    elif features['special_count'] < 2 and predicted_strength != 'Strong':
        suggestions.append("💡 Add more special characters for enhanced security.")
    
    # Check for repeated characters
    if features['has_repeated_chars'] == 1:
        suggestions.append("⚠ Avoid repeating characters consecutively (e.g., 'aa', '111').")
    
    # Check for common words
    if features['has_common_words'] == 1:
        suggestions.append("⚠ Avoid using common dictionary words or predictable patterns.")
    
    # Check character variety
    if features['char_variety'] < 0.6:
        suggestions.append("💡 Use a more diverse set of characters for better entropy.")
    
    # Check for mixed case
    if features['has_mixed_case'] == 0:
        suggestions.append("⚠ Mix uppercase and lowercase letters for stronger security.")
    
    # Check for letters and digits combination
    if features['has_letters_and_digits'] == 0:
        suggestions.append("⚠ Combine both letters and numbers in your password.")
    
    # If strong, provide positive feedback
    if predicted_strength == 'Strong' and len(suggestions) == 0:
        suggestions.append("✅ Excellent! Your password is strong.")
        suggestions.append("💡 Remember to never reuse this password across different accounts.")
        suggestions.append("💡 Consider using a password manager to store it securely.")
    
    # If no specific issues but not strong
    if len(suggestions) == 0 and predicted_strength != 'Strong':
        suggestions.append("💡 Your password is decent, but there's room for improvement.")
        suggestions.append("💡 Try adding more character variety and length.")
    
    return suggestions


def print_suggestions(suggestions):
    """
    Print suggestions in a formatted way.
    
    Args:
        suggestions (list): List of suggestion strings
    """
    if suggestions:
        print("\n" + "="*60)
        print("📋 SUGGESTIONS FOR IMPROVEMENT")
        print("="*60)
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")
        print("="*60)
