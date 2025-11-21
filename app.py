import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from utils import generate_content_from_gemini
from dotenv import load_dotenv
import pathlib
import json

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESUME_FOLDER'] = 'Resume'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_very_secret_key')
ALLOWED_EXTENSIONS = {'html', 'pdf'}
JSON_RESUME = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'html_file' not in request.files or 'my_resume' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        html_file = request.files['html_file']
        resume_file = request.files['my_resume']

        if html_file.filename == '' or resume_file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if (html_file and allowed_file(html_file.filename)) and (resume_file and allowed_file(resume_file.filename)):
            # Generate timestamped filenames
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y/%m/%d_%H-%M-%S")

            html_filename = secure_filename(f"{timestamp}_{html_file.filename}")
            resume_filename = secure_filename(f"{timestamp}_{resume_file.filename}")

            html_filepath = os.path.join(app.config['UPLOAD_FOLDER'], html_filename)
            resume_filepath = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
           
            # Save the files
            html_file.save(html_filepath)
            resume_file.save(resume_filepath)


            # Determine MIME type and call Gemini
            if resume_filename.rsplit('.', 1)[1].lower() == 'html':
                mime_type = 'text/html'
            elif resume_filename.rsplit('.', 1)[1].lower() == 'pdf':
                mime_type = 'application/pdf'
            else:  # Should not happen due to allowed_file, but good to have
                flash('Invalid file type for my_resume.', 'danger')
                return redirect(request.url)
            
            html_filepath = pathlib.Path(html_filepath)
            resume_filepath = pathlib.Path(resume_filepath)

            response_text = generate_content_from_gemini(html_filepath, resume_filepath, mime_type)

            if response_text:
                 flash("Gemini API Responded", "success")
                 global JSON_RESUME
                 try:
                     # Try to find JSON block if mixed with text, though utils tries to clean it
                     start_idx = response_text.find("{")
                     end_idx = response_text.rfind("}")
                     if start_idx != -1 and end_idx != -1:
                         JSON_RESUME = response_text[start_idx:end_idx+1]
                     else:
                         JSON_RESUME = response_text # Assume it's pure JSON
                 except Exception:
                     JSON_RESUME = response_text

                 return redirect(url_for('home', processed='true'))
            else:
                flash("Error processing files with Gemini API.", "danger")
            return redirect(request.url)

        else:
            flash('Invalid file type.', 'danger')
            return redirect(request.url)
    return render_template('home.html')

@app.route('/view_resume')
def view_resume():
    try:
        global JSON_RESUME
        print(JSON_RESUME)
        resume_data = json.loads(JSON_RESUME)  # Parse the JSON string
    except json.JSONDecodeError:
        return "Error: Invalid JSON data", 500  # Handle JSON parsing errors

    
    rendered = render_template('base_resume.html', **resume_data)
    
    pdf_path=os.path.join(app.config['RESUME_FOLDER'], str(resume_data["personal_info"]["name"]+"_"+resume_data["personal_info"]["title"]+".pdf"))

    return rendered

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESUME_FOLDER'], exist_ok=True)
    app.run(debug=True)