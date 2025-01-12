import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import main

UPLOAD_FOLDER = r"/Users/nathi/OneDrive/Desktop/Pdf Parser Python/uploads/"
ALLOWED_EXTENSIONS = {'pdf'}
FILE_PATHS = []

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            FILE_PATHS.append(UPLOAD_FOLDER + filename)
            print(f"File Paths: {FILE_PATHS}")
            return redirect(url_for('upload_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/combine', methods=['GET'])
def combine_files():
    main.test(FILE_PATHS)
    return '''
    <!doctype html>
    <title>I'm form a different file</title>
    <h1>I'm form a different file</h1>
    '''

if __name__ == "__main__":
    app.run(debug=True)