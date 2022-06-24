import tkinter as tk
import tkinter.font as font
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as m
from datetime import datetime
from sample_frames import ScrollableFrame
db_host='sql3.freemysqlhosting.net'
db_port=3306
db_pwd='BREglSJFnR'
db_usn='sql3470461'
db_name='sql3470461'
def convert(s):
    hr=s//3600
    mi=(s-(hr*3600))//60
    se=s-((mi*60)+(hr*3600))
    return(str(hr),str(mi),str(se))
def clear_frame(*frame):
    for i in frame:
        for widgets in i.winfo_children():
            widgets.destroy()
def studenthome(*par):
    global font1,font2,window,fA,fB,usn,usn_name,loginpage
    window=par[0]#par[0] window
    fA=par[1]#par[1] fA
    fB=par[2]#par[2] fB
    usn_name=par[3]#---->par[3] name
    #par[6] usn
    font1=par[4]
    font2=par[5]
    usn=par[6]
    clear_frame(fA,fB)
    lb1=tk.Label(fA,text=(" Hello "+usn_name.title()),font=font1)
    lb1.place(x=10,y=10)
    btn1=tk.Button(fA,text="JOIN EXAM",font=font2,command=basetest)
    btn2=tk.Button(fA,text="SEE PERFORMANCES",font=font2,command=prevtest)
    try:
        if loginpage:
            pass
    except NameError:
        loginpage=par[-1]
    finally:
        btn3=tk.Button(fA,text="LOGOUT",font=font2,command=loginpage)
    btn1.place(x=5,y=170)
    btn2.place(x=5,y=250)
    btn3.place(x=5,y=630)
