import tkinter as tk
import tkinter.font as font
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as m
from datetime import datetime
import os

from teacher import *
from student import *
"""
Room for imporvement:
Allow multiple teachers to correct
Visualize answers for correctino better
    
"""
#johntrial123@outlook.com
#Trythisonce
#freemysql pwd: Trythisonce123!
#https://www.phpmyadmin.co/

"""
Server: sql3.freemysqlhosting.net
DB Name: sql3470461
Username: sql3470461
Password: BREglSJFnR
Port number: 3306

"""
try:
    path1=os.path.join(os.getcwd(),'cache')
    os.mkdir(path1)
except FileExistsError:
    pass
db_host='sql3.freemysqlhosting.net'
db_port=3306
db_pwd='BREglSJFnR'
db_usn='sql3470461'
db_name='sql3470461'
def raise_frame(frame):
    frame.tkraise()


window=tk.Tk()

window.config(bg="#cfdee3")
window.geometry('1024x700')
window.title('TESTCAM')

font1=font.Font(family='Bodoni MT',size=17)
font2=font.Font(family='Bodoni MT',size=12)

fA=tk.Frame(master=window,width=240,height=680,borderwidth=10,bg="#cfdee3")
fB=tk.Frame(master=window,width=740,height=680,borderwidth=10,bg="#d5f3f7")
fA.place(x=5,y=20)
fB.place(x=240,y=20)

    
time=tk.Label(window,text=str(datetime.now().strftime("%H:%M:%S")),font=font2,bg='#cfdee3')
time.place(x=70,y=0)
a=(datetime.now().strftime("%H:%M:%S"))
b=time['text']

def update():
    global time
    #print('dk')
    if str(datetime.now().strftime("%H:%M:%S"))==str(time['text']):
        pass
    else:
        #time['text']=str(datetime.now("%H:%M:%S").strftime())
        time.config(text=(datetime.now().strftime("%H:%M:%S")))
    window.after(1000,update)
update()
def clear_frame(*frame):
    for i in frame:
        for widgets in i.winfo_children():
            widgets.destroy()
def loginpage():
    global fA,fB
    clear_frame(fA,fB)
    
    lb1=tk.Label(fA,text=" LOGIN ",font=font2)
    lb2=tk.Label(fA,text=" REGISTER AS ",font=font2)
    btn1=tk.Button(fA,text='STUDENT',font=font1,command=studentlogin)
    btn2=tk.Button(fA,text='TEACHER',font=font1,command=teacherlogin)
    btn3=tk.Button(fA,text='STUDENT',font=font1,command=studentreg)
    btn4=tk.Button(fA,text='TEACHER',font=font1,command=teacherreg)
    lb1.place(x=30,y=60)
    lb2.place(x=30,y=260)
    btn1.place(x=50,y=100)
    btn2.place(x=50,y=180)
    btn3.place(x=50,y=300)
    btn4.place(x=50,y=380)

def studentlogin():
    global fA,fB
    clear_frame(fB)
    lb_base=tk.Label(fB,text="STUDENT LOGIN",font=font1,bg="#cfdee3")
    lb1=tk.Label(fB,text="USERNAME",font=font2,bg="#d5f3f7")
    lb2=tk.Label(fB,text="PASSWORD",font=font2,bg="#d5f3f7")
    lb3=tk.Label(fB,text="MEETING CODE",font=font2,bg="#d5f3f7")
    ent1=tk.Entry(fB)
    ent2=tk.Entry(fB,show="*")
    ent3=tk.Entry(fB)

    lb_base.place(x=270,y=100)
    lb1.place(x=220,y=250)
    lb2.place(x=220,y=330)
    #lb3.place(x=220,y=410)
    ent1.place(x=330,y=250)
    ent2.place(x=330,y=330)
    #ent3.place(x=330,y=410)

    btn1=tk.Button(fB,text="SUBMIT",font=font2,command=lambda : verify_login(ent1,ent2,'stu'))
    btn2=tk.Button(fB,text="SHOW PASSWORD",font=font2,command=lambda : showpass([ent2],btn2))
    btn1.place(x=300,y=490)
    btn2.place(x=460,y=330)
