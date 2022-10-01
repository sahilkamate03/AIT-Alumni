import os

from requests import request
import os
from werkzeug import secure_filename

app.config['UPLOAD_FOLDER']=params['upload_location']

@app.route('/uploader', methods= ['GET','POST'])
@login_required
def uploader():
    if  (request.method=='POST'):
        f=request.files['file1']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        return "uploaded successfully"