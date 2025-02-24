import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask import send_from_directory

app = Flask(__name__)

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///patients.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db = SQLAlchemy(app)

# Database Model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    nid = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    image1 = db.Column(db.String(200), nullable=True)
    image2 = db.Column(db.String(200), nullable=True)
    image3 = db.Column(db.String(200), nullable=True)
    decision = db.Column(db.String(100), nullable=True)

# Create the database
with app.app_context():
    db.create_all()

def save_image(file):
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        return filename
    return None

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        nid = request.form["nid"]
        email = request.form["email"]
        gender = request.form["gender"]
        age = request.form["age"]
        decision = request.form["decision"]

        # Save images
        image1 = save_image(request.files["image1"])
        image2 = save_image(request.files["image2"])
        image3 = save_image(request.files["image3"])

        new_patient = Patient(
            name=name, phone=phone, nid=nid, email=email, gender=gender, age=age,
            image1=image1, image2=image2, image3=image3, decision=decision
        )
        db.session.add(new_patient)
        db.session.commit()

        return redirect(url_for("success"))

    return render_template("register.html")

@app.route("/success")
def success():
    patients = Patient.query.all()
    return render_template("success.html", patients=patients)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route('/patients')
def patients():
    patients = Patient.query.all()  # Assuming you have a Patient model
    return render_template('patients.html', patients=patients)
@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        
        file = request.files["file"]
        
        if file.filename == "":
            return "No selected file"
        
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            return render_template("index.html", uploaded_file=file.filename)

    return render_template("index.html", uploaded_file=None)

# @app.route("/uploads/<filename>")
# def uploaded_file(filename):
#     return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
