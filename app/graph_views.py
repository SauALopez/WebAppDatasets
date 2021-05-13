from app import app
from flask import render_template, url_for , request , redirect, send_from_directory, abort
from app.models.dataset_model import db, datasets, datetime 
from data_wrangling import Sensors
import os
import pdfkit


@app.route('/')
def index():
    return redirect('/upload-dataset')

def url_keys(keys):
    id  = keys['id']
    key = keys['key']
    url = '/view-dataset?id='+str(id)+'&key='+str(key)
    return url
def correct_file_type(data):
    fileextension = data.filename.split('.')[-1].lower()
    if fileextension == 'txt':
        return True
    else:
        raise Exception(" * BAD FILE TYPE")  

def file_lecture(name):
    s1 = Sensors()
    dataset= open(name)
    for line in dataset:
        sensor_information= line.split(' ')
        if len(sensor_information)==8:
            try:
                measures = {
                    "temperature" : float(sensor_information[4]),
                    "humidity" : float(sensor_information[5]),
                    "light" : float(sensor_information[6]),
                    "voltage" : float(sensor_information[7].rstrip('\n')) 
                }
                s1.data_input(int(sensor_information[3]),measures)
            except:
                pass

    return s1
    


@app.route('/upload-dataset',methods=["GET", "POST"])
def upload_dataset():
    if request.method == 'POST':
        #EXTRAC INFORMATION FROM REQUEST, FORM
        name = request.form['DatasetName']
        date = datetime.strptime(request.form['DatasetDate'],'%Y-%m-%d') 
        description = request.form['DatasetDescription']
        new_dataset = datasets(name= name,date_dataset=date,description= description)
        data_file = request.files['data']

        try:
            #CHECKING CORRECT FILE FORMAT & CHECKING MIN REQUIREMENTS FOR DATASET TO INCLUD
            correct_file_type(data_file)
            #SAVING DATASET INFORMATION IN DATABASE
            db.session.add(new_dataset)
            db.session.commit()
            print(" * DATASET COMMITED TO DATABASE")
            #QUERY TO OBTAIN UNIQUE ID OF DATASET AND SAVING DATA SET
            datasetId = db.session.query(datasets.id).order_by(datasets.date_entry.desc()).first()[0]
            filename = os.path.join(app.config['UPLOADS'],(str(datasetId)+"dataset.txt"))
            data_file.save(filename)
            print(" * DATASET SAVED")
            #REDIRECT TO VIEWDATASET
            return redirect(url_keys({'id':datasetId,'key':app.config['QSTR_DEFAULT']}))
        except Exception as exep:
            #PEN. CATCHING EXEPTION FOR BAD FILE TYPE TO RESPOND WITH ERROR MESSAGE IN FRONT END.
            return redirect('/upload-dataset')

    return render_template('graph/upload-dataset.html')


  


@app.route('/view-dataset',methods=["GET", "POST"])
def view_dataset():
    args = request.args
    datasetId = args['id']
    filename = os.path.join(app.config['UPLOADS'],(str(datasetId)+"dataset.txt"))
    try:
        dataset = file_lecture(filename)
        data = dataset.info(args['key'])
        return render_template('graph/view-dataset.html',id=datasetId, data = data,n_ids = len(data['IDS']),n_keys = len(data['keys']))
    except:
        abort(404)
    


@app.route('/recent-datasets',methods=["GET", "POST"])
def recent_dataset():
    return render_template('graph/recent-dataset.html')

@app.route('/originaldataset')
def original():
    args = request.args
    datasetId = args['id']
    filename = str(datasetId)+"dataset.txt"
    abspath = os.path.realpath(app.config['UPLOADS'])
    try:
        return send_from_directory(
            abspath, filename, as_attachment=True
        )
    except FileNotFoundError:
        abort(404)

@app.route('/report')
def report():
    #Generate data and report (HTML) template
    full_data = []
    args = request.args
    datasetID =args['id']
    filename = os.path.join(app.config['UPLOADS'],(str(datasetID)+"dataset.txt"))
    dataset = file_lecture(filename)
    for key in app.config['SENSOR_SQUEMA']:
        full_data.append( dataset.info(key) )
    html_page = render_template('graph/report.html',data = full_data,n_ids = len(full_data[0]['IDS']))
    #Generate pdf file from HTML template
    abspath = os.path.realpath(app.config['REPORTS'])
    filename = os.path.join(app.config['REPORTS'],("report.pdf"))
    pdfkit.from_string(html_page, filename)
    #Return file generated
    try:
        return send_from_directory(
            abspath, 'report.pdf', as_attachment=True
        )
    except FileNotFoundError:
        abort(404)

    