#login page code

#import#######
import mysql.connector
from tkinter import *
from PIL import Image
from tkinter import messagebox
from subprocess import call
import pygame

#commands#######
def loginbutton():
    mydb= mysql.connector.connect(host="localhost",user="root",passwd="dango@12345",database="mythiconlogin")
    cur=mydb.cursor()
    username=e1.get()
    password=e2.get()
    if username=="" or password=="":
        messagebox.showinfo('',"All fields are required")
        return False
    cur.execute("select * from Login where Username= %s and Password = %s",[(username),(password)])
    results = cur.fetchall()
    if results:
        messagebox.showinfo('','Login Successful!')
        uname = username
        f=open('mythicon_others/username.txt','w')
        f.write(uname)
        f.close()
        root.destroy()
        pygame.mixer.music.stop()
        call(['python','startpage.py'])
        return True
    else:
        messagebox.showinfo('',"Invalid Username and Password")
        return False

def registerbutton():
    mydb= mysql.connector.connect(host="localhost",user="root",passwd="dango@12345",database="mythiconlogin")
    cur=mydb.cursor()
    
    username=e1.get()
    password=e2.get()
    if username=="" or password=="":
        messagebox.showinfo('',"All fields are required")
        return False
    cur.execute("select * from Login where Username= %s",[(username)])
    results = cur.fetchall()
    if results:
        messagebox.showinfo('','Username taken')
        return False
    else:
        cur.execute("insert into Login(Username,Password,logindate)values(%s,%s,now())",(username,password))
        mydb.commit()
        messagebox.showinfo('','Registration Successful!')
        return True

#main segment#######
root = Tk()
root.title("Login")#title
#frame
frame= Frame(root)
frame.pack()
#creating canvas
canvas = Canvas(frame, bg="black",width=739,height=415)
canvas.pack()
#sound
pygame.mixer.init()# initialise the pygame
pygame.mixer.music.load("mythicon_sounds/skyrain.wav")
pygame.mixer.music.play(-1)
#images
bg_image = PhotoImage(file = r"mythicon_images/peakpx.png")
username_image=PhotoImage(file = r"mythicon_images/uname.png")
password_image=PhotoImage(file = r"mythicon_images/pasword.png")
login_image=PhotoImage(file = r"mythicon_images/login.png")
register_image=PhotoImage(file = r"mythicon_images/register.png")
loginpg_image=PhotoImage(file = r"mythicon_images/loginpage.png")
#Show bg using canvas
canvas.create_image(369.5,207.5,image=bg_image)
#heading login page
canvas.create_image(380,70,image=loginpg_image)
#show username and password images
canvas.create_image(250,150,image=username_image)
canvas.create_image(250,200,image=password_image)
#message
canvas.create_text(380,250,fill="white",font="courier",text="Please enter your details before logging in or registering.")
#global variables
global e1
global e2
global uname
#username entry
e1= Entry(root,font=("courier",15))
e1.place(x=400,y=135,width=200,height=28)
#password entry
e2 = Entry(root,font=("courier",15))
e2.place(x=400,y=185,width=200,height=28)
e2.config(show="*")
#buttons
Button(root,image=login_image,command=loginbutton,height=40,width=150).place(x=140,y=300)
Button(root,image=register_image,command=registerbutton,height=40,width=220).place(x=375,y=300)

root.mainloop()#end
