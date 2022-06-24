import tkinter as tk
import tkinter.font as font
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as m
from datetime import datetime,timedelta
import secrets
import string

from sample_frames import ScrollableFrame
db_host='sql3.freemysqlhosting.net'
db_port=3306
db_pwd='BREglSJFnR'
db_usn='sql3470461'
db_name='sql3470461'



def clear_frame(*frame):
    for i in frame:
        for widgets in i.winfo_children():
            widgets.destroy()


def teacherhome(*par):
    global font1,font2,window,fA,fB,usn,usn_name,loginpage
    window=par[0]#par[0] window
    fA=par[1]#par[1] fA
    fB=par[2]#par[2] fB
    usn_name=par[3]#---->par[3] name
    #par[6] usn
    loginpage=par[-1]
    font1=par[4]
    font2=par[5]
    usn=par[6]
    clear_frame(fA,fB)

    lb1=tk.Label(fA,text=(" Hello "+usn_name.title()),font=font1)
    
    lb1.place(x=10,y=10)

    btn1=tk.Button(fA,text="CREATE NEW EXAM",font=font2,command=lambda : createtest(fA,fB))
    btn2=tk.Button(fA,text="WORK ON DRAFTS",font=font2,command=draftwork)
    btn3=tk.Button(fA,text="EVALUATE EXAMS",font=font2,command=evaluate)
    try:
        loginpage=par[-1]
    except NameError:
        loginpage=par[-1]
    finally:
        btn5=tk.Button(fA,text="LOGOUT",font=font2,command=lambda :loginpage())
    
    btn1.place(x=5,y=170)
    btn2.place(x=5,y=250)
    btn3.place(x=5,y=320)
    btn5.place(x=5,y=630)

def createtest(*par):
    global fA,fB,fD,options_lb,options_ent,fC,total_qs,total_qs_l,fC_qp
    fA=par[0]#par[0] fA
    fB=par[1]#par[1] fB
    clear_frame(fB)
    choice=tk.StringVar()
    redirect=False
    #par[-1]=Condition To Be Redirected From Draft
    try:
        if par[2]==False:
            options_lb={}
            options_ent={}
            total_qs={}
            total_qs_l_temp=par[3]
            total_qs_l=[]
            redirect=True
    except IndexError:
        options_lb={}
        options_ent={}
        total_qs={}
        total_qs_l=[]
        
        
    fC=tk.Frame(master=fB,width=720,height=100,borderwidth=10,bg="#cfdee3")
    fC.place(x=0,y=0)
    fD=tk.Frame(master=fB,height=900,width=720,bg="#d5f3f7")
    fD.place(x=0,y=200)

    fC_master=tk.Frame(fC,height=100,width=720)
    fC_qp_c=ScrollableFrame(fC_master,height=500,width=720)
    fC_qp=fC_qp_c.frame
    fC_master.place(x=0,y=0)

    lb1=tk.Label(fB,text=" Type of Question : ",font=font2)
    lb_totalqs=tk.Label(fC,text=" Number of Questions : ",font=font2)
    lb_totalmarks=tk.Label(fC,text=" Total Marks : ",font=font2)

    lb_totalqs.place(x=500,y=30)
    lb_totalmarks.place(x=500,y=60)
    lb1.place(x=0,y=100)
    
    r1 = tk.Radiobutton(fB, text="MCQ", variable=choice, value='mcq',font=font2,command=lambda :radio1(choice.get(),False))
    r2 = tk.Radiobutton(fB, text="ENTRY", variable=choice, value='ent',font=font2,command=lambda :radio1(choice.get(),False))

    r1.place(x=20,y=130)
    r2.place(x=100,y=130)
    r1.deselect()
    r2.deselect()

    lb_marks=tk.Label(fB,text=" Number of Marks : ",font=font2)
    lb_marks.place(x=0,y=180)
    ent_marks=tk.Entry(fB)
    ent_marks.place(x=200,y=180)
    
    btn1=tk.Button(fB,text='ADD QUESTION',font=font2,command=lambda:addq(choice.get(),ent_marks.get(),lb_totalqs,lb_totalmarks,True))
    btnsave=tk.Button(fB,text='SAVE DRAFT',font=font2,command=save_d)
    btnpush=tk.Button(fB,text='SAVE EXAM',font=font2,command=save_e)
    if redirect and len(fC_qp.winfo_children())==0:
        for i in total_qs_l_temp:
            total_qs_l.append(i)
            addq(i[0],i[1],lb_totalqs,lb_totalmarks,False,i[2])
            
    btn1.place(x=0,y=630)
    btnsave.place(x=200,y=630)
    btnpush.place(x=400,y=630)