def studentreg():
    global fA,fB
    clear_frame(fB)
    lb_base=tk.Label(fB,text="STUDENT REGISTER",font=font1,bg="#cfdee3")
    lb1=tk.Label(fB,text="USERNAME",font=font2,bg="#d5f3f7")
    lb2=tk.Label(fB,text="PASSWORD",font=font2,bg="#d5f3f7")
    lb3=tk.Label(fB,text="CONFIRM \nPASSWORD",font=font2,bg="#d5f3f7")
    lb4=tk.Label(fB,text='NAME',font=font2,bg="#d5f3f7")
    
    ent1=ttk.Entry(fB)
    ent2=ttk.Entry(fB,show="*")
    ent3=ttk.Entry(fB,show="*")
    ent4=ttk.Entry(fB)
    
    lb_base.place(x=270,y=100)
    lb1.place(x=220,y=250)
    lb2.place(x=220,y=330)
    lb3.place(x=180,y=410)
    lb4.place(x=220,y=170)
    
    ent1.place(x=330,y=250)
    ent2.place(x=330,y=330)
    ent3.place(x=330,y=410)
    ent4.place(x=330,y=170)
    
    btn1=tk.Button(fB,text="SUBMIT",font=font2,command=lambda : verify_reg(ent1,ent2,ent3,ent4,'stu'))
    btn2=tk.Button(fB,text="SHOW PASSWORD",font=font2,command=lambda : showpass([ent2,ent3],btn2))
    btn1.place(x=300,y=490)
    btn2.place(x=460,y=330)

def teacherlogin():
    global fA,fB
    clear_frame(fB)

    lb_base=tk.Label(fB,text="TEACHER LOGIN",font=font1,bg="#cfdee3")
    lb1=tk.Label(fB,text="USERNAME",font=font2,bg="#d5f3f7")
    lb2=tk.Label(fB,text="PASSWORD",font=font2,bg="#d5f3f7")
    ent1=tk.Entry(fB)
    ent2=tk.Entry(fB,show="*")

    lb_base.place(x=270,y=100)
    lb1.place(x=220,y=250)
    lb2.place(x=220,y=330)
    ent1.place(x=330,y=250)
    ent2.place(x=330,y=330)

    btn1=tk.Button(fB,text="SUBMIT",font=font2,command=lambda : verify_login(ent1,ent2,'tea'))
    btn2=tk.Button(fB,text="SHOW PASSWORD",font=font2,command=lambda : showpass([ent2],btn2))
    btn1.place(x=300,y=490)
    btn2.place(x=460,y=330)
def teacherreg():
    global fA,fB
    clear_frame(fB)
    txt1=tk.StringVar()
    lb_base=tk.Label(fB,text="TEACHER REGISTER",font=font1,bg="#cfdee3")
    lb1=tk.Label(fB,text="USERNAME",font=font2,bg="#d5f3f7")
    lb2=tk.Label(fB,text="PASSWORD",font=font2,bg="#d5f3f7")
    lb3=tk.Label(fB,text="CONFIRM \nPASSWORD",font=font2,bg="#d5f3f7")
    lb4=tk.Label(fB,text='NAME',font=font2,bg="#d5f3f7")
    
    ent1=ttk.Entry(fB)
    ent2=ttk.Entry(fB,show="*")
    ent3=ttk.Entry(fB,show="*")
    ent4=ttk.Entry(fB)

    lb_base.place(x=270,y=100)
    lb1.place(x=220,y=250)
    lb2.place(x=220,y=330)
    lb3.place(x=180,y=410)
    lb4.place(x=220,y=170)
    
    ent1.place(x=330,y=250)
    ent2.place(x=330,y=330)
    ent3.place(x=330,y=410)
    ent4.place(x=330,y=170)
    
    btn1=tk.Button(fB,text="SUBMIT",font=font2,command=lambda : verify_reg(ent1,ent2,ent3,ent4,'tea'))
    btn2=tk.Button(fB,text="SHOW PASSWORD",font=font2,command=lambda : showpass([ent2,ent3],btn2))
    btn1.place(x=300,y=490)
    btn2.place(x=460,y=330)

def verify_reg(*cred):
    l=[]
    if cred[-1]=='stu':
        table='stu'
    elif cred[-1]=='tea':
        table='tea'
    cred=cred[0:-1]
    for i in cred:
        l.append((i.get()).strip())
    res=verify_detail(*l)
    l[3]=l[3].strip()
    for i in l[3]:
        if i.isalpha()==False:
            messagebox.showwarning('Warning','Name should contain only Alphabets')
            return False
    if len(l[3])<4 and len(l[3])>10:
        messagebox.showwarning('Warning','Name should contain Only 4-10 characters')
        return False
    
    if res[0]==False:
        messagebox.showwarning('Warning',res[1])
        return False
    
    #cred[0] =username
    #cred[1]=pwd
    #cred[2]confirm_pwd
    #cred[3] name
    try:
        con=m.connect(host=db_host,port=db_port,user=db_usn,password=db_pwd,database=db_name)
    except (m.errors.InterfaceError,m.errors.DatabaseError):
        messagebox.showerror('No Internet','Please check your connection to the Internet!')
        return False
    cur=con.cursor()
    cur.execute('SELECT * from '+table)
    data=cur.fetchall()
    for i in data:
        if i[0]==l[0]:
            messagebox.askretrycancel('Register','Username already Exists!')
            con.close()
            return False
            
    cur.execute('insert into '+table+'(usn,pwd,nam) values("{}","{}","{}")'.format(l[0],l[1],l[3].title()))
    messagebox.showinfo('Register','Successfully Registered!')
    
    con.commit()
    con.close()
    for i in cred:
        i.delete(0,tk.END)
    if table=='tea':
        teacherhome(window,fA,fB,l[3].title(),font1,font2,l[0],loginpage)
    elif table=='stu':
        studenthome(window,fA,fB,l[3].title(),font1,font2,l[0],loginpage)
            ##++++++++++++++++++++++++++##
