import inspect

from flask import Flask, request, send_from_directory
from flask_mail import Mail, Message
import logging, sys, os


app = Flask(__name__)
mail = Mail()
mail.init_app(app)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

UPLOAD_FOLDER = './Files/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/css/<path:path>')
def css(path):
    return send_from_directory('Recursos/css', path)

@app.route('/js/<path:path>')
def jss(path):
    return send_from_directory('Recursos/js', path)

@app.route('/')
def main_page_blank():
    return send_from_directory('Recursos/html', 'index.html')

@app.route('/<path:path>')
def html(path):
    return send_from_directory('Recursos/html', path)

@app.route('/contactar', methods=['POST'])
def send_message():
    try:
        msg = Message(str(request.form['mensaje']) + str(request.form['asunto']),sender=("Usuario FiltradoDatos", str(request.form['email'])),recipients=['jorgenietoaz@gmail.com'])
        mail.send(msg)
        return ('', 204)
    except Exception:
        return ('', 500)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    try:
        if request.method == 'POST':
            args=request.args.to_dict()
            if args['qqfile'] and allowed_file(args['qqfile']):
                script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
                rel_path = "Recursos/Files/"
                abs_file_path = os.path.join(script_dir, rel_path)
                file = open(abs_file_path + args['qqfile'] ,"w")
                file.write(str(request.data))
                app.logger.debug('pasa3')
                file.close()
                app.logger.debug('pasa4')
                return '{"success":true}'
        return '{"error":"Ocurrio algun error."}'
    except Exception as e:
        z=e
        app.logger.debug(z)
        return '{"error":"Ocurrio algun error."}'

@app.route('/see', methods=['GET', 'POST'])
def see_file():
    script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    rel_path = "Recursos/Files/main.py"
    abs_file_path = os.path.join(script_dir, rel_path)
    f = open(abs_file_path,'r')
    return str(f.read())




if __name__ == '__main__':
  app.run()