def radio1(*par):
    global fA,fB,window,fD,options_ent,options_lb
    clear_frame(fD)
    lb2=tk.Label(fD,text="",font=font2)
    choice=par[0]
    reset=par[1]
    if reset==True:
        for i in fB.winfo_children():
            if type(i)==tk.Radiobutton:
                i.invoke()
                i.select()
                clear_frame(fD)
                break
    if choice=='mcq':
        #lb2['text']='MCQ CHOSEN'

        lb3=tk.Label(fD,text="Enter\nQuestion : ",font=font2)
        lb3.place(x=0,y=40)
        lb4=tk.Label(fD,text="Number of Options : ",font=font2)
        lb4.place(x=0,y=100)
        lb5=tk.Label(fD,text="0",font=font2)
        lb5.place(x=200,y=100)
        
        ent1=tk.Text(fD,width=50,height=3)
        scroll1 = tk.Scrollbar(fD)
        ent1.configure(yscrollcommand=scroll1.set)
        ent1.place(x=100,y=40)
        
        scroll1.config(command=ent1.yview)
        scroll1.place(x=505,y=40)

        fD_options=tk.Frame(fD,height=300,width=720,bg="#d5f3f7")
        
        fD_options_c=ScrollableFrame(fD_options,height=1100,width=720)
        fD_options_sub=fD_options_c.frame
        fD_options.place(x=100,y=150)
        
        btn2=tk.Button(fD,text='-',font=font2,command= lambda : removeoption(lb5,fD_options_sub))
        btn3=tk.Button(fD,text='+',font=font2,command=lambda : addoption(lb5,fD_options_sub))
        btn2.place(x=150,y=100)
        btn3.place(x=250,y=100)
        
        
        #for i in range(1,3):
        #    options_lb['lb'+str(i)]=tk.Label(fD_options_sub,text="Option "+str(i)+' : ',font=font2)
        #    options_ent['ent'+str(i)]=tk.Entry(fD_options_sub)

        #    options_lb['lb'+str(i)].pack(side=tk.TOP)
        #    options_ent['ent'+str(i)].pack(side=tk.TOP)
    elif choice=='ent':
        lb2['text']='Enter \nQuestion : '
        ent1=tk.Text(fD,width=50,height=3)
        scroll1 = tk.Scrollbar(fD)
        ent1.configure(yscrollcommand=scroll1.set)
        ent1.place(x=100,y=40)
        
        scroll1.config(command=ent1.yview)
        scroll1.place(x=505,y=40)
        lb2.place(x=0,y=40)
def addoption(lb,frame):
    global options_lb,options_ent
    if lb['text']=='20':
        messagebox.showerror('LIMIT REACHED','Maximum of only 20 options allowed!')
        return False
    lb['text']=str(int(lb['text'])+1)
    options_lb['lb'+str(lb['text'])]=tk.Label(frame,text="Option "+str(lb['text'])+' : ',font=font2)
    options_ent['ent'+str(lb['text'])]=tk.Entry(frame)
    
    options_lb['lb'+str(lb['text'])].pack(side=tk.TOP)
    options_ent['ent'+str(lb['text'])].pack(side=tk.TOP)

    
    
def removeoption(lb,frame):
    
    global options_lb,options_ent
    if int(lb['text'])==2:
        messagebox.showerror("Error",'Should have alteast 2 options')
        return False
        
    num=str(lb['text'])
    options_lb['lb'+num].destroy()
    options_ent['ent'+num].destroy()
    del options_lb['lb'+num]
    del options_ent['ent'+num]

    lb['text']=str(int(lb['text'])-1)
