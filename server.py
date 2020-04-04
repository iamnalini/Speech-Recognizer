from flask import Flask, render_template, request, redirect
import speech_recognition as sr
from fpdf import FPDF

# creates a Flask application, named app
app = Flask(__name__)

# a route where we will display a welcome message via an HTML template
@app.route("/")
def hello():
    return render_template('speech_to_text.html')

@app.route('/convert', methods = ['POST'])
def convert():
    try:
        file = request.form['file']
        r = sr.Recognizer()
        #use the audio file as a audio source
        harvard = sr.AudioFile(file)  

        with harvard as source:
            #wait for a second to let the recognizer adjust the energy threshold based on surrounding noise level
            r.adjust_for_ambient_noise(source)
            #reads the audio file
            audio = r.record(source)
            try:
                #convert the voice to text
                text = r.recognize_google(audio)
                return render_template('display_text.html',data=text)
            
            except sr.UnknownValueError:
                return "Goole Speech Recognition could not understand audio"
                
            except sr.RequestError as e:
                return ("Could not request result from Google Speech Recognition service: {0}".format(e))

    except:
        return "Check whether the input file is in audio file format"

@app.route('/download', methods = ['POST'])
def download():
    try:
        info = request.form['data']
        filename = request.form['filename']
        pdf = FPDF(orientation='P', unit='mm', format='A4')
            
        #Add page to pdf
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=info, border=0, ln=1, align="C")

        #create pdf 
        pdf.output(filename+'.pdf')
        return render_template('success.html')

    except:
        return "Input file name may be already exists"
    
# run the application
if __name__ == "__main__":
    app.run(debug=True)