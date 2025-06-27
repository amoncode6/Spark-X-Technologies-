from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os, json

app = Flask(__name__)
app.config['UPLOAD_FOLDER_IMAGES'] = 'static/uploads/images'
app.config['UPLOAD_FOLDER_ZIPS'] = 'static/uploads/zips'
app.config['PROJECTS_FILE'] = 'projects.json'

@app.route('/')
def index():
    with open(app.config['PROJECTS_FILE'], 'r') as f:
        projects = json.load(f)
    return render_template('index.html', projects=projects)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        github_link = request.form['github']
        demo_link = request.form['demo']

        image = request.files['image']
        zip_file = request.files['zip_file']
        img_filename = secure_filename(image.filename)
        zip_filename = secure_filename(zip_file.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], img_filename))
        zip_file.save(os.path.join(app.config['UPLOAD_FOLDER_ZIPS'], zip_filename))

        new_project = {
            'title': title,
            'description': description,
            'image': f'static/uploads/images/{img_filename}',
            'zip': f'static/uploads/zips/{zip_filename}',
            'github': github_link,
            'demo': demo_link
        }

        with open(app.config['PROJECTS_FILE'], 'r+') as f:
            data = json.load(f)
            data.insert(0, new_project)
            f.seek(0)
            json.dump(data, f, indent=4)

        return redirect(url_for('index'))

    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