def addq(*l):
    try:
        #l[0]==choice
        #l[1]==marks
        global fD,options_ent,fC,total_qs,options_lb,total_qs_l,fC_qp
        if l[4]==False:
            ques=l[5]#bypass draft
        else:
            for i in fD.winfo_children():
                if type(i)==tk.Text:
                    ques=i.get(1.0,"end-1c").strip()
                    if ques=='':
                        messagebox.showerror('Error','Please Enter A Question!')
                        return False
        if l[0]=='mcq' and l[4]==True:#when user actually clikced the btn
            if len(list(options_ent.keys()))<2:
                messagebox.showerror('Error','Enter Atleast 2 Options')
                return False
            
            for i in options_ent:
                if options_ent[i].get()=='':
                    messagebox.showerror('Error','Please Fill in All Options!')
                    return False
        if l[1]=='':
            messagebox.showerror('Error','Please Enter Number of Marks to be Awarded!')
            return False
        for i in l[1]:
            if ord(i)<48 or ord(i)>57:
                messagebox.showerror('Error','Please Enter Only Digits in Number of Marks')
                return False
        
        full_q=[l[0],l[1],ques]
        if l[0]=='mcq':
            x=[]
            for i in options_ent:
                x.append(options_ent[i].get())
            full_q.append(x)
        elif l[0]=='ent':
            pass
        if l[4]==True:
            total_qs_l.append(full_q)
        
        if l[0]=='mcq' :
            total_qs[str(len(total_qs_l))]=tk.Label(fC_qp,text='Question '+str(len(total_qs_l))+' (MCQ) : '+str(ques))
            total_qs[str(len(total_qs_l))].pack(side=tk.TOP)
            
        elif l[0]=='ent':
            total_qs[str(len(total_qs_l))]=tk.Label(fC_qp,text='Question '+str(len(total_qs_l))+' (ENTRY) : '+str(ques))
            total_qs[str(len(total_qs_l))].pack(side=tk.TOP)
        sum1=0
        for i in range(len(total_qs_l)):
            sum1+=int(total_qs_l[i][1])
        l[2]['text']='Number of Questions : '+ str(len(total_qs_l))
        l[3]['text']='Total Marks : '+str(sum1)
        
        options_ent={}
        options_lb={}
        radio1('mcq',True)
        
        
    except NameError as e:
        messagebox.showerror("Error","Please Choose a Type Of Question First!")
        return False

