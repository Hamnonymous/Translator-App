
# Modules
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QComboBox, QLabel, QHBoxLayout, QVBoxLayout
import asyncio
from PyQt5.QtGui import QFont
from googletrans import Translator
from language import *

class TranslatorApp(QWidget):
    # Main application window for the translator
    def __init__(self):
        super().__init__()
        self.initial_UI()       #Set up the UI components
        self.settings()         #Set up the window settings
        self.clicked_button()   #Connect button events to their respective functions

    def initial_UI(self):
        # Create input and output text boxes, buttons, and combo boxes
        self.input_box = QTextEdit()
        self.output_box = QTextEdit()
        self.input_box.setPlaceholderText("Enter text to translate")
        self.output_box.setPlaceholderText("Translated text will appear here")

        # Create buttons for reversing text, resetting input/output, and submitting translation
        self.reverse = QPushButton("Reverse")
        self.reset = QPushButton("Reset")
        self.submit = QPushButton("Translate")

        # Create language selection combo boxes
        self.input_option = QComboBox()
        self.output_option = QComboBox()

        # Create and style the title label
        self.title = QLabel("Translator")
        self.title.setFont(QFont("Serif", 45))

        # Add language options to combo boxes
        self.input_option.addItems(values)
        self.output_option.addItems(values)

        # Set default language to English
        if "english" in values:
            english_index = values.index("english")
            self.input_option.setCurrentIndex(english_index)
            self.output_option.setCurrentIndex(english_index)

        # Layout Setup
        self.master = QHBoxLayout()

        col1 = QVBoxLayout()        # For input box
        col2 = QVBoxLayout()        # For buttons and language options
        col3 = QVBoxLayout()        # For output box

        # Add widgets to the layouts
        col2.addWidget(self.reverse)
        col2.addWidget(self.title)
        col2.addWidget(self.input_option)
        col2.addWidget(self.output_option)
        col2.addWidget(self.submit)
        col2.addWidget(self.reset)

        col1.addWidget(self.input_box)
        col3.addWidget(self.output_box)

        # Add columns to the main layout
        self.master.addLayout(col1, 40)
        self.master.addLayout(col2, 20)
        self.master.addLayout(col3, 40)

        self.setLayout(self.master)

        # Set the stylesheet for the application
        self.setStyleSheet("""
            QWidget {
                background-color: #8C4799; 
                color: white; 
                font-size: 20px;
            }

            QPushButton {
                background-color: #D00070; 
                color: white; 
                border: none; 
                padding: 10px 20px; 
                font-size: 16px; 
            }

            QPushButton:hover {
                background-color: #9C1954; 
            }
                           
            QLabel {
                color: white;
                font-size: 45px;
                font-weight: bold;
            }
        """)
        
        

    def settings(self):
        # Set the window title and size
        self.setWindowTitle("Translator")
        self.setGeometry(100, 100, 800, 600)
        

    def clicked_button(self):
        # Connect button clicks to their respective functions
        self.submit.clicked.connect(self.translate_C)
        self.reset.clicked.connect(self.reset_all)
        self.reverse.clicked.connect(self.reverse_all)

    async def translate_t(self, text, dest_lang, src_lang):
        """
        Asynchronous translation function.
        Uses googletrans to translate text from src_lang to dest_lang.
        """
        speaker = Translator()
        try:
            # Await the translation process
            translated = await speaker.translate(text, dest=dest_lang, src=src_lang)
            return translated.text
        except Exception as e:
            print(f"Error during translation: {e}")
            return "Translation Error"

    def translate_C(self):
        """
        Handles translation when the Translate button is clicked.
        Gets selected languages and input text, performs translation, and displays result.
        """
        try:
            value_key1 = self.output_option.currentText()
            value_key2 = self.input_option.currentText()

            # Find language codes from names
            key_value1 = [key for key, value in LANGUAGES.items() if value == value_key1]
            key_value2 = [key for key, value in LANGUAGES.items() if value == value_key2]

            # Run the async translation function
            loop = asyncio.get_event_loop()
            self.script = loop.run_until_complete(self.translate_t(self.input_box.toPlainText(), key_value1[0], key_value2[0]))
            self.output_box.setText(self.script)
        except Exception as e:
            print(f"Error during translation: {e}")
            self.output_box.setText("Translation Error")

    def reset_all(self):
        # Clears both input and output text boxes
        self.input_box.clear()
        self.output_box.clear()

    def reverse_all(self):
        # Swaps the text and languages between input and output boxes
        statem1, lang1 = self.input_box.toPlainText(),self.input_option.currentText()
        statem2, lang2 = self.output_box.toPlainText(), self.output_option.currentText()

        self.input_box.setText(statem2)
        self.output_box.setText(statem1)
        self.input_option.setCurrentText(lang2)
        self.output_option.setCurrentText(lang1)


# Main execution block to run the application
if __name__ in "__main__":
    app = QApplication([])
    main = TranslatorApp()
    main.show()
    app.exec_()
    