def verify_login(*cred):
    #cred[0] =username
    #cred[1]=pwd
    global window,fA,fB
    l=[]
    if cred[-1]=='stu':
        table='stu'
    elif cred[-1]=='tea':
        table='tea'
    cred=cred[0:-1]
    for i in cred:
        l.append((i.get()).strip())
    if l[0]=='' or l[1]=='':
        messagebox.showerror('Login','Please Enter All Fields!')
        return False
    
    try:
        con=m.connect(host=db_host,port=db_port,user=db_usn,password=db_pwd,database=db_name)
    except (m.errors.InterfaceError,m.errors.DatabaseError):
        messagebox.showerror('No Internet','Please check your connection to the Internet!')
        return False
    cur=con.cursor()
    cur.execute('SELECT * from '+table)
    data=cur.fetchall()
    for i in data:
        if i[0]==l[0]:
            if i[1]==l[1]:
                con.close()
                messagebox.showinfo('Login','Successfully Logged In!')
                order()
                if table=='tea':
                    teacherhome(window,fA,fB,i[2],font1,font2,i[0],loginpage)
                elif table=='stu':
                    studenthome(window,fA,fB,i[2],font1,font2,i[0],loginpage)
                ##++++++++++++++++++++++++++##
                return True
            else:
                messagebox.askretrycancel('Login','Password Doesn\'t Match!')
                con.close()
                return False
            
    else:
        messagebox.askretrycancel('Login','Username Doesn\'t Exist!')
        return False
    con.close()
    #"""
def verify_detail(*cred):
    #cred[0] =username
    #cred[1]=pwd
    #cred[2]confirm_pwd
    if cred[0]=='' or cred[1]=='' or cred[2]=='':
        return [False,'All Fields Must be Entered!']
    if not cred[0][0].isalpha() :
        if not cred[0][0]=='_':
            return [False,'Username should begin with an Alphabet or Underscore']
    for i in cred[0]:
        if ((ord(i)>=48 and ord(i)<58)==True) or(i.isalpha())==True or i=='_' :
            pass
        else:
            return [False,'Username should only contain Alphabets or digits or Underscores ']
    if len(cred[0])<4 or len(cred[0])>10:
        return [False,'Username should have 4-10 characters']
    for i in cred[1]:
        if ((ord(i)>=48 and ord(i)<58)==True)or (i.isalpha())==True or (ord(i) in [33,35,36,37,38,46,63,64])==True:
            pass
        else:
            return [False,'Password should only contain Alphabets or digits or {}'.format(list(map(chr,[33,35,36,37,38,46,63,64]))[1:-1])]
    num=0
    spec=0
    caps=0
    for i in cred[1]:
        if i.isupper():
            caps+=1
        if ord(i) in [33,35,36,37,38,46,63,64]:
            spec+=1
        if ord(i)>=48 and ord(i)<58:
            num+=1
    if num==0:
        return [False,'Password should contain atleast 1 digit']
    if caps==0:
        return [False,'Password should contain atleast 1 capital letter']
    if spec==0:
        return [False,'Password should contain atleast 1 special symbol']
    
    if len(cred[1])<4 or len(cred[1])>15:        return[False,'Passwords should have atleast 4-10 characters']
    if cred[1]!=cred[2]:
        return [False,'Passwords Don\'t Match']
    return [True,None]
        
def showpass(a,b):
    #a is list
    #a[0] is ent1
    #a[1] ent2(if exists)
    #b btn Show password
    if a[0].cget('show')=='*':
        for i in a:
            i.config(show='')
        b.config(text='HIDE PASSWORD')
    elif a[0].cget('show')=='':
        for i in a:
            i.config(show='*')
        b.config(text='SHOW PASSWORD')
def order():
    loginpage()
order()
window.mainloop()
