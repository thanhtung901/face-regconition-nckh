from tkinter import filedialog

import tkinter as tk
from tkinter import *
from tkinter import Message ,Text
from face_predict import Predict
from PIL import ImageFont, ImageTk, Image
from add_face import *
fontsize = 20
font = ImageFont.truetype("arial.ttf", fontsize)


window = tk.Tk()
#helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("UiTM Attendance system")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
#answer = messagebox.askquestion(dialog_title, dialog_text)

window.geometry('1280x720')
window.configure(background="#515151")



#window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
button_width=300
button_height=45
def Resize_Image(image, maxsize):
    r1 = image.size[0]/maxsize[0] # width ratio
    r2 = image.size[1]/maxsize[1] # height ratio
    ratio = max(r1, r2)
    newsize = (int(image.size[0]/ratio), int(image.size[1]/ratio))
    image = image.resize(newsize, Image.ANTIALIAS)
    return image

student_id =Image.open("icons/student_id.png")
student_id = Resize_Image(student_id,[button_width,100])
student_id =ImageTk.PhotoImage(student_id)

student_name =Image.open("icons/student_name.png")
student_name = Resize_Image(student_name,[button_width,100])
student_name =ImageTk.PhotoImage(student_name)

msg =Image.open("icons/msg.png")
msg = Resize_Image(msg,[button_width,100])
msg =ImageTk.PhotoImage(msg)

xlabels=300

title =Image.open("icons/title.png")
 #title = Resize_Image(title,[button_width,100])
title =ImageTk.PhotoImage(title)

logo1 =Image.open("icons/um6p_emines_logo.png")
logo1 = Resize_Image(logo1,[button_width,50])
logo1 =ImageTk.PhotoImage(logo1)



title_img = tk.Label(window, border=0,image = title  ,bg="#515151"  , activebackground = "#515151")
title_img.place(x=-160, y=40)

#logos
logo1_img = tk.Label(window, border=0,image = logo1  ,bg="#515151"  , activebackground = "#515151")
logo1_img.place(x=65, y=10)


####
lbl = tk.Label(window,border=0 ,image = student_id  ,bg="#515151"  , activebackground = "#515151" )
lbl.place(x=xlabels, y=200)

txt = tk.Entry(window,width=15 ,bg="#F1F0F0" ,fg="#5B5B5B",font=('Cambria', 20, ' bold '),justify = CENTER)
txt.place(x=700, y=205)

lbl2 = tk.Label(window, border=0 ,image = student_name  ,bg="#515151"  , activebackground = "#515151" )
lbl2.place(x=xlabels, y=300)

txt2 = tk.Entry(window,width=15  ,bg="#F1F0F0"  ,fg="#5B5B5B",font=('Cambria', 20, ' bold ') ,justify = CENTER )
txt2.place(x=700, y=305)

lbl3 = tk.Label(window, border=0 ,image = msg  ,bg="#515151"  , activebackground = "#515151")
lbl3.place(x=400, y=400)

#notif

message = tk.Label(window, text="" ,bg="#F1F0F0"  ,fg="#BC2226"  ,width=30  ,height=2, activebackground = "#515151" ,font=('times', 15, ' bold '))
message.place(x=750, y=400)

def addFace():
    Id=(txt.get())
    name=(txt2.get())
    names = Id+name
    create_filename(names)
    add_face(names)
    message.configure(text= "add face successfully!")

def predicts():
    Predict()

img_Predict =Image.open("icons/icon_predict.png")
img_Predict = Resize_Image(img_Predict,[button_width,button_height])
img_Predict =ImageTk.PhotoImage(img_Predict)
center_x=(window.winfo_screenwidth()-button_width)/2
bt_predict = tk.Button(window ,command = predicts ,border=0 ,image =img_Predict  ,bg="#515151"  , activebackground = "#515151" )
bt_predict.place(x=center_x-400, y=500)

img_addface =Image.open("icons/icon_addface.png")
img_addface = Resize_Image(img_addface,[button_width,button_height])
img_addface =ImageTk.PhotoImage(img_addface)

bt_addface = tk.Button(window, command=addFace ,border=0,image= img_addface ,bg="#515151"  , activebackground = "#515151" )
bt_addface.place(x=center_x, y=500)
window.mainloop()