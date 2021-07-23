from tkinter import *
import speech_recognition as s
import threading
import malji as chat_mj

main = Tk()
main.geometry("500x650")
main.title("Malji")
img = PhotoImage(file="bot.png")
photoL = Label(main, image=img)
photoL.pack(pady=5)

def takeQuery():
    print("Malji is listening try to speak.")
    with s.Microphone() as m:
        try:
            # user_response = chat_mj.input()
            user_response = chat_mj.speech_cmd()  #for voice command

            query = user_response
            if user_response is None:
                chat_mj.gTTS_cmd(chat_mj.random.choice(chat_mj.responses.QUIET_ERROR), "en")
                chat_mj.time.sleep(3)
            else:
                lang = chat_mj.detect(user_response)    
                if lang != "en":
                    user_response = chat_mj.translate(user_response, lang, "en")
                user_response=user_response.lower()
                if(user_response!='bye'):
                    if(user_response=='thanks' or user_response=='thank you' ):
                        flag=False
                        chat_mj.gTTS_cmd("You are welcome.", lang)
                        answer_from_bot = "You are welcome."
                    else:
                        if(chat_mj.greeting(user_response)!=None):
                            chat_mj.gTTS_cmd(chat_mj.greeting(user_response), "en")
                            answer_from_bot = chat_mj.greeting(user_response)

                        else:
                            chat_mj.response(user_response, lang)
                            chat_mj.sent_tokens.remove(user_response)
                            answer_from_bot = chat_mj.response(user_response, lang)
                else:
                    flag=False  
                    chat_mj.gTTS_cmd("Good bye!", lang)

            print(query)
            textF.delete(0, END)
            textF.insert(0, query)
            ask_from_bot(query)
        except Exception as e:
            print(e)
            print("Error: Not recognized.")

def ask_from_bot(query, answer_from_bot):
    msgs.insert(END, "You : " + query)
    print(type(answer_from_bot))
    msgs.insert(END, "Malji : " + str(answer_from_bot))
    textF.delete(0, END)
    msgs.yview(END)

frame = Frame(main)
sc = Scrollbar(frame)
msgs = Listbox(frame, width=80, height=20, yscrollcommand=sc.set)
sc.pack(side=RIGHT, fill=Y)
msgs.pack(side=LEFT, fill=BOTH, pady=10)
frame.pack()

# creating text field
textF = Entry(main, font=("Courier", 10))
textF.pack(fill=X, pady=10)
btn = Button(main, text="Ask Malji", font=(
    "Courier", 10),bg='blue', command=ask_from_bot)
btn.pack()

# creating a function
def enter_function(event):
    btn.invoke()

# going to bind main window with enter key...
main.bind('<Return>', enter_function)

def repeatL():
    while True:
        takeQuery()

t = threading.Thread(target=repeatL)
t.start()
main.mainloop()
