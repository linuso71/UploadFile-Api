from flask import Flask,request,render_template,session,redirect,url_for,jsonify,send_from_directory,abort
from dbhelper import DB
import uuid
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.abspath('uploads')
dbo = DB()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/perform_registration',methods=['post'])
def perform_registration():
    name = request.form.get('user_name')
    email = request.form.get('user_email')
    password = request.form.get('user_password')

    response = dbo.register(name, email, password)

    if response:
        return render_template('login.html',message = 'Registration Successful. Kindly login now' )
    else:
        return render_template('register.html',message = 'Email already exist')


@app.route('/perform_login',methods=['post'])
def perform_login():
    email = request.form.get('user_email')
    password = request.form.get('user_password')

    response = dbo.search(email,password)

    if response:
        session['user_id'] = str(uuid.uuid4())
        session['logged_in'] = True
        return render_template('profile.html')
    else:
        return render_template('login.html',message="Incorrect email/password")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('logged_in', None)
    return redirect(url_for('login.html'))

# generate unique filename
def generate_unique_filename(filename):
    return str(uuid.uuid4()) + '_' + filename

@app.route('/upload_page', methods=['GET', 'POST'])
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['GET', 'POST'])
def api_upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Generate a unique filename and save the file
        unique_filename = generate_unique_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)

        dbo.upload_file(unique_filename)
        # Save file information in the database

        return jsonify({'message': 'File successfully uploaded', 'filename': unique_filename})
    except Exception as e:
        return jsonify({'error': f'Error uploading file: {str(e)}'}), 500


@app.route('/files/<filename>', methods=['GET'])
def api_get_file(filename):
    # Retrieve a specific file
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/delete/<filename>', methods=['GET','DELETE'])
def api_delete_file(filename):
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Check if the file exists
        if not os.path.isfile(filepath):
            abort(404, "File not found")

        # Delete the file
        os.remove(filepath)
        dbo.delete_file(filename)

        return jsonify({'message': 'File deleted successfully'})
    except Exception as e:
        return jsonify({'error': f'Error deleting file: {str(e)}'}), 500

@app.route('/update_page', methods=['GET', 'POST'])
def update_file():
    return render_template('update.html')

@app.route('/update',methods=['GET','POST'])
def api_update_file():
    id = request.form.get('text')
    result = dbo.search_file(id)
    if result:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        id = request.form.get('text')

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        try:
            # Generate a unique filename and save the file
            unique_filename = generate_unique_filename(file.filename)
            up_file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(up_file_path)

            dl_filepath = os.path.join(app.config['UPLOAD_FOLDER'], result)
            if not os.path.isfile(dl_filepath):
                abort(404, "File not found")
            os.remove(dl_filepath)
            dbo.update_file(id,unique_filename)

            # Save file information in the database

            return jsonify({'message': 'File successfully updated', 'filename': unique_filename})
        except Exception as e:
            return jsonify({'error': f'Error updating file: {str(e)}'}), 500


app.run(debug=True)