def basetest(*l):
    global font1,font2,window,fA,fB,usn,usn_name,loginpage
    clear_frame(fB)
    def starttest(code):
        for i in code:
            if (ord(i)<48 or ord(i)>57) and (i.upper())==False:
                messagebox.showerror('Error','Meetcode should contain only Capital Alphabets and Digits')
                return False
        try:
            con=m.connect(host=db_host,port=db_port,user=db_usn,password=db_pwd,database=db_name)       
            cur=con.cursor()
            cur.execute('SELECT code,start,end from pending_exams where code="{}"'.format(code))
            data=cur.fetchall()
            con.close()
            if len(data)==0:
                messagebox.showerror('Error','Meetcode Dosen\'t Exists')
                return False
            if len(data[0])>0:
                if data[0][0]==code:
                    data=data[0]
                    start_datetime=data[1]
                    end_datetime=data[2]
                    if datetime.now()>=start_datetime and datetime.now()<end_datetime:
                        con1=m.connect(host=db_host,port=db_port,user=db_usn,password=db_pwd,database=db_name)       
                        cur1=con1.cursor()
                        cur1.execute('SELECT code,usn_stu from com_exam where code="{}" and usn_stu="{}"'.format(code,usn))
                        try:
                            data1=cur1.fetchall()[0]
                            if code==data1[0] and usn==data1[1]:
                                messagebox.showerror('Error','You have already submitted your response!')
                                return False
                        except IndexError as e:
                            pass
                        con1.close()
                        clear_frame(fB)
                        runtest(code,end_datetime)
                        return False
                    elif datetime.now()<start_datetime:
                        hr,mi,se=convert(start_datetime-datetime.now())
                        messagebox.showinfo('Exam Time','Exam will begin in another : {}:{}:{}'.format(hr,mi,se))
                        return False
                    elif datetime.now()>end_datetime:
                        messagebox.showerror('Exam Time Passed!','Exam was completed already!')
                        return False        
                else:
                    messagebox.showerror('Error','Database Error!')
                    return False
            else:
                messagebox.showerror('Error','Meetcode Dosen\'t Exists')
                return False
            
        except(m.errors.InterfaceError,m.errors.DatabaseError):
            message.showerror('Error','Please Connect to the Internet')
            return False
    def runtest(code,end_datetime):
        
        try:
            con=m.connect(host=db_host,port=db_port,user=db_usn,password=db_pwd,database=db_name)       
            cur=con.cursor()
            cur.execute('SELECT * from pending_exams where code="{}"'.format(code))
            data=cur.fetchall()[0]
            con.close()
        except (m.errors.InterfaceError,m.errors.DatabaseError):
            message.showerror('Error','Please Connect to the Internet')
            return False
        
        clear_frame(fA,fB)
        s1=(end_datetime-datetime.now())
        hr,mi,se=convert(s1)
        timer1=tk.Label(fB,text=("Time Remaining {}:{}:{}".format(hr.zfill(2),mi.zfill(2),se.zfill(2))),font=font2)
        timer1.place(x=450,y=120)
        def update_t():
            s1=(end_datetime-datetime.now())
            try:
                if s1.seconds==0:
                    try:
                        with open('cache\\exam_now.txt','r') as f:
                            txt=f.read().split('\t')
                            if txt[0]==code and txt[1]==usn:
                                push_db()
                    except FileNotFoundError:
                        messagebox.showerror('Error','No Question are Attempted.\nTime Up!')
                        loginpage()
                        return False
                    messagebox.showinfo('Time Up','Answers that are saved are sent!')
                    loginpage()
                    return False
                hr,mi,se=convert(s1.seconds)
                if ("Time Remaining {}:{}:{}".format(hr.zfill(2),mi.zfill(2),se.zfill(2)))==str(timer1['text']):
                    pass
                else:
                    timer1.config(text="Time Remaining {}:{}:{}".format(hr.zfill(2),mi.zfill(2),se.zfill(2)))
                fB.after(1000,update_t)
            except tk.TclError:
                pass
        update_t()
        fC=tk.Frame(master=fB,width=720,height=100,borderwidth=10,bg="#cfdee3")
        fC.place(x=0,y=0)
        fD=tk.Frame(master=fB,height=650,width=720,bg="#d5f3f7")
        fD.place(x=0,y=200)
        btn_exit=tk.Button(fA,text='EXIT EXAM',font=font1,command=loginpage)
        btn_exit.place(x=5,y=100)
        start_datetime=data[1]
        end_datetime=data[2]
        dur=data[4]
        question_l=eval(data[5])
        total_marks=0
        for i in eval(data[5]):
            total_marks+=int(i[1])
        with open('cache\\pending_exam_stu.txt','w') as f:
            f.write(str(data)+'\n')
            f.close()
        
        def ques_change(event):
            
            def save_local(*l):
                try:
                    with open('cache\\exam_now.txt','r') as f:
                        #l[0]=curr_q index#l[1]=ans
                        if l[1]=='':
                            messagebox.showerror('Answer Error','Please Fill in the Entry box')
                            return False
                        txt_showd['state']='normal'
                        str3=[]
                        str3=(txt_showd.get("1.0","end")).split('\n')[:-1]
                        txt_showd.delete("1.0", "end")
                        str3[curr_q]='Question {} : Completed'.format(curr_q+1)
                        txt_showd.insert(tk.END,"\n".join(str3))
                        txt_showd['state']='disabled'
                        f.seek(0)
                        x=False
                        x_=False
                        txt=f.read().split('\t')
                        gcode=txt[0]
                        gusn=txt[1]
                        local=eval(txt[2])
                        if code==gcode and usn==gusn:
                            x=True
                            for i in range(len(local)):
                                if int(local[i][0])==int(l[0]):
                                    local[i][1]=l[1]
                                    x_=True
                                    break
                            if x_==False:
                                local.append([l[0],l[1]])
                        f.close()
                    with open('cache\\exam_now.txt','w') as f:
                        f.write('{}\t{}\t{}\n'.format(gcode,usn,str(local)))
                        f.close()
                    if x==False:
                        with open('cache\\exam_now.txt','w') as f:
                            sam='{}\t{}\t{}'.format(code,usn,str([[l[0],l[1]]]))
                            f.write(str(sam)+'\n')
                            f.close()
                except (FileNotFoundError,EOFError):
                    with open('cache\\exam_now.txt','w') as f:
                        sam='{}\t{}\t{}'.format(code,usn,str([[l[0],l[1]]]))
                        f.write(str(sam)+'\n')
                        f.close()                 
            def push_db():
                global usn
                try:
                     with open('cache\\exam_now.txt','r') as f:
                         txt=f.read().split('\t')
                         gcode=txt[0]
                         gusn=txt[1]
                         if code==gcode and usn==gusn:
                             local=eval(txt[2])
                         else:
                            messagebox.showerror('Error','Please Attempt atleast One Question')
                            return False
                except FileNotFoundError:
                    messagebox.showerror('Error','Please Attempt atleast One Question')
                    return False
                
                try:
                    con=m.connect(host=db_host,port=db_port,user=db_usn,password=db_pwd,database=db_name)       
                    cur=con.cursor()
                    cur.execute('SELECT * from pending_exams where code="{}"'.format(code))
                    data=cur.fetchall()[0]
                    tea_usn=data[1]
                    cur.execute('insert into com_exam(code,usn_tea,usn_stu,answer) values("{}","{}","{}","{}")'.format(code,tea_usn,usn,local))
                    con.commit()
                    con.close()
                    messagebox.showinfo('Exam Completed','You have succesfully completed the exam!')
                    clear_frame(fB)
                    basetest()
                    return False
                except (m.errors.InterfaceError,m.errors.DatabaseError):
                    messagebox.showerror('Error','Please Connect to the Internet')
                    return False
            clear_frame(fD)
            lb_ques=tk.Label(fD,text='',font=font2)
            lb_ques.place(x=0,y=0)
            btn_savea=tk.Button(fD,text='SAVE ANSWER',font=font1)
            btn_quitsave=tk.Button(fD,text='QUIT AND SAVE EXAM',font=font1,command=push_db)
            curr_q=int(current_ques.get().split()[-1])-1
            lb_ques.config(text=question_l[curr_q][2]+' ('+str(question_l[curr_q][1]+' Marks)'))
            if question_l[curr_q][0]=='ent':
                ent_ans=tk.Text(fD,width=50,height=3)
                scroll1 = tk.Scrollbar(fD)
                ent_ans.configure(yscrollcommand=scroll1.set)
                ent_ans.place(x=0,y=100)
                scroll1.config(command=ent_ans.yview)
                scroll1.place(x=405,y=100)
                btn_savea.config(command=lambda:save_local(curr_q,ent_ans.get(1.0,"end-1c").strip()))
            elif question_l[curr_q][0]=='mcq':
                fD_options=tk.Frame(fD,height=150,width=720,bg="#d5f3f7")
                fD_options_c=ScrollableFrame(fD_options,height=1100,width=720)
                fD_options_sub=fD_options_c.frame
                fD_options.place(x=0,y=100)
                rb_options={}
                choice=tk.StringVar()
                for i in range(len(question_l[curr_q][3])):
                    rb_options['rb'+str(i+1)]=tk.Radiobutton(fD_options_sub, text=question_l[curr_q][3][i], variable=choice, value=str(i),font=font2)
                    rb_options['rb'+str(i+1)].pack(side=tk.TOP)
                    rb_options['rb'+str(i+1)].deselect()
                rb_options['rb1'].invoke()
                btn_savea.config(command=lambda:save_local(curr_q,int(choice.get())))
            btn_savea.place(x=0,y=400)
            btn_quitsave.place(x=300,y=400)
            try:
                with open('cache\\exam_now.txt','r') as f:
                    f.seek(0)
                    base=f.read()
                    txt=base.split('\t')
                    gcode=txt[0]
                    gusn=txt[1]
                    local=eval(txt[2])
                    if code==gcode and gusn==usn:
                        for i in range(len(local)):
                            if int(local[i][0])==int(curr_q):
                                if question_l[curr_q][0]=='ent':
                                    ent_ans.delete("1.0", "end")
                                    ent_ans.insert(tk.END,local[i][1])    
                                elif question_l[curr_q][0]=='mcq':
                                    rb_options['rb'+str(int(local[i][1])+1)].select()
                                break
                    f.close()
            except FileNotFoundError:
                pass
        lb_num=tk.Label(fC,text="Questions : {}".format(str(len(question_l))),font=font2)
        lb_marks=tk.Label(fC,text="Total Marks : {}".format(str(total_marks)),font=font2)
        lb_code=tk.Label(fC,text="CODE : {}".format(code),font=font2)
        lb_questions=tk.Label(fB,text="CHOOSE QUESTION",font=font2)

        txt_showd=tk.Text(fC,width=30,height=3,bg='#cfdee3')
        try:
            txt_showd['state']='normal'
            with open('cache\\exam_now.txt','r') as f:
                f.seek(0)
                txt=f.read().split('\t')
                gcode=txt[0]
                gusn=txt[1]
                local=eval(txt[2])
                if code==gcode and gusn==usn:
                    str2=[]
                    for i in range(len(question_l)):
                        str2.append('Question {} : Not Attempted'.format(i+1))
                    for i in range(len(local)):
                        q2=local[i][0]
                        str2[q2]='Question {} : Completed'.format(q2+1)
                    txt_showd.insert(tk.END,'\n'.join(str2))
                else:
                    str2=''
                    for i in range(len(question_l)):
                        str2+='Question {} : Not Attempted\n'.format(i+1)
                    txt_showd.insert(tk.END,str2)      
        except FileNotFoundError:
            str2=''
            for i in range(len(question_l)):
                str2+='Question {} : Not Attempted\n'.format(i+1)
            txt_showd.insert(tk.END,str2)
        txt_showd.config(state='disabled')
        scroll_txt = tk.Scrollbar(fC)
        txt_showd.configure(yscrollcommand=scroll_txt.set)
        txt_showd.place(x=0,y=0)
        scroll_txt.config(command=txt_showd.yview)
        scroll_txt.place(x=250,y=0)
        lb_code.place(x=400,y=5)
        lb_num.place(x=400,y=35)
        lb_marks.place(x=400,y=65)
        lb_questions.place(x=5,y=100)
        current_ques=tk.StringVar()
        choose_ques=ttk.Combobox(fB, width = 15, textvariable = current_ques,values=['Question '+str(i+1) for i in range(len(question_l))])
        choose_ques.bind('<<ComboboxSelected>>', ques_change)
        choose_ques.place(x=200,y=100)
    lb2=tk.Label(fB,text="MEET CODE",font=font1)
    ent_meetcode=tk.Entry(fB)
    btn1=tk.Button(fB,text='JOIN EXAM',command=lambda:starttest(ent_meetcode.get().strip()))
    lb2.place(x=100,y=100)
    ent_meetcode.place(x=400,y=100)
    btn1.place(x=250,y=300)
