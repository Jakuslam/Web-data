from urllib import request
from flask import Blueprint, render_template, request, flash
import os
from urllib.request import urlopen

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired



app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

views = Blueprint("views", __name__)

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@views.route("/", methods=["GET","POST"])
def home():
    form = UploadFileForm()

    if request.method == "POST": #základní otevření stránky
        email = request.form.get("email")
        password = request.form.get("password")
        if(email == "krubas59@gmail.com" and password == "a"):
            
            stranky = getFilesNames(r"C:\Users\Jakub Sláma\Desktop\Stranka\weby") #zjisteni stranek

            return render_template("h_k_data.html", stranky= stranky)

        elif(request.form.get("button")): #při rozkliknutí foldru
            try:
                hodnota = request.form.get("button")
                stranky = getFilesNames(r"C:\Users\Jakub Sláma\Desktop\Stranka\weby") #zjisteni stranek
                a = r"C:\Users\Jakub Sláma\Desktop\Stranka\weby/" + hodnota

                soubory = getFilesNames(a) #zjisteni souboru v těch adresářích
                print(hodnota)

                return render_template("nt.html", stranky = stranky, soubory = soubory, hodnota = hodnota)

            except:
                print(4)
                return render_template("home.html", text="login")


        elif(request.form.get("deleteFile")): #pro vymazání 
            hodnota = request.form.get("deleteFile")
            a = r"C:\Users\Jakub Sláma\Desktop\Stranka\weby/" + hodnota
            deleteFile(a)

            print(hodnota)


            b = hodnota.split("/")
            a = r"C:\Users\Jakub Sláma\Desktop\Stranka\weby/" + b[0]

            soubory = getFilesNames(a) #zjisteni souboru v těch adresářích
            stranky = getFilesNames(r"C:\Users\Jakub Sláma\Desktop\Stranka\weby") #zjisteni stranek
            return render_template("nt.html", stranky = stranky, soubory = soubory, hodnota = hodnota)
        
        elif(request.form.get("Upload")): #při rozkliknutí Upload
            try:
                hodnota = request.form.get("Upload")
                print(hodnota)
                a = r"C:\Users\Jakub Sláma\Desktop\Stranka\weby/" + hodnota


                stranky = getFilesNames(r"C:\Users\Jakub Sláma\Desktop\Stranka\weby") #zjisteni stranek
                a = r"C:\Users\Jakub Sláma\Desktop\Stranka\weby/" + hodnota
                soubory = getFilesNames(a) #zjisteni souboru v těch adresářích

                form = UploadFileForm()


                return render_template("nt.html", stranky = stranky, soubory = soubory, hodnota = hodnota, form=form, p = "true")

            except:
                print(4)
                return render_template("home.html", text="login")

        elif(request.form.get("addFolder")): #při přidání foldru
            print("Kliknuto")
            
            return render_template("home.html", text="login")

        if form.validate_on_submit():

            file = FileField("File", validators=[InputRequired()])
            file = form.file.data # First grab the files
            print(file)
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
            return "File has been uploaded."


    return render_template("home.html", text="login")



# odsud to je pouze zkopírovaná třida doc
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)

        return 1 
    except OSError:
        return 0



def saveFile(cesta, obsah): #vytvoří nový soubor, nebo uloží změny
    f = open(cesta, "w")
    f.write(obsah)
    f.close()



def readFile(cesta): #přečte soubor
    f = open(cesta, "r")
    return f.read()



def getFilesNames(cesta):
    os.chdir(cesta) #bude se měnit
    return(os.listdir())


def deleteFile(cesta):
    if os.path.exists(cesta):
        os.remove(cesta)
        return 1 
    else:
        return 0



def deleteFolder(cesta):
    if os.path.exists(cesta):
        os.rmdir(cesta)
        return 1 
    else:
        return 0



def rename(cesta, novaCesta):
    os.rename(cesta,novaCesta)