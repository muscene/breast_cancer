SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database.db'  # SQLite database file
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking to save memory

UPLOAD_FOLDER = 'uploads/'  # Directory to store uploaded files
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'png', 'jpeg'}  # Allowed file types
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB file size limit
LOG_FILENAME = 'app.log'  # Log file name
DEBUG = True  # Enable debug mode
HOST = '0.0.0.0'  # Host to bind the app to
PORT = 5000  # Port to run the app on
