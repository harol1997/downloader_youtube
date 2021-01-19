"""
modulo donde se encuentran todas las herramientas necesarias para
descargar un video
"""

from os import remove
from pafy import new
from moviepy.video.io.VideoFileClip import VideoFileClip
from proglog import ProgressBarLogger

class Downloader():
    """[clase encargada de convertir el video de youtube a formato mp3]
    """
    def __init__(self,url,dest):
        """[constructor]

        Args:
            url ([str]): [url de youtube]
        """
        self.url = url
        self.dest = dest

    def send_value(self,value,dest,state,name=""):
        """[esta funcion no hace nada por si sola, se debe sobreescribir]

        Args:
            value ([float]): [porcentaje de la conversion]
            dest ([str]): [id del salon en donde se encuentra el usuario]
            state ([str]): [estado de la conversion . 2 opciones("progress" o "finish")]
            name (str, nombre de la cancion): Defaults to "" si aun sigue en progreso.
        """

    def __process(self,bytes_sec,total_bytes,relacion,tasa,eta):
        """[process when is download the youtube video]

        Args:
            bytes_sec ([int]): [description]
            total_bytes ([int]): [description]
            relacion ([float]): [description]
            tasa ([float]): [description]
            eta ([]): [description]
        """
        percent = (relacion*100)/2
        self.send_value(percent,self.dest,'progress')

    def download(self,directory):
        """[llamara  esta funcion para descargar y convertir el video de youtube a
        formato mp3]

        Args:
            directory ([str]): [ruta en donde se guardaran las canciones para posteriormente
            enviarlas]
        """
        try:
            #download video
            video = new(self.url)
            stream = video.getbest(preftype='mp4')
            name = stream.title.replace('/','')
            extension = stream.extension
            stream.download(filepath=f"{name}.{extension}",quiet=True,callback=self.__process)
            #convert mp4 2 mp3
            with VideoFileClip(f"{name}.{extension}") as video_audio:
                logger = Logger(dest=self.dest)
                logger.send_value = self.send_value
                video_audio.audio.write_audiofile(f"{directory}/{name}.mp3",logger=logger)
            remove(f"{name}.{extension}")
            self.send_value(0,self.dest,'finish',name)#enviamos señal de que finalizo la conversion
        except Exception as error:
            print(str(error))

class Logger(ProgressBarLogger):
    """[clase encargada de contener la herramienta de obtener el porcentaje
    del proceso de la conversion de formato mp4 a formato mp3]

    Args:
        ProgressBarLogger ([clase]): [clase padre]
    """
    def __init__(self,init_state=None,
                bars=None,
                ignored_bars=None,
                logged_bars='all',
                min_time_interval=0,
                ignore_bars_under=0,
                dest=""):

        super().__init__(
            init_state=init_state,
            bars=bars,
            ignored_bars=ignored_bars,
            logged_bars=logged_bars,
            min_time_interval=min_time_interval,
            ignore_bars_under=ignore_bars_under
            )

        self.dest = dest

    def send_value(self,value,dest,state,name=""):
        """[esta funcion no hace nada por si sola, se debe sobreescribir]

        Args:
            value ([float]): [porcentaje de la conversion]
            dest ([str]): [id del salon en donde se encuentra el usuario]
            state ([str]): [estado de la conversion . 2 opciones("progress" o "finish")]
            name (str, nombre de la cancion): Defaults to "" si aun sigue en progreso.
        """
        pass

    def callback(self,**karg):
        """
        este metodo se llamaa dentro del proceso de covnersion
        como parametro logger de auto_writefile.
        Para saber mas ir a la documentacion de moviepy
        """
        if 'chunk' in self.bars:#si es que hay datos leidos
            index = int(self.bars['chunk']['index'])
            total = int(self.bars['chunk']['total'])
            percent = (((index/total)*100)/2)+50
            #print(f"{index} ---> {total} : {percent}%")
            self.send_value(percent,self.dest,'progress')
