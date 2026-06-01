"""
GUI Module for Intelligent Password Strength Checker
This module contains all the UI layout and interaction logic using ttkbootstrap.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import ttkbootstrap as ttk_boot
from ttkbootstrap.constants import *
from model import train_model_if_needed
from features import extract_features
from suggestions import generate_suggestions


class PasswordStrengthCheckerGUI:
    """
    Main GUI application for Password Strength Checker.
    Uses ttkbootstrap for modern, professional appearance.
    """
    
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root: The main tkinter window
        """
        self.root = root
        self.root.title("🔐 Intelligent Password Strength Checker")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Load or train the ML model
        self.classifier = None
        self.load_model()
        
        # Create the UI components
        self.create_widgets()
        
        # Center window on screen
        self.center_window()
    
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def load_model(self):
        """Load or train the ML model with progress indication."""
        self.classifier = train_model_if_needed()
    
    def create_widgets(self):
        """Create and layout all GUI components."""
        
        # Main container with padding
        main_frame = ttk_boot.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # ==================== HEADER ====================
        header_frame = ttk_boot.Frame(main_frame)
        header_frame.pack(fill=X, pady=(0, 20))
        
        # Title
        title_label = ttk_boot.Label(
            header_frame,
            text="🔐 Intelligent Password Strength Checker",
            font=("Helvetica", 24, "bold"),
            bootstyle="success"
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = ttk_boot.Label(
            header_frame,
            text="Powered by Machine Learning (Random Forest Classifier)",
            font=("Helvetica", 11),
            bootstyle="secondary"
        )
        subtitle_label.pack(pady=(5, 0))
        
        # ==================== INPUT SECTION ====================
        input_frame = ttk_boot.Labelframe(
            main_frame,
            text="📝 Enter Password",
            padding=15,
            bootstyle="primary"
        )
        input_frame.pack(fill=X, pady=(0, 20))
        
        # Password input field
        self.password_var = tk.StringVar()
        self.password_entry = ttk_boot.Entry(
            input_frame,
            textvariable=self.password_var,
            font=("Courier", 14),
            show="*",
            bootstyle="primary"
        )
        self.password_entry.pack(fill=X, pady=(0, 10))
        self.password_entry.bind('<Return>', lambda e: self.check_password())
        
        # Show/Hide password checkbox
        self.show_password_var = tk.BooleanVar(value=False)
        show_password_check = ttk_boot.Checkbutton(
            input_frame,
            text="Show Password",
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
            bootstyle="primary-round-toggle"
        )
        show_password_check.pack(anchor=W)
        
        # ==================== BUTTON SECTION ====================
        button_frame = ttk_boot.Frame(main_frame)
        button_frame.pack(fill=X, pady=(0, 20))
        
        # Check Strength Button (primary action)
        self.check_button = ttk_boot.Button(
            button_frame,
            text="🔍 Check Password Strength",
            command=self.check_password,
            bootstyle="success",
            width=30
        )
        self.check_button.pack(side=LEFT, padx=(0, 10))
        
        # Clear Button
        clear_button = ttk_boot.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_all,
            bootstyle="secondary",
            width=15
        )
        clear_button.pack(side=LEFT)
        
        # ==================== RESULTS SECTION ====================
        results_frame = ttk_boot.Labelframe(
            main_frame,
            text="📊 Analysis Results",
            padding=15,
            bootstyle="info"
        )
        results_frame.pack(fill=BOTH, expand=YES, pady=(0, 20))
        
        # Strength indicator (large display)
        self.strength_label = ttk_boot.Label(
            results_frame,
            text="Enter a password to analyze",
            font=("Helvetica", 20, "bold"),
            bootstyle="secondary"
        )
        self.strength_label.pack(pady=(0, 15))
        
        # Confidence meters frame
        confidence_frame = ttk_boot.Frame(results_frame)
        confidence_frame.pack(fill=X, pady=(0, 15))
        
        # Create progress bars for each strength level
        self.confidence_bars = {}
        strength_levels = [
            ("Weak", "danger"),
            ("Medium", "warning"),
            ("Strong", "success")
        ]
        
        for strength, style in strength_levels:
            level_frame = ttk_boot.Frame(confidence_frame)
            level_frame.pack(fill=X, pady=5)
            
            label = ttk_boot.Label(
                level_frame,
                text=f"{strength}:",
                width=10,
                font=("Helvetica", 11)
            )
            label.pack(side=LEFT, padx=(0, 10))
            
            progressbar = ttk_boot.Progressbar(
                level_frame,
                length=500,
                mode='determinate',
                bootstyle=style
            )
            progressbar.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))
            
            percentage_label = ttk_boot.Label(
                level_frame,
                text="0.0%",
                width=8,
                font=("Helvetica", 11, "bold")
            )
            percentage_label.pack(side=LEFT)
            
            self.confidence_bars[strength] = {
                'bar': progressbar,
                'label': percentage_label
            }
        
        # Features display
        features_inner_frame = ttk_boot.Frame(results_frame)
        features_inner_frame.pack(fill=X, pady=(10, 0))
        
        features_title = ttk_boot.Label(
            features_inner_frame,
            text="🔍 Password Features:",
            font=("Helvetica", 12, "bold")
        )
        features_title.pack(anchor=W, pady=(0, 5))
        
        self.features_text = scrolledtext.ScrolledText(
            features_inner_frame,
            height=6,
            font=("Courier", 10),
            wrap=tk.WORD,
            state='disabled',
            bg='#f8f9fa'
        )
        self.features_text.pack(fill=BOTH, expand=YES)
        
        # ==================== SUGGESTIONS SECTION ====================
        suggestions_frame = ttk_boot.Labelframe(
            main_frame,
            text="💡 Suggestions for Improvement",
            padding=15,
            bootstyle="warning"
        )
        suggestions_frame.pack(fill=BOTH, expand=YES)
        
        self.suggestions_text = scrolledtext.ScrolledText(
            suggestions_frame,
            height=8,
            font=("Helvetica", 11),
            wrap=tk.WORD,
            state='disabled',
            bg='#fff9e6'
        )
        self.suggestions_text.pack(fill=BOTH, expand=YES)
    
    def toggle_password_visibility(self):
        """Toggle password visibility in the entry field."""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def check_password(self):
        """
        Main function to check password strength and update UI.
        Called when user clicks the Check button or presses Enter.
        """
        password = self.password_var.get()
        
        # Validate input
        if not password:
            self.show_error("Please enter a password!")
            return
        
        try:
            # Extract features
            features = extract_features(password)
            
            # Predict strength
            predicted_strength, confidence_scores = self.classifier.predict(password)
            
            # Update UI with results
            self.display_strength(predicted_strength)
            self.update_confidence_bars(confidence_scores)
            self.display_features(features)
            
            # Generate and display suggestions
            suggestions = generate_suggestions(password, predicted_strength)
            self.display_suggestions(suggestions, predicted_strength)
            
        except Exception as e:
            self.show_error(f"Error analyzing password: {str(e)}")
    
    def display_strength(self, strength):
        """
        Update the main strength label with appropriate styling.
        
        Args:
            strength (str): Predicted strength (Weak/Medium/Strong)
        """
        strength_config = {
            'Weak': {
                'emoji': '🔴',
                'style': 'danger',
                'text': 'WEAK PASSWORD'
            },
            'Medium': {
                'emoji': '🟡',
                'style': 'warning',
                'text': 'MEDIUM PASSWORD'
            },
            'Strong': {
                'emoji': '🟢',
                'style': 'success',
                'text': 'STRONG PASSWORD'
            }
        }
        
        config = strength_config.get(strength, strength_config['Weak'])
        self.strength_label.config(
            text=f"{config['emoji']} {config['text']}",
            bootstyle=config['style']
        )
    
    def update_confidence_bars(self, confidence_scores):
        """
        Update the confidence progress bars.
        
        Args:
            confidence_scores (dict): Dictionary of confidence scores
        """
        for strength in ['Weak', 'Medium', 'Strong']:
            confidence = confidence_scores.get(strength, 0) * 100
            self.confidence_bars[strength]['bar']['value'] = confidence
            self.confidence_bars[strength]['label'].config(
                text=f"{confidence:.1f}%"
            )
    
    def display_features(self, features):
        """
        Display extracted password features.
        
        Args:
            features (dict): Dictionary of extracted features
        """
        self.features_text.config(state='normal')
        self.features_text.delete(1.0, tk.END)
        
        feature_text = f"""
Length: {features['length']} characters
Uppercase Letters: {features['uppercase_count']}
Lowercase Letters: {features['lowercase_count']}
Digits: {features['digit_count']}
Special Characters: {features['special_count']}
Character Variety: {features['char_variety']:.1%}
Has Mixed Case: {'Yes' if features['has_mixed_case'] else 'No'}
Contains Common Words: {'Yes' if features['has_common_words'] else 'No'}
Has Repeated Characters: {'Yes' if features['has_repeated_chars'] else 'No'}
        """.strip()
        
        self.features_text.insert(1.0, feature_text)
        self.features_text.config(state='disabled')
    
    def display_suggestions(self, suggestions, strength):
        """
        Display improvement suggestions.
        
        Args:
            suggestions (list): List of suggestion strings
            strength (str): Password strength level
        """
        self.suggestions_text.config(state='normal')
        self.suggestions_text.delete(1.0, tk.END)
        
        if not suggestions:
            self.suggestions_text.insert(1.0, "No suggestions available.")
        else:
            suggestion_text = "\n\n".join(f"{i}. {s}" for i, s in enumerate(suggestions, 1))
            self.suggestions_text.insert(1.0, suggestion_text)
        
        self.suggestions_text.config(state='disabled')
    
    def show_error(self, message):
        """
        Display an error message.
        
        Args:
            message (str): Error message to display
        """
        self.strength_label.config(
            text=f"⚠️ {message}",
            bootstyle="danger"
        )
    
    def clear_all(self):
        """Clear all input and output fields."""
        self.password_var.set("")
        self.strength_label.config(
            text="Enter a password to analyze",
            bootstyle="secondary"
        )
        
        # Reset confidence bars
        for strength in ['Weak', 'Medium', 'Strong']:
            self.confidence_bars[strength]['bar']['value'] = 0
            self.confidence_bars[strength]['label'].config(text="0.0%")
        
        # Clear text areas
        self.features_text.config(state='normal')
        self.features_text.delete(1.0, tk.END)
        self.features_text.config(state='disabled')
        
        self.suggestions_text.config(state='normal')
        self.suggestions_text.delete(1.0, tk.END)
        self.suggestions_text.config(state='disabled')
        
        # Focus back to password entry
        self.password_entry.focus()


def launch_gui():
    """
    Launch the GUI application.
    This is the main entry point for the GUI version.
    """
    # Create root window with modern theme
    root = ttk_boot.Window(themename="flatly")  # Modern flat theme
    
    # Create application
    app = PasswordStrengthCheckerGUI(root)
    
    # Start the GUI event loop
    root.mainloop()


if __name__ == '__main__':
    launch_gui()