def save_e(*l):
    global total_qs_l,window,fA,fB,usn_name,font1,font2,usn
    if len(total_qs_l)!=0:
        clear_frame(fB)
        lb_dur=tk.Label(fB,text='Duration of Test\n(Hours/Minutes/Seconds) : ',font=font2)
        lb_start=tk.Label(fB,text='Start Time \n(Hours/Minutes/Seconds) : ',font=font2)
        lb_sdate=tk.Label(fB,text='Start Date \n(YYYY/MM/DD) : ',font=font2)
        
        lb_end=tk.Label(fB,text='End Time : ',font=font2)
        lb_edate=tk.Label(fB,text='End Date : ',font=font2)
        
        lb_meetingcode=tk.Label(fB,text='Meeting Code : ',font=font2)
        
        lb_dur.place(x=50,y=100)
        lb_start.place(x=50,y=200)
        lb_sdate.place(x=50,y=300)

        lb_end.place(x=50,y=400)
        #lb_edate.place(x=50,y=500)
        lb_meetingcode.place(x=50,y=400)

        val=['00','01', '02', '03', '04', '05', '06', '07', '08', '09','10', '11', '12',
                      '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23',
                      '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34',
                      '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45',
                      '46', '47','48', '49', '50', '51', '52', '53', '54', '55', '56',
                      '57', '58', '59']
        
        
        hr_s = tk.StringVar()
        mini_s=tk.StringVar()
        sec_s=tk.StringVar()

        hr_dur_s=tk.StringVar()
        mini_dur_s=tk.StringVar()
        sec_dur_s=tk.StringVar()

        hr_dur=ttk.Combobox(fB, width = 3, textvariable = hr_dur_s)
        mini_dur=ttk.Combobox(fB, width = 3, textvariable = mini_dur_s)
        sec_dur=ttk.Combobox(fB, width = 3, textvariable = sec_dur_s)
        hr_dur['values']=val[:24]
        mini_dur['values']=val[:]
        sec_dur['values']=val[:]

        hr_dur['state']='readonly'
        mini_dur['state']='readonly'
        sec_dur['state']='readonly'

        
        hr = ttk.Combobox(fB, width = 3, textvariable = hr_s)
        hr['values']=val[:24]
        mini=ttk.Combobox(fB, width = 3, textvariable = mini_s)
        mini['values']=val[:]

        sec=ttk.Combobox(fB, width = 3, textvariable = sec_s)
        
        
        sec['values']=val[:]
        hr['state']='readonly'
        mini['state']='readonly'
        sec['state']='readonly'
        

        hr.place(x=300,y=200)
        mini.place(x=400,y=200)
        sec.place(x=500,y=200)

        hr_dur.place(x=300,y=100)
        mini_dur.place(x=400,y=100)
        sec_dur.place(x=500,y=100)
        day_s=tk.StringVar()
        month_s=tk.StringVar()
        year_s=tk.StringVar()

        day=ttk.Combobox(fB,width=3,textvariable=day_s)
        month=ttk.Combobox(fB,width=3,textvariable=month_s)
        year=ttk.Combobox(fB,width=4,textvariable=year_s)
        def month_change(event):
            m=int(month_s.get())
            if m in [1,3,5,7,8,10,12]:
                #31days
                day['state']='normal'
                day['values']=['01', '02', '03', '04', '05', '06', '07', '08', '09','10', '11', '12','13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23','24', '25', '26', '27', '28', '29', '30', '31']
                day.current(0)
                day['state']='readonly'
            elif m in [4,6,9,11]:
                #30 days
                day['state']='normal'
                day['values']=['01', '02', '03', '04', '05', '06', '07', '08', '09','10', '11', '12','13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23','24', '25', '26', '27', '28', '29', '30']
                day.current(0)
                day['state']='readonly'
            elif m==2:
                day['state']='normal'
                day['values']=['01', '02', '03', '04', '05', '06', '07', '08', '09','10', '11', '12','13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23','24', '25', '26', '27', '28']
                day.current(0)
                day['state']='readonly'
                if year_s.get()!='':
                    if int(year_s.get())%4==0:
                        day['state']='normal'
                        day['values']=['01', '02', '03', '04', '05', '06', '07', '08', '09','10', '11', '12','13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23','24', '25', '26', '27', '28','29']
                        day.current(0)
                        day['state']='readonly'
                    else:
                        day['state']='normal'
                        day['values']=['01', '02', '03', '04', '05', '06', '07', '08', '09','10', '11', '12','13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23','24', '25', '26', '27', '28']
                        day.current(0)
                        day['state']='readonly'
        def day_change(event):
            pass
        def year_change(event):
            y=int(year_s.get())
            if month_s.get()!='':
                if y %4==0:
                    if int(month_s.get())==2:
                        day['state']='normal'
                        day['values']=['01', '02', '03', '04', '05', '06', '07', '08', '09','10', '11', '12','13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23','24', '25', '26', '27', '28','29']
                        day.current(0)
                        day['state']='readonly'
                else:
                    if int(month_s.get())==2:
                        day['state']='normal'
                        day['values']=['01', '02', '03', '04', '05', '06', '07', '08', '09','10', '11', '12','13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23','24', '25', '26', '27', '28']
                        day.current(0)
                        day['state']='readonly'
            else:
                day['state']='normal'
                day['values']=['01', '02', '03', '04', '05', '06', '07', '08', '09','10', '11', '12','13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23','24', '25', '26', '27', '28','29','30','31']
                day.current(0)
                day['state']='readonly'
        


        day['values']=['01', '02', '03', '04', '05', '06', '07', '08', '09','10', '11', '12','13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23','24', '25', '26', '27', '28', '29', '30', '31']
        month['values']=['01', '02', '03', '04', '05', '06', '07', '08', '09','10', '11', '12']
        year['values']=['2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027','2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035','2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043','2044', '2045', '2046', '2047', '2048', '2049', '2050', '2051','2052', '2053', '2054', '2055', '2056', '2057', '2058', '2059','2060', '2061', '2062', '2063', '2064', '2065', '2066', '2067','2068', '2069', '2070', '2071', '2072', '2073', '2074', '2075','2076', '2077', '2078', '2079', '2080', '2081', '2082', '2083','2084', '2085', '2086', '2087', '2088', '2089','2090', '2091','2092', '2093', '2094', '2095', '2096', '2097', '2098', '2099']
        day['state'] = 'readonly'
        month['state'] = 'readonly'
        year['state'] = 'readonly'
        month.bind('<<ComboboxSelected>>', month_change)
        day.bind('<<ComboboxSelected>>', day_change)
        year.bind('<<ComboboxSelected>>', year_change)

        day.place(x=500,y=300)
        month.place(x=400,y=300)
        year.place(x=300,y=300)
        
        btn_push_e=tk.Button(fB,text='Submit',font=font1,command=lambda : on_submit_test([hr_s,mini_s,sec_s],[hr_dur_s,mini_dur_s,sec_dur_s],[year_s,month_s,day_s],
                                                                                         total_qs_l,code))
        btn_push_e.place(x=200,y=600)
        try:
            con=m.connect(host=db_host,port=db_port,user=db_usn,password=db_pwd,database=db_name)       
            cur=con.cursor()
            cur.execute('SELECT code from pending_exams')
            data=cur.fetchall()
            T=True
            while T:
                code=''
                for i in range(8):
                    code+=secrets.choice(string.ascii_uppercase+string.digits)
                if len(data)==0:
                    break
                loop=True
                for i in data:
                    #irepresents meeting code
                    if i[0]==code:
                        loop=False
                        break
                if loop==True:
                    T=False
                    break
                elif loop==False:
                    pass
                    
            lb_meetingcode['text']='Meeting Code : \t\t'+code
            #code is gen        
        except (m.errors.InterfaceError,m.errors.DatabaseError):
            messagebox.showerror('No Internet','Please check your connection to the Internet!')
            save_d()
            clear_frame(fB)
            return False
            #WORK HERE TO SAVEDATA LOCALLY
    else:
        messagebox.showerror("Error","Please Create A Test First!")
        return False
