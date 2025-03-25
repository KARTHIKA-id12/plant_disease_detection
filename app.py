from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import torch
import torch.nn.functional as F
from models.model import load_model
from utils.preprocessing import preprocess_image, save_uploaded_image
import google.generativeai as genai
import base64
import config  # ✅ Import config.py

# ✅ Initialize Flask App
app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ✅ Load AI Model Properly
MODEL_PATH = "models/resnet_leaf_disease.pth"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = load_model(MODEL_PATH).to(device)
model.eval()  # ✅ Set Model to Evaluation Mode

# ✅ Configure Google Gemini API (Using API Key from config.py)
genai.configure(api_key=config.GEMINI_API_KEY)
model_gemini = genai.GenerativeModel("gemini-2.0-pro-exp") 


# ✅ Ensure Upload Directory Exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🌿 **Home Page**
@app.route("/")
def home():
    return render_template("home.html")

# 📤 **Upload Page**
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("image")
        captured_image = request.form.get("captured_image")

        filename, error = None, None

        if file and file.filename:
            filename, error = save_uploaded_image(file)
        elif captured_image:
            filename = "captured_image.png"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            try:
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(captured_image.split(",")[1]))
            except Exception as e:
                flash(f"Error saving captured image: {str(e)}", "error")
                return redirect(url_for("upload"))

        if error:
            flash(error, "error")
            return redirect(url_for("upload"))

        return redirect(url_for("analysis", image_path=filename))

    return render_template("upload.html")

# 🔬 **Analysis Page (Prediction)**
@app.route("/analysis")
def analysis():
    image_path = request.args.get("image_path")

    if not image_path:
        flash("No image found! Please upload an image first.", "error")
        return redirect(url_for("upload"))

    full_image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_path)

    if not os.path.exists(full_image_path):
        flash("Error: Uploaded image not found!", "error")
        return redirect(url_for("upload"))

    # ✅ Preprocess Image
    processed_image = preprocess_image(full_image_path).to(device)

    # ✅ Perform AI Prediction
    try:
        with torch.no_grad():
            output = model(processed_image)
            probabilities = F.softmax(output, dim=1).squeeze(0)

        predicted_index = torch.argmax(probabilities).item()
        confidence_score = round(probabilities[predicted_index].item() * 100, 2)  # ✅ Confidence Score

        # ✅ Disease Labels
        disease_labels = [
            "Healthy", "Bacterial Spot", "Early Blight", 
            "Late Blight", "Leaf Mold", "Septoria Leaf Spot",
            "Target Spot", "Yellow Leaf Curl Virus", "Mosaic Virus",
            "Powdery Mildew", "Rust", "Anthracnose", "Downy Mildew"
        ]

        predicted_label = disease_labels[predicted_index] if predicted_index < len(disease_labels) else "Unknown"

        return render_template("analysis.html", image_url=url_for('static', filename=f'uploads/{image_path}'), 
                               disease=predicted_label, confidence=confidence_score)

    except Exception as e:
        flash(f"Prediction error: {str(e)}", "error")
        return redirect(url_for("upload"))

# 🤖 **Chatbot Route**
@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_message = request.form.get("message")

    try:
        response = model_gemini.generate_content(user_message)
        bot_reply = response.text if hasattr(response, "text") else "Sorry, the chatbot could not process your request."
    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    return jsonify({"reply": bot_reply})

# ⭐ **Feedback Submission**
@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    rating = request.form.get("rating")
    feedback = request.form.get("feedback")

    if not rating or not feedback:
        return jsonify({"status": "error", "message": "Please provide both rating and feedback."})

    try:
        with open("feedback.txt", "a") as f:
            f.write(f"Rating: {rating}/5 | Feedback: {feedback}\n")

        return jsonify({"status": "success", "message": "Thank you for your feedback!"})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error saving feedback: {str(e)}"})

# 🚀 **Run Flask App**
if __name__ == "__main__":
    app.run(debug=True)




