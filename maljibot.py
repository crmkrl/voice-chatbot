from tkinter import *
import time
import threading
from voice import *

main= Tk()
main.geometry("450x500")    #wxh

def greet():
    label.config(text= "Greetings!")
    textbox.delete(1.0, END)
    with open('txt/initial.txt','r', encoding='utf8', errors ='ignore') as fin:
        malji_greetings = fin.read().lower()
        textbox.insert(END, gTTS_cmd(malji_greetings, "en"))
        time.sleep(3)

def takeQuery():
    user_response = input()         
    robo_respose=""
    label.config(text= "Processing...")
    if user_response is None:
        robo_respose="Robot: "+gTTS_cmd(random.choice(responses.QUIET_ERROR), "en")
        time.sleep(3)
    else:
        lang = detect(user_response) 
        if lang != "en":
            user_response = translate(user_response, lang, "en")
        user_response=user_response.lower()
        if(user_response!='bye'):
            if(user_response=='thanks' or user_response=='thank you' ):
                flag=False
                robo_respose="Robot: "+gTTS_cmd("You are welcome.", lang)
            else:
                if(greeting(user_response)!=None):
                    robo_respose="Robot: "+gTTS_cmd(greeting(user_response), "en")
                else:
                    robo_respose="Robot: "+response(user_response, lang)
                    sent_tokens.remove(user_response)
        else:
            flag=False  
            robo_respose="Robot: "+gTTS_cmd("Good bye!", lang)
        return robo_respose

def thread_exit():
    main.destroy()

def thread_fun():
    greet()
    while(flag==True):
        textbox.delete(1.0, END)
        label.config(text= "Listening...")
        robot=takeQuery()
        textbox.insert(END, robot)
        label.config(text= "Wait for the robot...")
        time.sleep(7)

label= Label(main)
label.pack(pady=20)

textbox = Text(main, height = 20, width = 50)
textbox.pack()
threading.Thread(target=thread_fun).start()

main.title("nlp-maljibot")

exit_button = Button(main, text="Exit", command=thread_exit)
exit_button.pack(pady=20)

img = PhotoImage(file = 'malji.png') 
main.iconphoto(False, img)

main.mainloop()