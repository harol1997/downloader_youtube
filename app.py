"""
Script principal donde se utilizan todos los metodos neesarios acompañado de los 
decoradores correspondientes para la aplicacion
"""
from os import system,mkdir,path
from threading import Thread
from flask import Flask,render_template,request,copy_current_request_context,send_from_directory
from werkzeug.exceptions import NotFound
from flask_socketio import SocketIO,join_room,leave_room,close_room,rooms
from eventlet import monkey_patch,sleep
from download import Downloader

DIRECTORY_MUSIC = "static/music"

if not path.exists(DIRECTORY_MUSIC):
    mkdir(DIRECTORY_MUSIC)

monkey_patch()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,logger=True, engineio_logger=True)

@app.route('/')
def index():
    """[pagina principal]

    Returns:
        [html]: [html de la pagina principal]
    """
    return render_template('index.html')

@app.route('/downloadh/<id_video>')
def downloadh(id_video):
    """[pagina donde se muestra el proceso de conversion de un video de youtube
    a mp3]

    Args:
        id_video ([str]): [codigo del video que pertenece al link de youtube]

    Returns:
        [html]: [pagina de la barra del progreso]
    """
    return render_template('download.html')

@socketio.on('connect')
def connect():
    """[cuando un usuario se conecta se une a un salon
    Esto servira para cuando deseo informarle al usuario como va el proceso
    de conversion.
    El id del salon esta dado por el id de request]
    """
    join_room(request.sid)

@socketio.on('disconnect')
def disconnect():
    """[Cuando el usuario sufre una desconexion de cualquier tipo
    abandona el salon y eliminamos completamente el salon]
    """
    leave_room(request.sid)
    close_room(request.sid)

@socketio.on('url')
def convert2mp3(data):
    """[funcion que ejecuta el proceso de conversion]

    Args:
        data ([str]): [el url del video de youtube a convertir]
    """
    url = data['url'].strip()
    id_youtube = url.split('/')[-1]
    url_youtube = f"https://www.youtube.com/watch?v={id_youtube}"
    downloader = Downloader(url_youtube,request.sid)
    downloader.send_value = value2progressbar
    @copy_current_request_context
    def download_thread():
        """[se ejecuta en un hilo secundario]
        """
        downloader.download(DIRECTORY_MUSIC)
    Thread(target=download_thread).start()

def value2progressbar(value,dest,state,name=""):
    """[funcion que ayudara al descargador enviar el porcentaje del progreso al cliente]
    Args:
        value ([float]): [porcentaje del progreso de la conversion]
        dest ([str]): [id del salon a donde enviar el progreso]
        state ([str]): [estado de la conversion . 2 opciones("progress" o "finish")]
        name (str, nombre de la cancion): [description]. Defaults to "" si aun sigue en progreso.
    """
    if dest in rooms():
        socketio.emit('progressbar',
        {
            'state': state,
            'value':str(int(value)),
            'name':name
        },
        room=dest)
        sleep()
    else:
        raise Exception("desconexion")

@app.route('/download/<filename>')
def download(filename):
    """[funcion que envia el archivo mp3 al cliente]

    Args:
        filename ([type]): [description]

    Returns:
        [file]: [la cancion mp3]
    """
    print(filename)
    try:
        return send_from_directory(DIRECTORY_MUSIC,filename+'.mp3',as_attachment=True)
    except NotFound as error:
        return str(error)

if __name__ == "__main__":
    socketio.run(app,port=5000)
