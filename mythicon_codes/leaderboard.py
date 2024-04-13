#leaderboard
#import####
from tkinter import *
from tkinter import messagebox
from subprocess import call
import mysql.connector
import pygame

#commands###
def back():
    root.destroy()
    return True

#intializing tk###
root = Tk()
root.title("Leader Board")
#frame
frame= Frame(root)
frame.pack()
#canvas
canvas = Canvas(frame, bg="black",width=739,height=415)
canvas.pack()
#images
bg_surface= PhotoImage(file =(r'mythicon_images/lbinbg.png'))
lb_surface= PhotoImage(file =(r'mythicon_images/board2.png'))
back_surface=PhotoImage(file=(r"mythicon_images/back.png"))
canvas.create_image(369.5,207.5,image=bg_surface)
canvas.create_image(450.5,240,image=lb_surface)

#getting highscore and player id from mysql
mydb= mysql.connector.connect(host="localhost",user="root",passwd="dango@12345",database="mythiconlogin")
cur=mydb.cursor()
cur.execute('select highscore,playerid from login')
results=cur.fetchall()
results=list(results)
#sorting results in descending
sorted_result=(sorted(results, key = lambda x: x[0], reverse=True))

#getting the user info using mysql and results
userlist=[]
for user in sorted_result:
    cur.execute('select * from login where playerid =%s',[(user[1])])
    userdet=cur.fetchall()
    userlist.append(userdet)
    
#displaying the details
x=150
y=210
for i in range(5):
    canvas.create_text(x,y,fill="black",font=("courier",20),text=str(userlist[i][0][4]),anchor = W)
    canvas.create_text(x+130,y,fill="black",font=("courier",20),text=(str(userlist[i][0][0])).upper(),anchor = W)
    canvas.create_text(x+330,y,fill="black",font=("courier",20),text=str(userlist[i][0][2]),anchor = W)
    y+=42
    
#printing the user's personal highscore
f=open(r'mythicon_others/username.txt','r')
username=f.read().strip()
f.close()
cur.execute('select * from login where username =%s',[(username)])
user_details=cur.fetchall()
user_highscore=user_details[0][2]
canvas.create_text(140,40,fill='white',font=('courier',20),text='Username:'+str(username)+' Highscore:'+str(user_highscore),anchor = W)

#button
Button(root,image=back_surface,command=back,height=40,width=50).place(x=684,y=370)

root.mainloop()#end
















