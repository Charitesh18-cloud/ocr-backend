# OCR + Translation Flutter App

## Backend Setup

1. Clone the backend repository or copy the `main.py` file.
2. Ensure the following Python packages are installed:

```bash
pip install fastapi uvicorn pillow pytesseract pdf2image requests python-multipart pydantic
Install Tesseract OCR and language traineddata files:

For Windows: https://github.com/UB-Mannheim/tesseract/wiki

Make sure to include all required .traineddata files inside the tessdata folder.

Add Tesseract to system PATH.

Start the FastAPI server:

bash
Copy
Edit
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
Frontend Setup (Flutter)
Open your Flutter project in VS Code or Android Studio.

Update IP address in 2_uploadextract.dart:

dart
Copy
Edit
final apiUrl = 'http://<your_ip>:8000/ocr';
final apiUrl = 'http://<your_ip>:8000/translate';
Run the app:

bash
Copy
Edit
flutter run
Notes
This app uses Deep Translate API for language translation.


Make sure OCR .traineddata files for languages like tel, hin, tam, etc., are placed inside the Tesseract data directory.

App supports image and PDF OCR and translates to 20+ languages.

Requirements
text
Copy
Edit
fastapi
uvicorn
pillow
pytesseract
pdf2image
requests
python-multipart
pydantic
Also required:

Tesseract OCR installed and accessible in PATH

Corresponding .traineddata files placed inside tessdata directory

Firestore (Optional)
If using Firebase Auth and Firestore in Flutter:

Setup Firebase project

Add Firebase config files (google-services.json / firebase_options.dart)

Enable Authentication (Google Sign-in)

Setup Firestore rules for saving saved_docs

kotlin
Copy
Edit

Let me know if you want this content zipped or uploaded as a downloadable file too.