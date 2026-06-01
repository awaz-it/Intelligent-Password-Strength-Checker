# 🔐 Intelligent Password Strength Checker

A machine learning-powered password strength checker that uses a Random Forest classifier to evaluate password security and provide personalized improvement suggestions.

## 📋 Features

- **ML-Powered Classification**: Uses Random Forest algorithm to classify passwords as Weak, Medium, or Strong
- **Comprehensive Feature Extraction**: Analyzes 11 different password characteristics including:
  - Length
  - Character composition (uppercase, lowercase, digits, special characters)
  - Character variety and entropy
  - Repeated patterns
  - Common dictionary words
- **Intelligent Suggestions**: Provides personalized recommendations to improve password strength
- **Synthetic Dataset Generation**: Auto-generates training data if not available
- **Interactive CLI**: User-friendly command-line interface
- **Confidence Scores**: Shows probability distribution across all strength categories

## 📁 Project Structure

```
awaz ai/
│
├── main.py                 # Entry point for the application
├── model.py                # Random Forest classifier training and prediction
├── features.py             # Password feature extraction functions
├── suggestions.py          # Password improvement recommendations
├── generate_dataset.py     # Synthetic dataset generation script
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
│
├── dataset.csv            # Training dataset (auto-generated)
└── password_model.pkl     # Trained model (auto-generated)
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Steps

1. **Navigate to the project directory:**
   ```bash
   cd "c:\Users\WAZ\Desktop\awaz ai"
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Running the Application

Simply run the main script:

```bash
python main.py
```

The application will:
1. Check if a trained model exists
2. If not, automatically generate a synthetic dataset (300 samples)
3. Train the Random Forest classifier
4. Launch the interactive password checker

### Interactive Menu

Once running, you'll see three options:

1. **Check a password**: Enter any password to get strength analysis and suggestions
2. **Show example passwords**: View pre-analyzed example passwords
3. **Exit**: Close the application

### Example Session

```
🔐 INTELLIGENT PASSWORD STRENGTH CHECKER
============================================================
   Powered by Machine Learning (Random Forest)
============================================================

Options:
  1. Check a password
  2. Show example passwords
  3. Exit

Enter your choice (1-3): 1

Enter password to check (input will be hidden): ********

📊 PASSWORD ANALYSIS RESULTS
============================================================

🔑 Password: ******** (Length: 8)

🟡 Predicted Strength: MEDIUM

📈 Confidence Scores:
   Weak     [████░░░░░░░░░░░░░░░░░░░░░░░░░░]  13.5%
   Medium   [████████████████████░░░░░░░░░░]  66.2%
   Strong   [██████░░░░░░░░░░░░░░░░░░░░░░░░]  20.3%

🔍 Password Features:
   • Length: 8
   • Uppercase letters: 2
   • Lowercase letters: 4
   • Digits: 2
   • Special characters: 0
   • Character variety: 87.50%

============================================================

📋 SUGGESTIONS FOR IMPROVEMENT
============================================================
1. ⚠ Add special characters (!@#$%^&*) to significantly boost password strength.
2. 💡 Consider making your password longer (12+ characters) for better security.
============================================================
```

## 🎓 Training Your Own Model

### Automatic Training

The model trains automatically on first run. If you want to retrain:

1. Delete the existing model:
   ```bash
   rm password_model.pkl
   ```

2. Run the application again:
   ```bash
   python main.py
   ```

### Manual Training

You can also train the model manually:

```bash
python model.py
```

### Custom Dataset Generation

To generate a custom dataset with a specific number of samples:

```bash
python generate_dataset.py
```

Or modify the script to change the number of samples (default: 300).

## 🔬 How It Works

### 1. Feature Extraction (`features.py`)
The system extracts 11 features from each password:
- Basic metrics (length, character counts)
- Pattern detection (repeated characters, common words)
- Diversity metrics (character variety, mixed case)

### 2. Dataset Generation (`generate_dataset.py`)
Creates synthetic passwords with realistic patterns:
- **Weak**: Short, simple, common patterns
- **Medium**: Decent length, mixed characters, missing some elements
- **Strong**: Long, diverse character types, high entropy

### 3. Model Training (`model.py`)
Uses Random Forest Classifier with:
- 100 decision trees
- 80/20 train-test split
- Stratified sampling for balanced classes

### 4. Prediction & Suggestions (`suggestions.py`)
- Classifies password strength
- Analyzes specific weaknesses
- Generates targeted improvement recommendations

## 📊 Model Performance

The Random Forest classifier typically achieves:
- **Accuracy**: ~85-95% on test set
- **Balanced performance** across all three classes
- **Top features**: Length, special character count, character variety

## 🛠️ Customization

### Adding More Features

Edit `features.py` to add new feature extraction logic:

```python
def extract_features(password):
    features = {}
    # Add your custom feature here
    features['custom_feature'] = your_logic(password)
    return features
```

### Modifying Suggestions

Edit `suggestions.py` to customize recommendations:

```python
def generate_suggestions(password, predicted_strength):
    suggestions = []
    # Add your custom suggestion logic
    return suggestions
```

### Tuning the Model

Edit `model.py` to adjust Random Forest parameters:

```python
self.model = RandomForestClassifier(
    n_estimators=200,      # Increase number of trees
    max_depth=15,          # Increase tree depth
    # ... other parameters
)
```

## 🔒 Security Notes

- **Input Privacy**: Passwords are never logged or stored
- **Masked Display**: Passwords shown as asterisks in output
- **Local Processing**: All analysis happens locally on your machine
- **No Network Calls**: No data sent to external servers

## ⚠️ Limitations

- This is an educational project, not a production-ready security tool
- The model is trained on synthetic data, not real password breaches
- Cannot detect context-specific weaknesses (e.g., personal information)
- Should be used alongside other security practices

## 🤝 Contributing

Feel free to enhance this project by:
- Adding more sophisticated features
- Improving the dataset generation
- Implementing different ML algorithms
- Creating a web interface
- Adding support for password breach databases

## 📝 License

This project is open-source and available for educational purposes.

## 🙏 Acknowledgments

- Built with scikit-learn's Random Forest implementation
- Inspired by password security best practices
- Created as a demonstration of ML in cybersecurity

---

**Remember**: Always use strong, unique passwords for each account, and consider using a password manager! 🔐