def prevtest(*l):
    try:
        con=m.connect(host=db_host,port=db_port,user=db_usn,password=db_pwd,database=db_name)       
        cur=con.cursor()
        cur.execute('SELECT code,checked from com_exam where usn_stu="{}" and checked is not NULL'.format(usn))
        com_exams=cur.fetchall()
        con.close()
        exams_l=[]
        ans={}
        if len(com_exams)==0:
            messagebox.showerror('Error','You haven\'t attempted any Exams!')
            return False
        else:
            for i in com_exams:
                clear_frame(fB)
                ans[i[0]]=eval(i[1])
                exams_l.append(i[0])
        con.close()
    except (m.errors.InterfaceError,m.errors.DatabaseError) :
        mesagebox.showerror('Error','Please Connect to the Internet!')
        return False
    def exam_change():
        def q_change(event):
            curr_q=int(qs.get().split()[-1])-1
            if len(q_exams)!=0:
                lb_question.config(text=str(q_exams[curr_q][2]))
                h=ans[qps.get()]
                for i in h:
                    if i[0]==curr_q:
                        final_ans=i[1]
                        break
                if q_exams[curr_q][0]=='ent':
                    lb_answer.config(text='Your Answer : {} \n Marks Awarded : {} out of {}'.format(str(ans_d[curr_q]),str(final_ans),q_exams[curr_q][1]))
                elif q_exams[curr_q][0]=='mcq':
                    lb_answer.config(text='Your Answer : {} \n Marks Awarded : {} out of {}'.format(str(q_exams[curr_q][-1][ans_d[curr_q]]),str(final_ans),q_exams[curr_q][1]))
        qs=tk.StringVar()
        fC=tk.Frame(fB,width=740,height=680,borderwidth=10,bg="#d5f3f7")
        fC.place(x=0,y=200)
        lb2=tk.Label(fC,text='Choose Question : ',font=font1)
        lb_question=tk.Label(fC,font=font2)
        lb_answer=tk.Label(fC,font=font2)
        qs_choose=ttk.Combobox(fC,width=15,textvariable=qs)
        qs_choose['values']=[]
        qs_choose.bind('<<ComboboxSelected>>',q_change)
        lb2.place(x=0,y=0)
        qs_choose.place(x=200,y=0)
        lb_question.place(x=0,y=100)
        lb_answer.place(x=0,y=200)
        try:
            con=m.connect(host=db_host,port=db_port,user=db_usn,password=db_pwd,database=db_name)       
            cur=con.cursor()
            cur.execute('SELECT ques from pending_exams where code="{}"'.format(qps.get()))
            data1=cur.fetchall()
            cur.execute('SELECT answer from com_exam where code="{}" and usn_stu="{}" and checked is not NULL'.format(qps.get(),usn))
            data2=cur.fetchall()
            con.close()
            q_exams=[]
            ans_d={}
            if len(data1)!=0 and len(data2)!=0:
                data1=eval(data1[0][0])
                data2=eval(data2[0][0])
                val=[]
                marks=0
                for i in range(len(data1)):
                    if data1[i]:
                        q_exams.append(data1[i])
                        val.append('Question : {}'.format(i+1))
                        marks+=int(q_exams[i][1])
                for i in range(len(data2)):
                    if data2[i]:
                        ans_d[data2[i][0]]=data2[i][1]
                qs_choose['values']=val
            else:
                messagebox.showerror('Error','Your answers are yet to be Evaluated!')
                clear_frame(fB)
                return False
        except (m.errors.InterfaceError,m.errors.DatabaseError) :
            mesagebox.showerror('Error','Please Connect to the Internet!')
            return False
        stu_marks=0
        for i in ans:
            if i==qps.get():
                for j in  ans[qps.get()]:
                    stu_marks+=j[1]
        lb_totalmarks=tk.Label(fC,text="Marks Scored : {}/{}".format(stu_marks,marks),font=font1)
        lb_totalmarks.place(x=350,y=0)  
    qps=tk.StringVar()
    lb1=tk.Label(fB,text='Choose Answer Paper :',font=font2)
    btn_cd=tk.Button(fB,text='See Results',font=font1,command=exam_change)
    qp_choose=ttk.Combobox(fB,width=10,textvariable=qps)
    qp_choose['values']=exams_l
    lb1.place(x=0,y=100)
    qp_choose.place(x=200,y=100)
    btn_cd.place(x=300,y=100)