def on_submit_test(*par):
    font1,font2,window,fA,fB,usn
    #l[0]=start time
    #l[1]=duration time
    #l[2]=start date
    #par[3]=total_qs_l
    #par[4]=code
    code=par[4]
    
    for i in par[:3]:
        for j in i:
            if j.get()=='':
                messagebox.showerror("Error","Please Fill In All Fields!")
                return False
    l=[]
    for i in par[:3]:
        x=[]
        for j in i:
            x.append(int(j.get()))
        l.append(x)
    start_datetime=datetime(l[2][0],l[2][1],l[2][2],l[0][0],l[0][1],l[0][2])
    dur_time=timedelta(hours=l[1][0],minutes=l[1][1],seconds=l[1][2])
    if (start_datetime<datetime.now()):
        messagebox.showerror("Error","Please Enter a Start Time that is 5 Minutes From Current Time")
        return False
    end_datetime=((datetime(l[2][0],l[2][1],l[2][2],l[0][0],l[0][1],l[0][2]))+timedelta(hours=l[1][0],minutes=l[1][1],seconds=l[1][2]))
    try:
        con=m.connect(host=db_host,port=db_port,user=db_usn,password=db_pwd,database=db_name)
        cur=con.cursor()
        cur.execute('insert into pending_exams(code,tea_usn,start,end,dur,ques) values ("{}","{}","{}","{}","{}","{}")'.format(code,usn,str(start_datetime),str(end_datetime),str(dur_time),str(par[3])))
        con.commit()
        con.close()
        messagebox.showinfo("Exam","Exam Successfully Added!")
        teacherhome(window,fA,fB,usn_name,font1,font2,usn,loginpage)
        
        return False
    except (m.errors.InterfaceError,m.errors.DatabaseError):
        messagebox.showerror('No Internet','Please check your connection to the Internet!')
        return False
def draftwork():
    global fA,fB,usn_name,font1,font2,usn,options_lb,options_ent,total_qs
    clear_frame(fB)
    total_qs_l=[]
    options_lb={}
    options_ent={}
    total_qs={}
    try:
        with open('cache\\draft_qp_tea.txt','r') as f:
            drafts=f.readlines()
            f.close()
    except FileNotFoundError:
        messagebox.showerror('Test Error','You have no previous drafts!')
        return False
    def changedraft(event):
        num=int(((qps.get()).split())[-1])#get question '1'
        total_qs_l_temp=eval(drafts[num-1])
        str1=''
        cnt=1
        for i in total_qs_l_temp:
            if i[0]=='mcq':
                a='MCQ'
            elif i[0]=='ent':
                a='ENTRY'
            str1+=' QUESTION {}:({}) {} ({} Marks)\n'.format(cnt,a,i[2],i[1])
            cnt+=1
        lb_showd.config(state='normal')
        lb_showd.delete('1.0',tk.END)
        lb_showd.insert('1.0',str1)
        lb_showd.config(state='disabled')
    def choosedraft():
        num=int(((qps.get()).split())[-1])
        total_qs_l_temp=eval(drafts[num-1])
        createtest(fA,fB,False,total_qs_l_temp)
    total_qp=[]
    for i in range(1,len(drafts)+1):
        total_qp.append('Draft '+str(i))
    qps=tk.StringVar()
    lb1=tk.Label(fB,text='Choose Draft :',font=font2)
    btn_cd=tk.Button(fB,text='Continue',font=font1,command=choosedraft)
    qp_choose=ttk.Combobox(fB,width=7,textvariable=qps)
    qp_choose['values']=total_qp
    lb_showd=tk.Text(fB,width=70,height=10,bg="#cfdee3")
    lb_showd.config(state='disabled')
    scroll1 = tk.Scrollbar(fB)
    lb_showd.configure(yscrollcommand=scroll1.set)
    lb_showd.place(x=0,y=200)
    scroll1.config(command=lb_showd.yview)
    scroll1.place(x=565,y=200)
    qp_choose.place(x=200,y=100)
    lb1.place(x=0,y=100)
    btn_cd.place(x=100,y=450)
    qp_choose.bind('<<ComboboxSelected>>', changedraft)    
