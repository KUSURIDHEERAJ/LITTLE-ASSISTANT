import wolframalpha                     # Part 1 - The import
import wikipedia
import PySimpleGUI as sg
import speech_recognition as sr
import pyttsx3

app_id = '42AEQP-P5XR3LQKJU'  # get your own at https://products.wolframalpha.com/api/
client = wolframalpha.Client(app_id)

sg.theme('DarkGrey 8')  #touch of colour u can change themes :)# Define the window's contents
# obtain audio from the microphone
while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
       print("Please wait. Calibrating microphone...")
       # listen for 5 seconds and create the ambient noise energy level
       r.adjust_for_ambient_noise(source, duration=1)
       print("Ask Queries!")
       audio = r.listen(source)

    # recognize speech
    try:
        text = r.recognize_google(audio, language = 'en-IN', show_all = True )
        layout = [  [sg.Text("Requested Query")],
                    [sg.Input(r.recognize_google(audio))],
                    [sg.Button('Search'), sg.Button('New Query')]]   # Part 2 - The Layout
        window = sg.Window('Little Assistant', layout)      # Create the window # Part 3 - Window Defintion
        print("I think you said '" + r.recognize_google(audio) + "'")
        while True:                 # Display and interact with the Window # Part 4 - Event loop or Window.read call
            event, values = window.read()
            if event in (None,'New Query'):
                break
            try:
                res = client.query(values[0])
                wolfram_res=next(res.results).text  # Do something with the information gathered
            except Exception as a:
                wolfram_res=" Input not related to Science, Maths and History :)"
            try:
                wiki_res=wikipedia.summary(values[0],sentences=2)
            except Exception as e:
                wiki_res=" Ambiguous input detected to get data from Wikipedia"


            engine = pyttsx3.init()
            voices = engine.getProperty('voices')       #getting details of current voice
            engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
            engine.say(wolfram_res)
            engine.say(wiki_res)
            sg.PopupNonBlocking("Wolfram Result: "+wolfram_res,"Wikipedia Result: "+wiki_res)
            engine.runAndWait()
            print(values[0])
            window.close()

    except sr.RequestError as e:
       print("error; {0}".format(e))

    except Exception as e:
       print (e)

window.close()     # Finish up by removing from the screen     # Part 5 - Close the Window
