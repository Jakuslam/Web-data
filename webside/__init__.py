from urllib import request
from flask import Blueprint, render_template, request, flash
import os

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'weby'

cestaKeSlozece = r"path...." #Change variable cestaKeSložce to your patho to that folther.

e = "newMember@gmail.com"
p = "123"


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route("/", methods=["GET","POST"])
def home():
    form = UploadFileForm()

    if request.method == "POST": #základní otevření stránky
        email = request.form.get("email")
        password = request.form.get("password")
        if(email == e and password == p):
            
            stranky = getFilesNames(cestaKeSlozece) #zjisteni stranek

            return render_template("h_k_data.html", stranky= stranky)

        elif(request.form.get("button")): #při rozkliknutí foldru
            try:
                hodnota = request.form.get("button")
                stranky = getFilesNames(cestaKeSlozece) #zjisteni stranek
                a = cestaKeSlozece + hodnota
                
                soubory = getFilesNames(a) #zjisteni souboru v těch adresářích
                print(soubory)

                return render_template("nt.html", stranky = stranky, soubory = soubory, hodnota = hodnota)

            except:
                print(4)
                return render_template("home.html", text="login")


        elif(request.form.get("deleteFile")): #pro vymazání 
            hodnota = request.form.get("deleteFile")
            a = cestaKeSlozece + hodnota
            deleteFile(a)

            print(hodnota)


            b = hodnota.split("/")
            a = cestaKeSlozece + b[0]

            soubory = getFilesNames(a) #zjisteni souboru v těch adresářích
            stranky = getFilesNames(cestaKeSlozece) #zjisteni stranek
            return render_template("nt.html", stranky = stranky, soubory = soubory, hodnota = hodnota)
        
        elif(request.form.get("Upload")): #při rozkliknutí Upload
            try:
                
                hodnota = request.form.get("Upload")
                print(hodnota)
                a = cestaKeSlozece + hodnota

                stranky = getFilesNames(cestaKeSlozece) #zjisteni stranek
                a = cestaKeSlozece + hodnota
                
                soubory = getFilesNames(a) #zjisteni souboru v těch adresářích


                form = UploadFileForm()


                return render_template("upload.html", form=form, cesta = a)

            except:
                print(4)
                return render_template("home.html", text="login")

        elif(request.form.get("cesta")): #uploadne soubor do místa

            cesta = request.form.get("cesta")

            print(cesta)
            app.config['UPLOAD_FOLDER'] = str(cesta)

            file = form.file.data # First grab the file

            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
            


            stranky = getFilesNames(cestaKeSlozece) #zjisteni stranek

            return render_template("h_k_data.html", stranky= stranky)

        elif(request.form.get("addFolder")): #přepošle nás na add folder

            hodnota = request.form.get("addFolder")

            a = cestaKeSlozece + hodnota
         

            
            return render_template("createFolder.html", cesta = a)

        elif(request.form.get("createFolder")): #vytvoří folder

            hodnota = request.form.get("createFolder")
            hodnota2 = request.form.get("folderName")

            a =  hodnota + hodnota2
         
            createFolder(a)

            stranky = getFilesNames(cestaKeSlozece) #zjisteni stranek

            return render_template("h_k_data.html", stranky= stranky)

        elif(request.form.get("deleteFolder")): #smaže folder

            hodnota = request.form.get("deleteFolder")

            
            
            a = cestaKeSlozece + hodnota
            print(a)

            deleteFolder(a)

            stranky = getFilesNames(cestaKeSlozece) #zjisteni stranek
            return render_template("h_k_data.html", stranky= stranky)

        elif(request.form.get("rename")): #jde na stránku, kde e přejmenuje soubor soubor

            hodnota = request.form.get("rename")
            hodnota2 = hodnota.rsplit("/", 1)

            a = cestaKeSlozece + hodnota
            b = cestaKeSlozece + hodnota2[0]

            print(a)
            print(b)


            return render_template("rename.html", cesta = a, cestaN = b)
        
        elif(request.form.get("newName")): #přejmenuje soubor

            hodnota = request.form.get("newName")
            hodnota2 = request.form.get("pomocna")
            staraCesta = request.form.get("oldFilePath")
            
            

            a = hodnota2 + "/" + hodnota
            print(staraCesta)
            print(a)
            
                

            rename(staraCesta, a)

            stranky = getFilesNames(cestaKeSlozece) #zjisteni stranek
            return render_template("h_k_data.html", stranky= stranky)

        elif(request.form.get("openFolder")): #otevře Folder

            hodnota = request.form.get("openFolder")

            cesta = cestaKeSlozece + hodnota



            print(cesta)
            
            soubory = getFilesNames(cesta) #zjisteni souboru v těch adresářích
  
            return render_template("openFolder.html", stranka = hodnota, soubory = soubory)
        
        elif(request.form.get("back")): #vrácení se zpět na začátek
            stranky = getFilesNames(cestaKeSlozece) #zjisteni stranek

            return render_template("h_k_data.html", stranky= stranky)
        

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


if(__name__ == "__main__"):
    app.run(debug=True)