def save_d(*l):
    global total_qs_l
    with open('cache\\draft_qp_tea.txt','a') as f:
        f.write(str(total_qs_l)+'\n')
        f.close()
def evaluate():
    global fA,fB,usn_name,font1,font2,usn,options_lb,options_ent,total_qs,loginpage
    clear_frame(fB)
    total_qs_l=[]
    options_lb={}
    options_ent={}
    total_qs={}
    def exam_change(event):
        if len(stu_choose['values'])>1:
            stu_choose.current(0)
        try:
            con=m.connect(host=db_host,port=db_port,user=db_usn,password=db_pwd,database=db_name)       
            cur=con.cursor()
            nowtime=datetime.now().strftime('%y-%m-%d %H:%M:%S')
            cur.execute('SELECT com_exam.usn_stu,stu.nam from com_exam,stu where com_exam.code="{}" and com_exam.usn_tea="{}" and com_exam.checked is NULL and com_exam.usn_stu=stu.usn'.format(qps.get(),usn,nowtime))
            data_attend=cur.fetchall()
            cur.execute('select code from pending_exams where end>"{}" and tea_usn="{}"'.format(nowtime,usn))
            data_time=cur.fetchall()
            con.close()
            for j in data_time:
                if j[0]==qps.get():
                    messagebox.showerror('Exam Incomplete','Exam is Still Being Conducted!')
                    return False
            if len(data_attend)!=0:
                sm=[]
                for i in data_attend:
                    sm.append('{} : {}'.format(i[1],i[0]))
                stu_choose['values']=sm
                data_attend=sm
            else:
                messagebox.showinfo('Exam Incomplete','No Students\' are left to be Evaluated!')
                return False
        except (m.errors.InterfaceError,m.errors.DatabaseError) :
            mesagebox.showerror('Error','Please Connect to the Internet!')
            return False
    def evaluate_page():
        if qps.get()=='' and st.get()=='':
            messagebox.showerror('Incomplete Fields','Please Fill in  All Fields')
            return False
        def ques_change(event):
            def add_mark(*l):
                if l[1]=='':
                    messagebox.showerror('Error','Enter Marks!')
                    return False
                for i in l[1]:
                    if i.isdigit()==False:
                        messagebox.showerror('Error','Enter Marks in Numbers')
                        return False
                if int(question_l[curr_q][1])<int(l[1]):
                    messagebox.showerror('Error','Mark Entered Is Greater than Mark assigned to this question.')
                    return False
                try:
                    with open('cache\\check_exam.txt','r') as f:
                        txt_showd['state']='normal'
                        str3=[]
                        str3=(txt_showd.get("1.0","end")).split('\n')[:-1]
                        txt_showd.delete("1.0", "end")
                        str3[curr_q]='Question {} : Checked'.format(curr_q+1)
                        txt_showd.insert(tk.END,"\n".join(str3))
                        txt_showd['state']='disabled'
                        f.seek(0)
                        x=False
                        x_=False
                        sm1=f.readlines()
                        for i in range(len(sm1)):
                            txt=sm1[i].split('\t')
                            if txt[0]==code and txt[1]==usn_stu:
                                local=eval(txt[2])
                                x=True
                                for j in range(len(local)):
                                    if int(local[j][0])==int(l[0]):
                                        local[j][1]=int(l[1])
                                        x_=True
                                        break
                                if x_==False:
                                    local.append([l[0],int(l[1])])
                                f.close()
                                sm1[i]='{}\t{}\t{}\n'.format(txt[0],usn_stu,str(local))
                    with open('cache\\check_exam.txt','w') as f:
                        f.writelines(sm1)
                        f.close()
                    if x==False:
                        with open('cache\\check_exam.txt','a') as f:
                            sam='{}\t{}\t{}'.format(code,usn_stu,str([[l[0],int(l[1])]]))
                            f.write(str(sam)+'\n')

                            txt_showd['state']='normal'
                            str3=(txt_showd.get("1.0","end")).split('\n')[:-1]
                            txt_showd.delete("1.0", "end")
                            str3[curr_q]='Question {} : Checked'.format(curr_q+1)
                            txt_showd.insert(tk.END,"\n".join(str3))
                            txt_showd['state']='disabled'
                            f.close()
                except (FileNotFoundError,EOFError):
                    with open('cache\\check_exam.txt','w') as f:
                        sam='{}\t{}\t{}'.format(code,usn_stu,str([[l[0],int(l[1])]]))

                        txt_showd['state']='normal'
                        str3=(txt_showd.get("1.0","end")).split('\n')[:-1]
                        txt_showd.delete("1.0", "end")
                        str3[curr_q]='Question {} : Checked'.format(curr_q+1)
                        txt_showd.insert(tk.END,"\n".join(str3))
                        txt_showd['state']='disabled'

                        f.write(str(sam)+'\n')
                        f.close()
            def push_db():
                try:
                    with open('cache\\check_exam.txt','r') as f:
                        sm=f.readlines()
                        attended_qs=[]
                        for i in sm:
                            txt=i.split('\t')
                            if txt[0]==code and txt[1]==usn_stu:
                                attended_qs=eval(txt[2])
                        if len(attended_qs)<len(question_l):
                            messagebox.showerror('Error','Check All the Questions First!')
                            return False
                except FileNotFoundError:
                    messagebox.showerror('Error','Check All the Questions First!')
                    return False
                try:
                    clear_frame(fB)
                    con=m.connect(host=db_host,port=db_port,user=db_usn,password=db_pwd,database=db_name)       
                    cur=con.cursor()
                    cur.execute('update com_exam set checked="{}" where code="{}" and usn_stu="{}"'.format(attended_qs,code,usn_stu))
                    con.commit()
                    con.close()
                    messagebox.showinfo('Correction Completed','You have succesfully corrected the Exam!')
                    
                    evaluate()
                    return False
                except (m.errors.InterfaceError,m.errors.DatabaseError):
                    messagebox.showerror('Error','Please Connect to the Internet')
                    return False
            clear_frame(fD)
            lb_ques=tk.Label(fD,text='',font=font2)
            lb_ques.place(x=0,y=0)
            lb_askmark=tk.Label(fD,text='Enter Mark : ',font=font2)
            mark_s=tk.Entry(fD)
            lb_askmark.place(x=0,y=200)
            mark_s.place(x=200,y=200)
            btn_savea=tk.Button(fD,text='ADD MARK',font=font1,command=lambda:add_mark(curr_q,mark_s.get()))
            btn_quitsave=tk.Button(fD,text='QUIT AND SAVE EVALUATION',font=font1,command=push_db)

            btn_savea.place(x=0,y=400)
            btn_quitsave.place(x=300,y=400)
            curr_q=int(current_ques.get().split()[-1])-1
            lb_ques.config(text=question_l[curr_q][2]+' ('+str(question_l[curr_q][1]+' Marks)'))
            try:
                with open('cache\\check_exam.txt','r') as f:
                    mark_s.delete(0,"end")
                    sm=f.readlines()
                    for i in sm:
                        txt=i.split('\t')
                        if txt[0]==code and txt[1]==usn_stu:
                            for j in eval(txt[2]):
                                if j[0]==curr_q:
                                    mark_s.insert(0,str(j[1]))
                                    break

                            
            except FileNotFoundError:
                pass
            
            if question_l[curr_q][0]=='ent':
                ent_ans=tk.Text(fD,width=50,height=3)
                scroll1 = tk.Scrollbar(fD)
                ent_ans.configure(yscrollcommand=scroll1.set)
                ent_ans.place(x=0,y=100)
                scroll1.config(command=ent_ans.yview)
                scroll1.place(x=405,y=100)
                ent_ans.config(state='normal')
                ent_ans.delete('1.0',tk.END)
                try:
                    if stu_ans[curr_q]:
                        ent_ans.insert('1.0',stu_ans[curr_q])
                except KeyError:
                    ent_ans.insert('1.0',"")
                ent_ans.config(state='disabled')
            elif question_l[curr_q][0]=='mcq':
                try:
                    if stu_ans[curr_q] or True:
                        choice=tk.StringVar()
                        rb=tk.Radiobutton(fD,text=question_l[curr_q][3][stu_ans[curr_q]], variable=choice, value=str(stu_ans[curr_q]),font=font2)
                        rb.place(x=0,y=100)
                        rb.configure(state=tk.DISABLED)
                except KeyError:
                    lb_remark=tk.Label(fD,text='Student Hasn\'t Answered This Question',font=font2)
                    lb_remark.place(x=0,y=100)
        code=qps.get()
        usn_stu=st.get().split()[-1]
        clear_frame(fB)
        fC=tk.Frame(master=fB,width=720,height=100,borderwidth=10,bg="#cfdee3")
        fC.place(x=0,y=0)
        fD=tk.Frame(master=fB,height=650,width=720,bg="#d5f3f7")
        fD.place(x=0,y=200)
        txt_showd=tk.Text(fC,width=30,height=3,bg='#cfdee3')
        try:
            con=m.connect(host=db_host,port=db_port,user=db_usn,password=db_pwd,database=db_name)       
            cur=con.cursor()
            cur.execute('SELECT answer from com_exam where code="{}" and usn_stu="{}" '.format(code,usn_stu))
            question_l_ans=(cur.fetchall())
            if len(question_l_ans)>0:
                question_l_ans=eval(question_l_ans[0][0])
                cur.execute('SELECT ques from pending_exams where code="{}" and tea_usn="{}" '.format(code,usn))
                dat=cur.fetchall()
                question_l=eval(dat[0][0])
                stu_ans={}
                for i in question_l_ans:
                    stu_ans[i[0]]=i[1]
                total_marks=0
                for i in question_l:
                    total_marks+=int(i[1])
                con.close()
            else:
                messagebox.showerror('Incomplete','Student hasn\'t answered any questions!')
                return False
        except (m.errors.InterfaceError,m.errors.DatabaseError) :
            mesagebox.showerror('Error','Please Connect to the Internet!')
            return False    
        try:
            txt_showd['state']='normal'

            with open('cache\\check_exam.txt','r') as f:
                T=False
                f.seek(0)
                sm=f.readlines()
                for i in sm:
                    txt=i.split('\t')
                    gcode=txt[0]
                    gusn=txt[1]
                    local=eval(txt[2])
                    if code==gcode and gusn==usn_stu:
                        str2=[]
                        T=True
                        for i in range(len(question_l)):
                            str2.append('Question {} : Not Checked'.format(i+1))
                        for j in range(len(local)):
                            q2=local[j][0]
                            str2[q2]='Question {} : Checked'.format(q2+1)
                        txt_showd.insert(tk.END,'\n'.join(str2))
                        break
                f.close()
            if T==False:
                str2=''
                for i in range(len(question_l)):
                    str2+='Question {} : Not Checked\n'.format(i+1)
                txt_showd.insert(tk.END,str2)  
        except FileNotFoundError:
            str2=''
            for i in range(len(question_l)):
                str2+='Question {} : Not Checked\n'.format(i+1)
            txt_showd.insert(tk.END,str2)
        lb_num=tk.Label(fC,text="Questions : {}".format(str(len(question_l))),font=font2)
        lb_marks=tk.Label(fC,text="Total Marks : {}".format(str(total_marks)),font=font2)
        lb_code=tk.Label(fC,text="CODE : {}".format(code),font=font2)
        lb_questions=tk.Label(fB,text="CHOOSE QUESTION",font=font2)
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
    try:
        con=m.connect(host=db_host,port=db_port,user=db_usn,password=db_pwd,database=db_name)       
        cur=con.cursor()
        cur.execute('SELECT code from pending_exams where tea_usn="{}" '.format(usn))
        data_exams=cur.fetchall()
        data_attend=[]
        con.close()
        exams_l=[]
        if len(data_exams)==0:
            messagebox.showerror('Error','Create An Exam First!')
            clear_frame(fB)
            return False
        else:
            for i in data_exams:
                exams_l.append(i[0])
            
        con.close()
    except (m.errors.InterfaceError,m.errors.DatabaseError) :
        mesagebox.showerror('Error','Please Connect to the Internet!')
        return False
    qps=tk.StringVar()
    st=tk.StringVar()
    lb1=tk.Label(fB,text='Choose Question :',font=font2)
    lb2=tk.Label(fB,text='Choose Student :',font=font2)
    btn_cd=tk.Button(fB,text='Continue',font=font1,command=evaluate_page)
    qp_choose=ttk.Combobox(fB,width=8,textvariable=qps)
    qp_choose['values']=exams_l
    qp_choose.bind('<<ComboboxSelected>>',exam_change)
    stu_choose=ttk.Combobox(fB,width=20,textvariable=st)
    stu_choose['values']=[]
    lb1.place(x=0,y=100)
    lb2.place(x=0,y=200)
    qp_choose.place(x=200,y=100)
    stu_choose.place(x=200,y=200)
    btn_cd.place(x=100,y=450)
