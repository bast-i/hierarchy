"""Cloud Foundry test"""
from flask import Flask, render_template, Markup, request, redirect, url_for
import os
import json
from werkzeug import secure_filename

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

COLOR = "#33CC33"

# get CF environment variables
#port = int(os.getenv("PORT"))

#VCAP_APPLICATION = json.loads(os.environ['VCAP_APPLICATION'])
#app_instance = int(VCAP_APPLICATION['instance_index'])
#app_guid = VCAP_APPLICATION['application_id']
#app_name = VCAP_APPLICATION['application_name']

#content = '<h1>Hello World!</h1></br>I am instance <strong>#' + str(app_instance) + '</strong> serving application <strong>' + app_name + '</strong> with GUID <strong> ' + app_guid + ' !'
#content = Markup(content)

#@app.route('/')
#def hello_world():
#    return render_template("index.html",bgcolor=COLOR,content=content)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
