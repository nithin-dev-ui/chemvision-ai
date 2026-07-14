from PIL import Image
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# =========================
# GEMINI SETUP
# =========================

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# =========================
# AI ASSISTANT
# =========================

@app.route("/assistant", methods=["GET", "POST"])
def assistant():

    answer = ""

    if request.method == "POST":

        question = request.form.get("question", "")

        try:

            prompt = f"""
You are ChemVision AI.

You are an expert chemistry assistant.

Answer only chemistry-related questions.

Question:
{question}
"""

            response = model.generate_content(prompt)

            answer = response.text

        except Exception as e:

            answer = f"Error: {str(e)}"

    return render_template(
        "assistant.html",
        answer=answer
    )


# =========================
# AI REACTION PREDICTOR
# =========================

@app.route("/predictor", methods=["GET", "POST"])
def predictor():

    result = ""

    if request.method == "POST":

        reaction = request.form.get("reaction", "")

        try:

            prompt = f"""
You are an expert chemistry reaction prediction AI.

Predict the reaction below.

Reaction:
{reaction}

Provide:

1. Products
2. Reaction Type
3. Short Explanation

Format the answer clearly.
"""

            response = model.generate_content(prompt)

            result = response.text

        except Exception as e:

            result = f"Error: {str(e)}"

    return render_template(
        "predictor.html",
        result=result,
        reaction_type=""
    )


# =========================
# UPLOAD ANALYZER
# =========================

@app.route("/upload", methods=["GET", "POST"])
def upload():

    image_path = ""
    analysis = ""

    if request.method == "POST":

        file = request.files.get("image")

        if file and file.filename:

            filename = secure_filename(file.filename)

            save_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            file.save(save_path)

            image_path = f"/uploads/{filename}"

            try:

                img = Image.open(save_path)

                response = model.generate_content([
                    """
You are ChemVision AI.

Analyze this chemistry-related image.

Provide:
1. What is visible
2. Chemical structures or reactions detected
3. Safety concerns
4. Educational explanation
5. Research insights
""",
                    img
                ])

                analysis = response.text

            except Exception as e:

                analysis = f"AI Analysis Error: {str(e)}"

    return render_template(
        "upload.html",
        image_path=image_path,
        analysis=analysis
    )


# =========================
# AI SAFETY CHECKER
# =========================

@app.route("/safety", methods=["GET", "POST"])
def safety():

    hazard = ""

    if request.method == "POST":

        chemical = request.form.get("chemical", "")

        try:

            prompt = f"""
You are a chemistry safety expert.

Analyze this chemical:

{chemical}

Provide:

1. Hazard Level
2. Corrosive or Not
3. Flammable or Not
4. Toxicity Level
5. Safety Precautions
6. Storage Recommendations

Format clearly.
"""

            response = model.generate_content(prompt)

            hazard = response.text

        except Exception as e:

            hazard = f"Error: {str(e)}"

    return render_template(
        "safety.html",
        hazard=hazard,
        corrosive="",
        flammable="",
        toxicity="",
        recommendation=""
    )


# =========================
# REPORTS
# =========================

@app.route("/reports", methods=["GET", "POST"])
def reports():

    report = ""

    if request.method == "POST":

        experiment = request.form.get(
            "experiment",
            ""
        )

        try:

            prompt = f"""
Generate a professional chemistry laboratory report.

Experiment:
{experiment}

Include:
1. Title
2. Objective
3. Theory
4. Procedure
5. Observation
6. Conclusion
7. Safety Precautions
"""

            response = model.generate_content(prompt)

            report = response.text

        except Exception as e:

            report = f"Error: {str(e)}"

    return render_template(
        "reports.html",
        report=report
    )

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )
if __name__ == "__main__":
    app.run(debug=True)