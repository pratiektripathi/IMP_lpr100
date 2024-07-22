#!/usr/bin/env python3
import datetime
from dateutil.relativedelta import relativedelta
import multiprocessing
import queue as q
import subprocess
import sys
import tkinter as tk
import uuid
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font
import serial
import win32print
from PIL import Image, ImageTk
import db_pg as db
import exel
from tkcalendar import DateEntry
import report2
import templete as temp
import zebrapl
import sqlite3 as lite
import pandas as pd



xuid=0

try:
    chuid=int(db.Lcheck())
    if chuid==1:
        xuid = 1
    else:
        xuid = 0
except:
    xuid = 0




xcom=[]

try:
    xcom=db.loadCom()
except:
    xcom=['COM5', 19200, ' Kg', 0, 8]


com=xcom[0]
baurd=int(xcom[1])
rfind=xcom[2]
Dp=int(xcom[3])
xfilter=int(xcom[4])



class SerialThread(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue
    def run(self):
        try:
            s = serial.Serial(com,baurd, timeout=2)
            while True:
                if xuid==1:
                    k = s.readline().decode('utf-8')
                    data= k.find(rfind)
                    if Dp!=0:
                        text=k[data-5:data-Dp]+"."+k[data-Dp:data]
                    else:
                        text=k.replace(" ","")


                    # text = k
                    self.queue.put(text)
                else:
                    self.queue.put("VerErr")

        except:
            self.queue.put("ComErr")








class MainApp(tk.Tk):


    flag=1
    am=1
    k = []
    i = 0
    r=xfilter


    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        if xuid==1:
            self.title("Impex IMP-100 v1.5 (Activated)")
        else:
            self.title("Impex IMP-100 v1.5(demo)")

        self.iconbitmap('myicon.ico')


        menubar=tk.Menu(self)

        helpmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="Settings", command=self.settings)
        helpmenu.add_separator()
        helpmenu.add_command(label="check for update", command=self.check_for_update)
        self.config(menu=menubar)

        xcord=(self.winfo_screenwidth()/2)-300
        ycord=(self.winfo_screenheight()/2)-300
        

        self.geometry("600x600"+"+"+str(int(xcord))+"+"+str(int(ycord)))


        

        frame1 = tk.Frame(self, bg='white')


        weight_font = Font(family="Arquitecta", size=20)
        Label1_font = Font(family="Arquitecta", size=15)
        Label2_font = Font(family="Arquitecta", size=15)

        field_font = Font(family="Arquitecta", size=10)

        self.bind("<Escape>", lambda e: self.ext())
        self.bind("<Alt_L>" + "<F9>", lambda e: self.destroy())
        self.bind("<F5>", lambda e: self.reconwt())
        self.bind("<Alt_L>" + "<p>", lambda e: self.rePrint())



        self.errtext = tk.StringVar()

        self.hero = tk.StringVar()

        self.TempValue = tk.StringVar()
        self.curentframe = tk.StringVar()
        self.but=tk.StringVar()
        self.but.set(self.am)

        # logo
        framelogo = tk.Frame(frame1)
        im = Image.open('new_impex_logo.gif')

        resized = im.resize((100, 50), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)
        labellogo = tk.Label(framelogo, image=self.image, bg='white')
        labellogo.pack()
        framelogo.grid(row=0, column=0, rowspan=2)

        frame1.grid_columnconfigure(2, weight=1)

        frame_weight = tk.Frame(frame1, bg='white')

        self.label3 = tk.Label(frame_weight, textvariable=self.TempValue, bg="black", fg="red", font=weight_font,
                               width=8, justify='left')
        self.label3.pack(side='left', padx=0, pady=5, ipady=10)

        self.Label2 = tk.Label(frame_weight, text="Kg.", fg="black", bg='white', font=Label2_font).pack(side='left',
                                                                                                        padx=5, pady=0,
                                                                                                        anchor='s')
        frame_weight.grid(row=0, column=4, rowspan=2, columnspan=2, sticky='E')



        self.reconnect=tk.Radiobutton(frame1,font=field_font,text="Auto",variable=self.but,value=1,bg='white',fg='green',activeforeground = 'green',bd=0,activebackground='white',highlightthickness = 0,command=lambda:self.Auto()).grid(row=0,column=3,sticky='SW')
        self.reconnect2=tk.Radiobutton(frame1,font=field_font,text="Manual",variable=self.but,value=2,bg='white',fg='green',activeforeground = 'green',bd=0,activebackground='white',highlightthickness = 0,command=lambda:self.Manual()).grid(row=1,column=3,sticky='NW')

        frame1.pack(anchor="n", fill="both", expand=True)
        # clock
        #         self.clocklabel = tk.Label(frame1, text=self.clock,fg="black",bg='white', font=Label1_font)
        #         self.clocklabel.grid(row=13,column=3,columnspan = 2, padx=6,pady=10,sticky='E')

        self.errlabel = tk.Label(frame1, textvariable=self.errtext, fg="red", bg='white', font=Label1_font)
        self.errlabel.grid(row=13, column=2, columnspan=2, padx=6, pady=10)


        frame1.grid_rowconfigure(11, weight=1)

        container = tk.Frame(frame1, bg='grey')

        container.grid(row=3, column=0, rowspan=4, columnspan=6)

        self.frames = {}

        for F in (StartPage, ComPage, StkSetPage, PasswordPage, PageThree,JobPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame(StartPage)





        self.queue = multiprocessing.Queue()
        self.thread = SerialThread(self.queue)
        self.thread.start()

        self.process_serial()
        self.checkbt()

    def check_for_update(self):
        print("hello")
    
    def settings(self):
        self.frames[PasswordPage].F1()


    def ext(self):
        self.frames[StkSetPage].close()
        self.frames[PasswordPage].close()
        self.frames[PageThree].close()

        #         self.frames[PageFive].close()
        #         self.frames[PageSix].close()
    def Auto(self):
        self.am=1
        self.frames[StartPage].gremove()






    def Manual(self):
        self.am=2
        self.frames[StartPage].backgrid()




    def checkbt(self):
        if self.am==1:

            iwt = None
            if self.i <= self.r and self.i >= 0:
                w = self.TempValue.get()
                if len(w) != 0:
                    try:
                        iwt = float(w)
                    except:
                        pass

                    if iwt is not None:
                        self.k.append(iwt)
                        self.i += 1
                    else:
                        self.i = self.i
                else:
                    pass

            k = self.k

            if len(k)>=self.r:
                if len(set(k)) == 1 :
                    pwt = set(k).pop()
                    self.k = []
                    self.i=0
                    if pwt <= 2 and pwt >= 0:
                        self.flag = 0
                        self.label3.configure(fg="white")

                    elif (pwt > 2 and self.flag == 0):

                        try:
                            self.label3.configure(fg="green")
                            self.zprint()
                            self.flag = 1


                        except:
                            self.flag = 1

                    else:
                        pass

                else:
                    try:
                        self.label3.configure(fg="red")
                    except:
                        pass
                    self.k=[]
                    self.i = 0
        else:
            self.label3.configure(fg="red")
            pass


        self.after(200, self.checkbt)


    def reconwt(self):
        self.queue = multiprocessing.Queue()
        self.thread = SerialThread(self.queue)
        self.thread.start()


    def process_serial(self):
        while self.queue.qsize():
            try:
               data= self.queue.get()
               if (data=='Err') :
                   self.TempValue.set("Err")


               elif (data=='.'):
                   self.TempValue.set("------")


               else:
                   self.TempValue.set(str(data))



            except q.Empty():
                self.TempValue.set("------")
                pass

        self.after(200, self.process_serial)





    def rePrint(self):
        PrintData = db.loadPrint()
        PrinterName = PrintData[0].strip("\n")
        Copy =int(PrintData[1].strip("\n"))

        file = open('zebra.zpl', 'r')
        message= file.read()
        file.close()

        if sys.version_info>=(3,):
            raw_data= bytes(message,"utf-8")
        else:
            raw_data= message


        if len(PrinterName)!=0:
            hprinter=win32print.OpenPrinter(PrinterName)
            try:
                win32print.StartDocPrinter(hprinter, 1,("ticket",None,"RAW"))
                try:
                    win32print.StartPagePrinter(hprinter)
                    win32print.WritePrinter(hprinter, raw_data)
                    win32print.EndPagePrinter(hprinter)
                finally:
                    win32print.EndDocPrinter(hprinter)
            finally:
                win32print.ClosePrinter(hprinter)






    def zprint(self):
        # print("printing")
        try:
            zebrapl.zeepl(self.TempValue.get())
            self.errtext.set("")
        except:
            self.errtext.set("Printer not found")


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        self.hero.set(cont)



class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        frame2 = tk.Frame(self, bg='white',height=600)

        Label1_font = Font(family="Arquitecta", size=14)
        icon = Font(family="Arquitecta", size=11)
        err_font = Font(family="Arquitecta", size=8)


        self.f1 = tk.StringVar()
        self.f2 = tk.StringVar()
        self.f3 = tk.StringVar()
        self.f4 = tk.StringVar()
        self.f5 = tk.StringVar()
        self.f6 = tk.StringVar()
        self.f7 = tk.StringVar()




        self.field1 = tk.StringVar()
        self.field1b = tk.StringVar()
        self.field3 = tk.StringVar()
        self.err=tk.StringVar()
        itrow=db.loadData()
        plno=db.lplno()
        self.field1b.set(str(plno))
        self.field1.set(str(itrow[0]))





        self.controller = controller





        framec4= tk.Frame(frame2, bg='white')


        self.validation=self.register(self.only_number)
        self.errlb = tk.Label(frame2, textvariable=self.err, fg="red", bg='white', height=1, width=20,
                              font=err_font).grid(row=12, column=1, padx=6, pady=5)
        




        self.field_3_label = tk.Label(framec4, text="Gross wt.:",fg="black",bg='white',font=Label1_font)
        self.field_3_label.grid(row=1,column=0, padx=1,pady=5,sticky='e')

        self.feild_3_value = tk.Entry(framec4,fg="black",bg='white', textvariable=self.field3,width=10,validate='key',validatecommand=(self.validation,'%P'), highlightthickness=2,highlightcolor='yellow',font=icon,justify='center',exportselection=0)
        self.feild_3_value.bind("<Return>", lambda e: self.xprint())
        self.feild_3_value.grid(row=1,column=1, padx=1,pady=5,columnspan=2,sticky='w')

        self.field_3_label.grid_remove()
        self.feild_3_value.grid_remove()

        framec4.grid(row=1, column=0,padx=3,sticky='ew',columnspan=5)


        framec2= tk.Frame(frame2, bg='yellow')

        self.field_0b_label = tk.Label(framec2, text='Lot No.:', fg="black", bg='yellow',  font=Label1_font)
        self.field_0b_label.grid(row=0, column=0,padx=3, pady=1,sticky='n')

        self.field_1b_label = tk.Label(framec2, textvariable=self.field1b, fg="black", bg='yellow', font=Label1_font)
        self.field_1b_label.grid(row=0, column=1,padx=3)

        self.field_0_label = tk.Label(framec2, text='Party.:', fg="black", bg='yellow',  font=Label1_font)
        self.field_0_label.grid(row=1, column=0,padx=3, pady=1,sticky='n')

        self.field_1_label = tk.Label(framec2, textvariable=self.field1, fg="black", bg='yellow', font=Label1_font)
        self.field_1_label.grid(row=1, column=1,padx=3)

        framec2.grid(row=2, column=0,padx=3,columnspan=5,sticky='ew')


        framec1 = tk.Frame(frame2,bg='white')

        itrow = temp.loadData()
        Variety=str(itrow[1])
        weight=str(itrow[2])
        CoreWt=str(itrow[3])
        TareWt = str(itrow[4])
        NetWt = str(itrow[5])
        Rollno = str(itrow[6])
        xdate=str(itrow[7])



        self.f1.set("ADITYA FLEXIPACK PVT LTD")
        self.f2.set("Job Name.:"+Variety)
        self.f3.set("Gross wt.:"+weight)
        self.f4.set("Core wt.:"+CoreWt)
        self.f4.set("Tare wt.:" + TareWt)
        self.f5.set("Net wt.:" + NetWt)
        self.f6.set("Roll No..:" + Rollno)
        self.f7.set(xdate)




        self.f1l = tk.Label(framec1,textvariable=self.f1, fg="black", bg='white',  font=Label1_font)
        self.f1l.grid(row=0, column=0,columnspan = 2,padx=3, pady=1,sticky='n')
        self.f2l = tk.Label(framec1, textvariable=self.f2, fg="black",  bg='white',  font=Label1_font)
        self.f2l.grid(row=1, column=0,columnspan =3,padx=3, pady=1,sticky='n')
        self.f3l = tk.Label(framec1, textvariable=self.f3, fg="black",  bg='white',  font=Label1_font)
        self.f3l.grid(row=2, column=0,columnspan = 2,padx=3, pady=1,sticky='n')
        self.f4l = tk.Label(framec1, textvariable=self.f4, fg="black",  bg='white',  font=Label1_font)
        self.f4l.grid(row=3, column=0,columnspan = 2,padx=3, pady=1,sticky='n')
        self.f5l = tk.Label(framec1, textvariable=self.f5, fg="black", bg='white',  font=Label1_font)
        self.f5l.grid(row=4, column=0,columnspan = 2,padx=3, pady=1,sticky='n')
        self.f6l = tk.Label(framec1, textvariable=self.f6, fg="black",  bg='white',  font=Label1_font)
        self.f6l.grid(row=5, column=0,columnspan = 2,padx=3, pady=1,sticky='n')
        self.f7l = tk.Label(framec1, textvariable=self.f7, fg="black", bg='white',  font=Label1_font)
        self.f7l.grid(row=5, column=1,columnspan = 2,padx=3, pady=1,sticky='')


        framec1.grid(row=3,column=0,   padx = 10, pady = 5)






        framec3= tk.Frame(frame2, bg='yellow')

        self.savebut = tk.Button(framec3, text='Change', width=10, bg='lightgrey',font=icon, activebackground='lightgrey',
                                 activeforeground='black', command=lambda: self.Change())

        self.savebut.bind("<Return>", lambda e: self.Change())
        self.savebut.grid(row=1, column=0, padx=5, pady=5 )

        self.reportbut = tk.Button(framec3, text='Packing list', width=15, bg='lightgrey',font=icon, activebackground='lightgrey',
                                 activeforeground='black', command=lambda: self.reporter())

        self.reportbut.bind("<Return>", lambda e: self.reporter())
        self.reportbut.grid(row=1, column=3, padx=5, pady=5 )


        framec3.grid(row=4, column=0,padx=3,sticky='ew',columnspan=5)








        frame2.pack(fill='both', expand= 1)

        controller.bind("<Alt_L>" + "<F6>", lambda e: self.refresh())

    def gremove(self):
        self.field_3_label.grid_remove()
        self.feild_3_value.grid_remove()
        self.controller.focus_set()


    def backgrid(self):
        self.field_3_label.grid()
        self.feild_3_value.grid()
        self.feild_3_value.focus_set()



    def xprint(self):
        if len(self.field3.get())!=0:
            zebrapl.zeepl(self.field3.get())

            try:
                temp.gettkt(self.field3.get())
                pitrow = temp.loadData()
                Variety = str(pitrow[1])
                weight = str(pitrow[2])
                CoreWt = str(pitrow[3])
                TareWt = str(pitrow[4])
                NetWt = str(pitrow[5])
                Rollno = str(pitrow[6])
                xdate = str(pitrow[7])

                self.f1.set("ADITYA FLEXIPACK PVT LTD")
                self.f2.set("Job Name.:" + Variety)
                self.f3.set("Gross wt.:" + weight)
                self.f4.set("Core wt.:" + CoreWt)
                self.f4.set("Tare wt.:" + TareWt)
                self.f5.set("Net wt.:" + NetWt)
                self.f6.set("Roll No..:" + Rollno)
                self.f7.set(xdate)

            except:
                pass
        self.field3.set("")
        self.feild_3_value.focus_set()


    def only_number(self,char):
        if char=="":
            return True

        else:
            try:
                float(char)
            except:
                return False

        return True



    def Change(self):
        self.controller.frames[PageThree].F1()
        # self.controller.frames[PageThree].feild_1_value.focus_set()


    def refresh(self):
        itrow=db.loadData()
        plno=db.lplno()
        self.field1b.set(plno)
        self.field1.set(str(itrow[0]))
        wt = self.controller.TempValue.get()
        try:
            temp.gettkt(wt)
        except:
            temp.gettkt(0)

        pitrow = temp.loadData()
        Variety=str(pitrow[1])
        weight=str(pitrow[2])
        CoreWt=str(pitrow[3])
        TareWt = str(pitrow[4])
        NetWt = str(pitrow[5])
        Rollno = str(pitrow[6])
        xdate=str(pitrow[7])



        self.f1.set("ADITYA FLEXIPACK PVT LTD")
        self.f2.set("Job Name.:"+Variety)
        self.f3.set("Gross wt.:"+weight)
        self.f4.set("Core wt.:"+CoreWt)
        self.f4.set("Tare wt.:" + TareWt)
        self.f5.set("Net wt.:" + NetWt)
        self.f6.set("Roll No..:" + Rollno)
        self.f7.set(xdate)

    def reporter(self):
        window=Report(self)
        window.grab_set()




class Report(tk.Toplevel):

    def __init__(self, parent, **kwargs):
        tk.Toplevel.__init__(self, parent,**kwargs,bg="#ADD8E0")
        s=ttk.Style(self)
        s.theme_use('clam')
       

  

        self.geometry(str(self.winfo_screenwidth())+"x"+str(self.winfo_screenheight()))
        self.state('zoomed')
        self.iconbitmap('myicon.ico')
        self.focus_set()
        self.title("REPORTS")
        self.count = tk.StringVar()
        self.cc = 0
        self.count.set(str(self.cc) + " data marked")
        


        label_font = Font(family="Arquitecta", size=10)
        field_font = Font(family="Arquitecta", size=8)
        fieldx_font = Font(family="Arquitecta", size=10)
        

        frame_but = tk.Frame(self, bg="#ADD8E0")
        frame_but.pack(fill="both", expand=True, padx=30, pady=10,anchor="e")

        frame_top = tk.Frame(self, bg="white")
        frame_top.pack(fill="both", expand=True, padx=10, pady=10)

        botom_frame=tk.Frame(self,bg="#ADD8E0")
        botom_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.errlb = tk.Label(frame_but, textvariable=self.count, fg="black", bg='white', width=30, font=field_font)
        self.errlb.grid(row=0, column=0)

        self.markall = tk.Button(frame_but, text='mark all', width=20, bg='white', activebackground='white',
                                 activeforeground='black', command=lambda: self.mall())
        self.markall.grid(row=0, column=2,padx=4)

        self.umarkall = tk.Button(frame_but, text='unmark all', width=20, bg='white', activebackground='white',
                                  activeforeground='black', command=lambda: self.umall())
        self.umarkall.grid(row=0, column=3,padx=4)


        start_ticket_label = tk.Label(frame_but,font=label_font, text="Start Roll No : ", bg="#ADD8E0")
        start_ticket_label.grid(row=2, column=0, sticky="w")

        self.start_ticket_var = tk.StringVar()
        self.start_ticket_entry = ttk.Entry(frame_but,font=field_font, textvariable=self.start_ticket_var, width=10,validate="key")
        self.start_ticket_entry['validatecommand'] = (self.start_ticket_entry.register(self.validate_positive_int), '%P')
        self.start_ticket_entry.grid(row=2, column=1, padx=5, pady=2, sticky="w")

        end_ticket_label = tk.Label(frame_but,font=label_font, text="End Roll No : ", bg="#ADD8E0")
        end_ticket_label.grid(row=3, column=0, sticky="w")

        self.end_ticket_var = tk.StringVar()
        self.end_ticket_entry = ttk.Entry(frame_but,font=field_font, textvariable=self.end_ticket_var,width=10, validate="key")
        self.end_ticket_entry['validatecommand'] = (self.end_ticket_entry.register(self.validate_positive_int), '%P')
        self.end_ticket_entry.grid(row=3, column=1, padx=5, pady=2, sticky="w")



        start_date_label = tk.Label(frame_but,font=label_font, text="Start Date : ", bg="#ADD8E0")
        start_date_label.grid(row=2, column=2, sticky="w")

        self.start_date_entry = DateEntry(frame_but,font=field_font,state="readonly",background="darkblue",
                                          foreground="white", date_pattern="dd-mm-yyyy", borderwidth=2)
        self.start_date_entry.grid(row=2, column=3, padx=5, pady=2, sticky="w")

        # Add the End Date label and DateEntry
        end_date_label = tk.Label(frame_but,font=label_font, text="End Date : ", bg="#ADD8E0")
        end_date_label.grid(row=3, column=2, sticky="w")

        self.end_date_entry = DateEntry(frame_but,font=field_font, background="darkblue",state="readonly", date_pattern="dd-mm-yyyy",
                                        foreground="white", borderwidth=2)
        self.end_date_entry.grid(row=3, column=3, padx=5, pady=2, sticky="w")


        party_name_label = tk.Label(frame_but,font=label_font, text="Party Name : ", bg="#ADD8E0")
        party_name_label.grid(row=3, column=4, sticky="w")

        self.party_name_var = tk.StringVar()
        self.party_name_entry = ttk.Entry(frame_but,font=field_font, textvariable=self.party_name_var,width=50)
        self.party_name_entry.grid(row=3, column=5, padx=5, pady=2, sticky="w",columnspan=3)

        material_label = tk.Label(frame_but,font=label_font, text="Job Name: ", bg="#ADD8E0")
        material_label.grid(row=2, column=4, sticky="w")

        self.material_var = tk.StringVar()
        self.material_entry = ttk.Entry(frame_but,font=field_font, textvariable=self.material_var,width=50)
        self.material_entry.grid(row=2, column=5, padx=5, pady=2, sticky="w",columnspan=3)


        F_label = tk.Label(frame_but,font=label_font, text="Status :", bg="#ADD8E0")
        F_label.grid(row=2, column=8,pady=10,padx=10,sticky="e")

        self.combobox_var = tk.StringVar()
        self.combobox = ttk.Combobox(frame_but, textvariable=self.combobox_var,font=field_font,width=8, values=["Done", "All","Pending"], state="readonly")
        self.combobox.grid(row=2, column=9,sticky="w", padx=10, pady=10)


        
        today_date=datetime.datetime.today().strftime("%Y-%m-%d")
        one_month=(datetime.datetime.today() - relativedelta(months=1)).strftime("%Y-%m-%d")
        sql_data=db.GetFromDate(one_month,today_date)
        
        self.df = pd.DataFrame(sql_data)
        self.df.insert(0,"Mark","") 

        self.filtered_data = self.df.copy()
     


        
    



        treeview_width = int((self.winfo_screenwidth())/1.55)
   
        self.treeview = ttk.Treeview(frame_top, columns=("Mark","ID","Lot No","Roll No",
             "PartyName", "Job Name","GrossWeight", "TareWeight","CoreWeight" ,"NetWeight","Date","Status"
        ),height=22,selectmode="extended")


        self.treeview.column("#0", minwidth=0, width=0, stretch=False, anchor="center")
        self.treeview.column("Mark", minwidth=int(treeview_width * 0.05), width=int(treeview_width * 0.05), stretch=False, anchor="center")
        self.treeview.column("ID", minwidth=int(treeview_width * 0.1), width=int(treeview_width * 0.1), stretch=False, anchor="center")
        self.treeview.column("Lot No", minwidth=int(treeview_width * 0.1), width=int(treeview_width * 0.1), stretch=False, anchor="center")
        self.treeview.column("Roll No", minwidth=int(treeview_width * 0.1), width=int(treeview_width * 0.1), stretch=False, anchor="center")
        self.treeview.column("PartyName", minwidth=int(treeview_width * 0.3), width=int(treeview_width * 0.3), stretch=False, anchor="center")
        self.treeview.column("Job Name", minwidth=int(treeview_width * 0.3), width=int(treeview_width * 0.3), stretch=False, anchor="center")
        self.treeview.column("GrossWeight", minwidth=int(treeview_width * 0.1), width=int(treeview_width * 0.1), stretch=False, anchor="center")
        self.treeview.column("TareWeight", minwidth=int(treeview_width * 0.1), width=int(treeview_width * 0.1), stretch=False, anchor="center")
        self.treeview.column("CoreWeight", minwidth=int(treeview_width * 0.1), width=int(treeview_width * 0.1), stretch=False, anchor="center")
        self.treeview.column("NetWeight", minwidth=int(treeview_width * 0.1), width=int(treeview_width * 0.1), stretch=False, anchor="center")
        self.treeview.column("Date", minwidth=int(treeview_width * 0.1), width=int(treeview_width * 0.1), stretch=False, anchor="center")
        self.treeview.column("Status", minwidth=int(treeview_width * 0.1), width=int(treeview_width * 0.1), stretch=False, anchor="center")
        # Add headings
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Mark", text="Mark")
        self.treeview.heading("Lot No", text="Lot No")
        self.treeview.heading("Roll No", text="Roll No")
        self.treeview.heading("PartyName", text="PartyName")
        self.treeview.heading("Job Name", text="Job Name")
        self.treeview.heading("GrossWeight", text="GrossWeight")
        self.treeview.heading("TareWeight", text="TareWeight")
        self.treeview.heading("CoreWeight", text="CoreWeight")
        self.treeview.heading("NetWeight", text="NetWeight")
        self.treeview.heading("Date", text="Date")
        self.treeview.heading("Status", text="Status")


        self.treeview.bind("<KeyPress-1>", self.toggle_value)
        self.treeview.bind("<KeyPress-0>", self.toggle_value)
        self.treeview.bind("<Double-1>", self.toggle_value)

        self.visible_rows = 22
        self.total_rows = db.GetAllCount()[0]
        
   
        self.loaded_start = 0
        self.loaded_end = self.visible_rows
        
      

        # Set the focus on the first cell of the second column
        self.treeview.focus_set()


        # self.vsb = ttk.Scrollbar(frame_top, orient="vertical", command=self.treeview.yview)
        self.treeview.bind("<MouseWheel>", self.on_scrollTable)
        # self.vsb.pack(side="right", fill="y")
        # self.vsb.set(0,25/self.total_rows)
        
        
        self.scale=tk.Scale(frame_top,from_=0,to=self.total_rows-22,orient="vertical",showvalue=False,command=self.on_scroll)
        self.scale.pack(side="right",fill="y")
        # Create the horizontal scrollbar
        scrollbar_x = ttk.Scrollbar(frame_top, orient="horizontal", command=self.treeview.xview)
        scrollbar_x.pack(side="bottom",fill="x")
        self.treeview.configure(xscrollcommand=scrollbar_x.set)



        self.treeview.pack(side="left", fill="both", expand=True, padx=5, pady=1)


  

        label_frame=tk.LabelFrame(botom_frame,bg="#ADD8E0")
        label_frame.pack(side="left")

        self.label1=tk.StringVar()
        self.label2=tk.StringVar()
        self.label3=tk.StringVar()
        self.label_1=tk.Label(label_frame,textvariable=self.label1,font=fieldx_font,bg="#ADD8E0")
        self.label_1.grid(row=0,column=0,sticky="w")
        self.label_2=tk.Label(label_frame,textvariable=self.label2,font=fieldx_font,bg="#ADD8E0")
        self.label_2.grid(row=0,column=1,sticky="w")
        self.label_3=tk.Label(label_frame,textvariable=self.label3,font=fieldx_font,bg="#ADD8E0")
        self.label_3.grid(row=0,column=2,sticky="w")

        self.label4=tk.StringVar()
        self.label_4=tk.Label(label_frame,textvariable=self.label4,font=fieldx_font,bg="#ADD8E0")
        self.label_4.grid(row=0,column=3,sticky="w")
        self.label5=tk.StringVar()  
        self.label_5=tk.Label(label_frame,textvariable=self.label5,font=fieldx_font,bg="#ADD8E0")
        self.label_5.grid(row=0,column=4,sticky="w")


        self.label1.set(f"Selected Rolls |\n{0}")
        self.label2.set(f"Selected Gross Weight |\n{0} KG")
        self.label3.set(f"Selected Tare Weight |\n{0} KG")
        self.label4.set(f"Selected Core Weight |\n{0} KG")
        self.label5.set(f"Selected Net Weight  \n{0} KG")



        self.party_name_var.trace('w', lambda *args: self.auto_capitalize(self.party_name_var))
        self.material_var.trace('w', lambda *args: self.auto_capitalize(self.material_var))

    
        # -------------------------button---------------------------

        button_frame=tk.Frame(botom_frame,bg="#ADD8E0")
        button_frame.pack(side="right")



        image2 = Image.open("res/clear.jpg")
        button_image2 = ImageTk.PhotoImage(image2)


        image3 = Image.open("res/print.jpg")
        button_image3 = ImageTk.PhotoImage(image3)

        image4 = Image.open("res/exit.jpg")
        button_image4 = ImageTk.PhotoImage(image4)

        image5 = Image.open("res/printxl.jpg")
        button_image5 = ImageTk.PhotoImage(image5)

        



        self.button2 = tk.Button(button_frame,relief="groove", image=button_image2, compound="left",command=lambda:self.clr())
        self.button2.image = button_image2  # Store the image reference
        self.button2.bind("<Return>", lambda e: self.clr())
        self.button2.grid(row=0,column=3,rowspan=3,padx=10, pady=10)


        self.button4 = tk.Button(button_frame,relief="groove", image=button_image4, compound="left",command=lambda:self.close())
        self.button4.image = button_image4  # Store the image reference
        self.button4.bind("<Return>", lambda e: self.close())
        self.button4.grid(row=0,column=4,rowspan=3, padx=10, pady=10)


        self.button3 = tk.Button(button_frame,relief="groove", image=button_image3, compound="left",command=lambda:self.printing("pdf"))
        self.button3.image = button_image3  # Store the image reference
        self.button3.bind("<Return>", lambda e: self.printing("pdf"))
        self.button3.grid(row=0,column=5,rowspan=3, padx=10, pady=10)




        self.button5 = tk.Button(button_frame,relief="groove", image=button_image5, compound="left",command=lambda:self.printing("xl"))
        self.button5.image = button_image5  # Store the image reference
        self.button5.bind("<Return>", lambda e: self.printing("xl"))
        self.button5.grid(row=0,column=6,rowspan=3, padx=10, pady=10)

        self.button3.grid_remove()  # Hide the button initially
        self.button5.grid_remove()  # Hide the button initially
        


        # self.delete_button = tk.Button(button_frame, text="Delete", command=lambda:self.delete_selected_record())
        # self.delete_button.grid(row=0,column=1,rowspan=3, padx=10, pady=10)
        # self.delete_button.grid_remove()  # Hide the button initially



        self.bind("<Alt_L>"+"<E>",lambda e:self.toggle_buttons_visibility())
        self.bind("<Alt_L>"+"<e>",lambda e:self.toggle_buttons_visibility())


        

        
        

        self.clr()
        
        self.refresh_data(self.df)
        
      
        self.loading_data = False
       

        self.start_ticket_var.trace_add("write", lambda *args: self.view_report())
        self.end_ticket_var.trace_add("write", lambda *args: self.view_report())
        self.start_date_entry.bind("<<DateEntrySelected>>", lambda event: self.view_report())
        self.end_date_entry.bind("<<DateEntrySelected>>", lambda event: self.view_report())
        self.party_name_var.trace_add("write", lambda *args: self.view_report())
        self.material_var.trace_add("write", lambda *args: self.view_report())
        self.combobox_var.trace_add("write", lambda *args: self.view_report())
        






        


    def toggle_buttons_visibility(self):
        if self.button3.winfo_viewable():    
            self.button3.grid_remove()
        else:     
            self.button3.grid()

        if self.button5.winfo_viewable():    
            self.button5.grid_remove()
        else:     
            self.button5.grid()

  

    def delete_selected_record(self):
        selected_item = self.treeview.focus() 
        values = self.treeview.item(selected_item, "values")
        MsgBox = tk.messagebox.askquestion ('Are You Sure','Do you want to delete '+"roll no.:"+str(values[0])+"\nrecord:"+str(values),icon = 'question')
        if MsgBox == 'yes':
            db.delone(values[0])
            MsgBox = tk.messagebox.showinfo("Done","roll no.:"+str(values[0])+"data deleted")
            self.df.drop(self.df[self.df[0] == int(values[0])].index, inplace=True)
            self.refresh_data(self.df)
            
        else:
            pass
        



    def validate_positive_int(self, value):
        if value.isdigit() or value == "":
            return True
        return False

    def auto_capitalize(self, variable):
        value = variable.get()
        variable.set(value.upper())

    def toggle_value(self, event):
        selected_items = self.treeview.selection()
        for selected_item in selected_items:
            values = self.treeview.item(selected_item, 'values')
            f_value = values[0]
            if event.char=="??":
                if f_value=="":
                    event.char="1"
                else:
                    event.char="0"
            index = int(self.treeview.item(selected_item, 'text'))  # Get the index from the Treeview's text property
            if event.char == "1" and f_value == "":
                value = "✔"
                self.df.at[index, 'Mark'] = "✔"  # Update DataFrame
                self.filtered_data.at[index, 'Mark'] = "✔"  # Update DataFrame
                self.cc += 1
            elif event.char == "0" and f_value == "✔":
                value = ""
                self.df.at[index, 'Mark'] = ""  # Update DataFrame
                self.filtered_data.at[index, 'Mark'] = ""  # Update DataFrame
                self.cc -= 1
            else:
                continue
            self.treeview.set(selected_item, 'Mark', value)

        self.count.set(str(self.cc) + " data marked")
        self.calculate_weights()
    
    def calculate_weights(self):
        
        selected_rows = self.df[self.df["Mark"] == "✔"]

        sum_grossweight = pd.to_numeric(selected_rows[5], errors='coerce').sum()
        sum_tareweight = pd.to_numeric(selected_rows[6], errors='coerce').sum()
        sum_coreweight = pd.to_numeric(selected_rows[7], errors='coerce').sum()
        sum_netweight = pd.to_numeric(selected_rows[8], errors='coerce').sum()

        self.label1.set(f"Selected Rolls |\n{self.cc}")
        self.label2.set(f"Selected Gross Weight |\n{round(sum_grossweight, 3)} KG")
        self.label3.set(f"Selected Tare Weight |\n{round(sum_tareweight, 3)} KG")
        self.label4.set(f"Selected Core Weight |\n{round(sum_coreweight, 3)} KG")
        self.label5.set(f"Selected Net Weight  \n{round(sum_netweight, 3)} KG")



    def refresh_data(self,data):
        self.total_rows=len(data)
        self.scale.configure(to=self.total_rows-22)
        self.treeview.delete(*self.treeview.get_children())
        self.treeview.tag_configure('Pending', background='#FFAAAA')
        self.treeview.tag_configure('Done', background='white')
        data = data.iloc[self.loaded_start:self.loaded_end]
        

     
        for index, row in data.iterrows():
            values = [str(value) for value in row]

            self.treeview.insert("", index, text=index, values=values, tags=(row[10]))

    def on_scroll(self, *args):
        new=self.scale.get()
        
     
        new_end = min(self.total_rows, new+22)
        self.loaded_start = new
        self.loaded_end = new_end
        self.refresh_data(self.filtered_data)
            

    def on_scrollTable(self, *args):
        if (args[0].delta)>0:
            self.scale.set(self.scale.get()-5)
            self.on_scroll()
        else :
            self.scale.set(self.scale.get()+5)
            self.on_scroll()


    def close(self):
        
        self.destroy()


    def clr(self):
        # Clear all entry box values
        self.start_ticket_var.set('')
        self.end_ticket_var.set('')
        today_date=datetime.datetime.today().strftime("%d-%m-%Y")
        one_month=(datetime.datetime.today() - relativedelta(months=1)).strftime("%d-%m-%Y")
        
        self.start_date_entry.set_date(one_month)

     
        self.end_date_entry.set_date(today_date)



    


        self.party_name_var.set('')
        self.material_var.set('')

        # self.delete_button.grid_remove()
        # Set the combobox value to "ALL"
        self.combobox_var.set('All')

        # Call the view_report function to update the treeview based on the cleared values
        self.treeview.delete(*self.treeview.get_children())


    def view_report(self):
        # Get the values from the entry boxes and combo box
        start_ticket = self.start_ticket_var.get()
        end_ticket = self.end_ticket_var.get()
        start_date_str = self.start_date_entry.get()
        end_date_str = self.end_date_entry.get()

        party_name = self.party_name_var.get()
        material = self.material_var.get()
        ticket_type = self.combobox_var.get()

        # Check if the start date is less than the current date
        current_date = datetime.datetime.now().date()
        start_date = datetime.datetime.strptime(start_date_str, "%d-%m-%Y").date()
        start_date_str = datetime.datetime.strptime(start_date_str, "%d-%m-%Y").date() if start_date_str else None
        end_date_str = datetime.datetime.strptime(end_date_str, "%d-%m-%Y").date() if end_date_str else None


        self.filtered_data = self.df.copy()


        if start_date <= current_date:
            # Start date is before the current date, proceed with filtering
            

            def populate_column(row):
                if row[10]:
                    return row[10]
                elif row[8]:
                    return row[8]
                else:
                    return row[10]

            # Apply the custom function to create the fourth column
            self.filtered_data[10] = self.filtered_data.apply(populate_column, axis=1)
            





            if ticket_type == "Done":
                self.filtered_data = self.filtered_data[self.filtered_data[10] == "Done"]
            elif ticket_type == "Pending":
                self.filtered_data = self.filtered_data[self.filtered_data[10] != "Done"]

            if start_ticket:
                self.filtered_data = self.filtered_data[self.filtered_data[2].astype("Int64") >= int(start_ticket)]

            if end_ticket:
                self.filtered_data = self.filtered_data[self.filtered_data[2].astype("Int64") <= int(end_ticket)]


            self.filtered_data[9] = pd.to_datetime(self.filtered_data[9], errors="coerce",yearfirst=True).dt.date



            if start_date_str:
                self.filtered_data = self.filtered_data[(self.filtered_data[9] >= start_date_str)]


            if end_date_str:
                self.filtered_data = self.filtered_data[(self.filtered_data[9] <= end_date_str)]


            if party_name:
                self.filtered_data = self.filtered_data[self.filtered_data[3].str.contains(party_name, case=False, na=False)]

            if material:
                self.filtered_data = self.filtered_data[self.filtered_data[4].str.contains(material, case=False, na=False)]


            self.refresh_data(self.filtered_data)
        else:
            self.clr()
            tk.messagebox.showerror("ERROR","Start Date Must Be Less Than End Date")
            self.refresh_data(self.df)

    def mall(self):
        for item in self.treeview.get_children():
            index = int(self.treeview.item(item, 'text'))
            self.treeview.item(item, values=["✔" if i == 0 else val for i, val in enumerate(self.treeview.item(item)["values"])])
            # self.df.at[index, 'Mark'] = "✔"
        self.filtered_data['Mark'] = "✔"
        self.df.loc[self.df[0].isin(self.filtered_data[0]), 'Mark'] = "✔"
        

        self.cc =  self.df['Mark'].value_counts().get('✔', 0)
        self.count.set(str(self.cc) + " data marked")
        self.calculate_weights()
        

    def umall(self):
        for item in self.treeview.get_children():
            index = int(self.treeview.item(item, 'text'))
            self.treeview.item(item, values=["" if i == 0 else val for i, val in enumerate(self.treeview.item(item)["values"])])
        
        self.df['Mark'] = ""
        self.filtered_data['Mark'] = ""
        self.cc = 0
        self.count.set(str(self.cc) + " data marked")
        self.calculate_weights()


    def printing(self,format):

        
        selected_rows = self.df[self.df["Mark"] == "✔"]
        ids=selected_rows[0].tolist()
        db.update_status(ids)
        
        


        toprint=selected_rows.copy()
        
        if format=="xl":
            exel.create_report(toprint.values.tolist())
            self.print_exel()
        elif format=="pdf":
            report2.create_report(toprint.values.tolist())
            self.print_pdf()
        else:
            pass



        

    def print_exel(self):
        filename = "packing_list.xlsx"
        # Open the PDF file using the default PDF viewer
        subprocess.run(["start", filename], shell=True)


    def print_pdf(self):
        filename = "packing_list.pdf"
        subprocess.run(["start",filename], shell=True)


    



class StkSetPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        frame2 = tk.Frame(self, bg='white')

        icon = Font(family="Web Symbols", size=12)

        Label1_font = Font(family="Arquitecta", size=11)

        field_font = Font(family="Arquitecta", size=10)

        self.controller = controller

        self.field1 = tk.StringVar()
        self.field2 = tk.StringVar()
        self.field3 = tk.StringVar()
        self.field4 = tk.StringVar()
        self.field5 = tk.StringVar()
        self.field6 = tk.StringVar()
        self.field7 = tk.StringVar()
        self.field8 = tk.StringVar()
        self.field9 = tk.StringVar()
        self.field10 = tk.StringVar()
        self.fontsize1 = tk.StringVar()
        self.fontsize2 = tk.StringVar()
        self.fontsize3 = tk.StringVar()
        self.fontsize4 = tk.StringVar()
        self.fontsize5 = tk.StringVar()
        self.fontsize6 = tk.StringVar()
        self.fontsize7 = tk.StringVar()
        self.fontsize8 = tk.StringVar()
        self.fontsize9 = tk.StringVar()
        self.fontsize10 = tk.StringVar()
        self.x1 = tk.StringVar()
        self.y1 = tk.StringVar()
        self.x2 = tk.StringVar()
        self.y2 = tk.StringVar()
        self.x3 = tk.StringVar()
        self.y3 = tk.StringVar()
        self.x4 = tk.StringVar()
        self.y4 = tk.StringVar()
        self.x5 = tk.StringVar()
        self.y5 = tk.StringVar()
        self.x6 = tk.StringVar()
        self.y6 = tk.StringVar()
        self.x7 = tk.StringVar()
        self.y7 = tk.StringVar()
        self.x8 = tk.StringVar()
        self.y8 = tk.StringVar()
        self.x9 = tk.StringVar()
        self.y9 = tk.StringVar()
        self.x10 = tk.StringVar()
        self.y10 = tk.StringVar()
        self.bar = tk.StringVar()
        self.barsize = tk.StringVar()
        self.barsw = tk.StringVar()
        self.barx = tk.StringVar()
        self.bary = tk.StringVar()

        # field2

        self.field_1_label = tk.Label(frame2, text='f1', fg="black", bg='white', font=Label1_font).grid(row=4, column=0,
                                                                                                        padx=3, pady=1)
        self.feild_1_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field1, highlightthickness=2,
                                      highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.feild_1_value.grid(row=4, column=1, padx=3, pady=1, columnspan=2)

        self.fontsize1cb = ttk.Combobox(frame2, textvariable=self.fontsize1, font=Label1_font, width=3,
                                        state="readonly")
        self.fontsize1cb["values"] = self.lint()
        self.fontsize1cb.current(50)
        self.fontsize1cb.grid(row=4, column=3, padx=3)

        self.x_1_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.x1, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.x_1_value.grid(row=4, column=4, padx=3, pady=1)

        self.y_1_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.y1, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.y_1_value.grid(row=4, column=5, padx=3, pady=1)

        # field3
        self.field_2_label = tk.Label(frame2, text='f2', fg="black", bg='white', font=Label1_font).grid(row=5, column=0,
                                                                                                        padx=3, pady=1)
        self.feild_2_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field2, highlightthickness=2,
                                      highlightcolor='yellow', font=field_font, justify='center',
                                      exportselection=0).grid(row=5, column=1, padx=3, pady=1, columnspan=2)
        self.fontsize2cb = ttk.Combobox(frame2, textvariable=self.fontsize2, font=Label1_font, width=3,
                                        state="readonly")
        self.fontsize2cb["values"] = self.lint()
        self.fontsize2cb.current(50)
        self.fontsize2cb.grid(row=5, column=3, padx=3)

        self.x_2_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.x2, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.x_2_value.grid(row=5, column=4, padx=3, pady=1)

        self.y_2_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.y2, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.y_2_value.grid(row=5, column=5, padx=3, pady=1)

        # field4
        self.field_3_label = tk.Label(frame2, text='f3', fg="black", bg='white', font=Label1_font).grid(row=6, column=0,
                                                                                                        padx=3, pady=1)
        self.feild_3_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field3, highlightthickness=2,
                                      highlightcolor='yellow', font=field_font, justify='center',
                                      exportselection=0).grid(row=6, column=1, padx=3, pady=1, columnspan=2)
        self.fontsize3cb = ttk.Combobox(frame2, textvariable=self.fontsize3, font=Label1_font, width=3,
                                        state="readonly")
        self.fontsize3cb["values"] = self.lint()
        self.fontsize3cb.current(50)
        self.fontsize3cb.grid(row=6, column=3, padx=3)

        self.x_3_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.x3, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.x_3_value.grid(row=6, column=4, padx=3, pady=1)

        self.y_3_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.y3, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.y_3_value.grid(row=6, column=5, padx=3, pady=1)

        self.field_4_label = tk.Label(frame2, text='f4', fg="black", bg='white', font=Label1_font).grid(row=7, column=0,
                                                                                                        padx=3, pady=1)
        self.feild_4_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field4, highlightthickness=2,
                                      highlightcolor='yellow', font=field_font, justify='center',
                                      exportselection=0).grid(row=7, column=1, padx=3, pady=1, columnspan=2)
        self.fontsize4cb = ttk.Combobox(frame2, textvariable=self.fontsize4, font=Label1_font, width=3,
                                        state="readonly")
        self.fontsize4cb["values"] = self.lint()
        self.fontsize4cb.current(50)
        self.fontsize4cb.grid(row=7, column=3, padx=3)

        self.x_4_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.x4, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.x_4_value.grid(row=7, column=4, padx=3, pady=1)

        self.y_4_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.y4, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.y_4_value.grid(row=7, column=5, padx=3, pady=1)

        self.field_5_label = tk.Label(frame2, text='f5', fg="black", bg='white', font=Label1_font).grid(row=8, column=0,
                                                                                                        padx=3, pady=1)
        self.feild_5_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field5, highlightthickness=2,
                                      highlightcolor='yellow', font=field_font, justify='center',
                                      exportselection=0).grid(row=8, column=1, padx=3, pady=1, columnspan=2)
        self.fontsize5cb = ttk.Combobox(frame2, textvariable=self.fontsize5, font=Label1_font, width=3,
                                        state="readonly")
        self.fontsize5cb["values"] = self.lint()
        self.fontsize5cb.current(50)
        self.fontsize5cb.grid(row=8, column=3, padx=3)

        self.x_5_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.x5, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.x_5_value.grid(row=8, column=4, padx=3, pady=1)

        self.y_5_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.y5, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.y_5_value.grid(row=8, column=5, padx=3, pady=1)
        # ----------------------------------------------------------------------
        self.field_6_label = tk.Label(frame2, text='f6', fg="black", bg='white', font=Label1_font).grid(row=9, column=0,
                                                                                                        padx=3, pady=1)
        self.feild_6_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field6, highlightthickness=2,
                                      highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.feild_6_value.grid(row=9, column=1, padx=3, pady=1, columnspan=2)

        self.fontsize6cb = ttk.Combobox(frame2, textvariable=self.fontsize6, font=Label1_font, width=3,
                                        state="readonly")
        self.fontsize6cb["values"] = self.lint()
        self.fontsize6cb.current(50)
        self.fontsize6cb.grid(row=9, column=3, padx=3)

        self.x_6_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.x6, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.x_6_value.grid(row=9, column=4, padx=3, pady=1)

        self.y_6_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.y6, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.y_6_value.grid(row=9, column=5, padx=3, pady=1)

        # field3
        self.field_7_label = tk.Label(frame2, text='f7', fg="black", bg='white', font=Label1_font).grid(row=10,
                                                                                                        column=0,
                                                                                                        padx=3, pady=1)
        self.feild_7_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field7, highlightthickness=2,
                                      highlightcolor='yellow', font=field_font, justify='center',
                                      exportselection=0).grid(row=10, column=1, padx=3, pady=1, columnspan=2)
        self.fontsize7cb = ttk.Combobox(frame2, textvariable=self.fontsize7, font=Label1_font, width=3,
                                        state="readonly")
        self.fontsize7cb["values"] = self.lint()
        self.fontsize7cb.current(50)
        self.fontsize7cb.grid(row=10, column=3, padx=3)

        self.x_7_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.x7, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.x_7_value.grid(row=10, column=4, padx=3, pady=1)

        self.y_7_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.y7, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.y_7_value.grid(row=10, column=5, padx=3, pady=1)

        # field4
        self.field_8_label = tk.Label(frame2, text='f8', fg="black", bg='white', font=Label1_font).grid(row=11,
                                                                                                        column=0,
                                                                                                        padx=3, pady=1)
        self.feild_8_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field8, highlightthickness=2,
                                      highlightcolor='yellow', font=field_font, justify='center',
                                      exportselection=0).grid(row=11, column=1, padx=3, pady=1, columnspan=2)
        self.fontsize8cb = ttk.Combobox(frame2, textvariable=self.fontsize8, font=Label1_font, width=3,
                                        state="readonly")
        self.fontsize8cb["values"] = self.lint()
        self.fontsize8cb.current(50)
        self.fontsize8cb.grid(row=11, column=3, padx=3)

        self.x_8_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.x8, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.x_8_value.grid(row=11, column=4, padx=3, pady=1)

        self.y_8_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.y8, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.y_8_value.grid(row=11, column=5, padx=3, pady=1)

        self.field_9_label = tk.Label(frame2, text='f9', fg="black", bg='white', font=Label1_font).grid(row=12,
                                                                                                        column=0,
                                                                                                        padx=3, pady=1)
        self.feild_9_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field9, highlightthickness=2,
                                      highlightcolor='yellow', font=field_font, justify='center',
                                      exportselection=0).grid(row=12, column=1, padx=3, pady=1, columnspan=2)
        self.fontsize9cb = ttk.Combobox(frame2, textvariable=self.fontsize9, font=Label1_font, width=3,
                                        state="readonly")
        self.fontsize9cb["values"] = self.lint()
        self.fontsize9cb.current(50)
        self.fontsize9cb.grid(row=12, column=3, padx=3)

        self.x_9_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.x9, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.x_9_value.grid(row=12, column=4, padx=3, pady=1)

        self.y_9_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.y9, width=3, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.y_9_value.grid(row=12, column=5, padx=3, pady=1)

        self.field_10_label = tk.Label(frame2, text='f10', fg="black", bg='white', font=Label1_font).grid(row=13,
                                                                                                          column=0,
                                                                                                          padx=3,
                                                                                                          pady=1)
        self.feild_10_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field10, highlightthickness=2,
                                       highlightcolor='yellow', font=field_font, justify='center',
                                       exportselection=0).grid(row=13, column=1, padx=3, pady=1, columnspan=2)
        self.fontsize10cb = ttk.Combobox(frame2, textvariable=self.fontsize10, font=Label1_font, width=3,
                                         state="readonly")
        self.fontsize10cb["values"] = self.lint()
        self.fontsize10cb.current(50)
        self.fontsize10cb.grid(row=13, column=3, padx=3)

        self.x_10_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.x10, width=3, highlightthickness=2,
                                   highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.x_10_value.grid(row=13, column=4, padx=3, pady=1)

        self.y_10_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.y10, width=3, highlightthickness=2,
                                   highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.y_10_value.grid(row=13, column=5, padx=3, pady=1)

        self.bar_label = tk.Label(frame2, text='bc', fg="black", bg='white', font=Label1_font).grid(row=14, column=0,
                                                                                                    padx=3, pady=1)
        self.bar_value = tk.Entry(frame2, fg="black", bg='white', width=14, textvariable=self.bar, highlightthickness=2,
                                  highlightcolor='yellow', font=field_font, justify='center', exportselection=0).grid(
            row=14, column=1, padx=3, pady=1)
        self.barsizecb = ttk.Combobox(frame2, textvariable=self.barsize, font=Label1_font, width=3, state="readonly")
        self.barsizecb["values"] = [1,2,3,4,5,6,7,8,9,10]
        self.barsizecb.current(5)
        self.barsizecb.grid(row=14, column=2, padx=3)

        self.barswcb = ttk.Combobox(frame2, textvariable=self.barsw, font=Label1_font, width=3, state="readonly")
        self.barswcb["values"] = ("N", "Y")
        self.barswcb.current(0)
        self.barswcb.grid(row=14, column=3, padx=3)

        self.barx_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.barx, width=3,
                                   highlightthickness=2, highlightcolor='yellow', font=field_font, justify='center',
                                   exportselection=0)
        self.barx_value.grid(row=14, column=4, padx=3, pady=1)

        self.bary_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.bary, width=3,
                                   highlightthickness=2, highlightcolor='yellow', font=field_font, justify='center',
                                   exportselection=0)
        self.bary_value.grid(row=14, column=5, padx=3, pady=1)

        self.savebut = tk.Button(frame2, text='Save', width=3, bg='lightgrey', activebackground='lightgrey',
                                 activeforeground='black', command=lambda: self.asktosave())

        self.savebut.bind("<Return>", lambda e: self.asktosave())
        self.savebut.grid(row=15, column=3, pady=1)

        self.closebut = tk.Button(frame2, text='Close', width=3, bg='lightgrey', activebackground='lightgrey',
                                  activeforeground='black', command=lambda: self.close())
        self.closebut.bind("<Return>", lambda e: self.close())
        self.closebut.grid(row=15, column=4, pady=1)

        frame2.pack(fill='both', expand=True)

    def asktosave(self):
        MsgBox = tk.messagebox.askquestion('Ask To Save', 'Do you want to save?', icon='question')
        if MsgBox == 'yes':
            self.save()
        else:
            pass

    def save(self):

        db.UpdatefixData(str(self.field1.get()), int(self.fontsize1.get()), int(self.x1.get()), int(self.y1.get()),
                         str(self.field2.get()), int(self.fontsize2.get()), int(self.x2.get()), int(self.y2.get()),
                         str(self.field3.get()), int(self.fontsize3.get()), int(self.x3.get()), int(self.y3.get()),
                         str(self.field4.get()), int(self.fontsize4.get()), int(self.x4.get()), int(self.y4.get()),
                         str(self.field5.get()), int(self.fontsize5.get()), int(self.x5.get()), int(self.y5.get()),
                         str(self.field6.get()), int(self.fontsize6.get()), int(self.x6.get()), int(self.y6.get()),
                         str(self.field7.get()), int(self.fontsize7.get()), int(self.x7.get()), int(self.y7.get()),
                         str(self.field8.get()), int(self.fontsize8.get()), int(self.x8.get()), int(self.y8.get()),
                         str(self.field9.get()), int(self.fontsize9.get()), int(self.x9.get()), int(self.y9.get()),
                         str(self.field10.get()), int(self.fontsize10.get()), int(self.x10.get()), int(self.y10.get()),
                         str(self.bar.get()), int(self.barsize.get()), str(self.barsw.get()), int(self.barx.get()),
                         int(self.bary.get()))

    def close(self):
        self.clear()
        self.controller.show_frame(StartPage)
        self.controller.focus_set()

    def clear(self):
        fixrow = []
        fixrow = db.getfix()

        self.field1.set(fixrow[1])
        self.fontsize1cb.current(int(fixrow[2]) - 10)
        self.x1.set(int(fixrow[3]))
        self.y1.set(int(fixrow[4]))
        self.field2.set(fixrow[5])
        self.fontsize2cb.current(int(fixrow[6]) - 10)
        self.x2.set(int(fixrow[7]))
        self.y2.set(int(fixrow[8]))
        self.field3.set(fixrow[9])
        self.fontsize3cb.current(int(fixrow[10]) - 10)
        self.x3.set(int(fixrow[11]))
        self.y3.set(int(fixrow[12]))
        self.field4.set(fixrow[13])
        self.fontsize4cb.current(int(fixrow[14]) - 10)
        self.x4.set(int(fixrow[15]))
        self.y4.set(int(fixrow[16]))
        self.field5.set(fixrow[17])
        self.fontsize5cb.current(int(fixrow[18]) - 10)
        self.x5.set(int(fixrow[19]))
        self.y5.set(int(fixrow[20]))
        self.field6.set(fixrow[21])
        self.fontsize6cb.current(int(fixrow[22]) - 10)
        self.x6.set(int(fixrow[23]))
        self.y6.set(int(fixrow[24]))
        self.field7.set(fixrow[25])
        self.fontsize7cb.current(int(fixrow[26]) - 10)
        self.x7.set(int(fixrow[27]))
        self.y7.set(int(fixrow[28]))
        self.field8.set(fixrow[29])
        self.fontsize8cb.current(int(fixrow[30]) - 10)
        self.x8.set(int(fixrow[31]))
        self.y8.set(int(fixrow[32]))
        self.field9.set(fixrow[33])
        self.fontsize9cb.current(int(fixrow[34]) - 10)
        self.x9.set(int(fixrow[35]))
        self.y9.set(int(fixrow[36]))
        self.field10.set(fixrow[37])
        self.fontsize10cb.current(int(fixrow[38]) - 10)
        self.x10.set(int(fixrow[39]))
        self.y10.set(int(fixrow[40]))

        self.bar.set(fixrow[41])
        self.barsizecb.current(int(fixrow[42]) - 1)
        if fixrow[43] == "N":
            tig = 0
        else:
            tig = 1

        self.barswcb.current(tig)
        self.barx.set(int(fixrow[44]))
        self.bary.set(int(fixrow[45]))

    def lint(self):
        res = list(range(10, 200, 1))
        return res


class ComPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        frame2 = tk.Frame(self, bg='white')

        self.field0 = tk.StringVar()
        self.field1 = tk.StringVar()
        self.field2 = tk.StringVar()
        self.field3 = tk.StringVar()
        self.field4 = tk.StringVar()
        self.controller = controller
        self.errmsg = tk.StringVar()

        err_font = Font(family="Arquitecta", size=10)
        Label1_font = Font(family="Arquitecta", size=14)
        field_font = Font(family="Arquitecta", size=12)

        self.errorlabel = tk.Label(frame2, width=25, height=1, textvariable=self.errmsg, fg="red", bg='white',
                                   font=err_font)
        self.errorlabel.grid(row=11, column=0, padx=1, pady=1, columnspan=3)

        self.field_0_label = tk.Label(frame2, text="COM PORT:", fg="black", bg='white', font=Label1_font,
                                      height=1).grid(row=2, column=0, padx=0, pady=0, sticky='w')

        self.feild_0_value= tk.Spinbox(frame2,readonlybackground='white',highlightthickness=2,highlightcolor='yellow',textvariable=self.field0,font=field_font,state='readonly',exportselection=0)
        self.feild_0_value["values"]=('COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9','COM10')
        self.feild_0_value.bind("<Return>", lambda e: self.feild_1_value.focus_set())
        self.feild_0_value.grid(row=2,column=1, padx=5,pady=2,columnspan=3,sticky='w')


        self.field_1_label = tk.Label(frame2, text="BAURD RATE:", fg="black", bg='white', font=Label1_font, height=1).grid(
            row=4, column=0, padx=0, pady=0, sticky='w')
        self.feild_1_value= tk.Spinbox(frame2,readonlybackground='white',highlightthickness=2,highlightcolor='yellow',textvariable=self.field1,font=field_font,state='readonly',exportselection=0)
        self.feild_1_value["values"]=('600','1200','2400','4800','9600','19200','38400','76800','153600')
        self.feild_1_value.bind("<Return>", lambda e: self.feild_2_value.focus_set())
        self.feild_1_value.grid(row=4, column=1, padx=1, pady=0, columnspan=2)


        # field3
        self.field_2_label = tk.Label(frame2, text="R-find", fg="black", bg='white', font=Label1_font).grid(row=6,
                                                                                                             column=0,
                                                                                                             padx=0,
                                                                                                             pady=0,
                                                                                                             sticky='w')
        self.feild_2_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field2, highlightthickness=2,
                                      highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.feild_2_value.bind("<Return>", lambda e: self.feild_3_value.focus_set())
        self.feild_2_value.grid(row=6, column=1, padx=1, pady=0, columnspan=2)



        self.field_3_label = tk.Label(frame2, text="DP",fg="black",bg='white',font=Label1_font).grid(row=8,column=0, padx=0,pady=0,sticky='w')
        self.feild_3_value= tk.Spinbox(frame2,readonlybackground='white',highlightthickness=2,highlightcolor='yellow',textvariable=self.field3,font=field_font,state='readonly',exportselection=0)
        self.feild_3_value["values"]=('0','1','2','3','4','5')
        self.feild_3_value.bind("<Return>", lambda e: self.feild_41_value.focus_set())
        self.feild_3_value.grid(row=8, column=1, padx=1, pady=0, columnspan=2)


        self.field_41_label = tk.Label(frame2, text="auto filter",fg="black",bg='white',font=Label1_font).grid(row=9,column=0, padx=0,pady=0,sticky='w')
        self.feild_41_value= tk.Spinbox(frame2,readonlybackground='white',highlightthickness=2,highlightcolor='yellow',textvariable=self.field4,font=field_font,state='readonly',exportselection=0)
        self.feild_41_value["values"]=('2','3','4','5','6','8','10','12','14','16','18','20','22','24','28')
        self.feild_41_value.bind("<Return>", lambda e: self.asktosave())
        self.feild_41_value.grid(row=9, column=1, padx=1, pady=0, columnspan=2)


        self.field_4_label = tk.Label(frame2, text=" \" COM-PORT DETAILS \" ", fg="green", bg='white',
                                      font=err_font).grid(row=12, column=0, padx=0, pady=0, sticky='w')

        frame2.pack(fill='both', expand=True)



    def asktosave(self):
        #        self.save()
        try:
            if (len(self.field0.get()) != 0):
                MsgBox = tk.messagebox.askquestion('Ask To Save', 'Do you want to save?', icon='question')
                if MsgBox == 'yes':
                    self.save()
                else:
                    pass
            else:
                self.errmsg.set("enter valid data")

        except:
            self.errmsg.set("error saving")

    def save(self):
        db.ComData(str(self.field0.get()), self.field1.get(), str(self.field2.get()), self.field3.get(), self.field4.get())
        self.controller.frames[StartPage].refresh()
        self.close()

    def clr(self):
        xcom=db.loadCom()
        self.field0.set(xcom[0])
        self.field1.set(xcom[1])
        self.field2.set(xcom[2])
        self.field3.set(xcom[3])
        self.field4.set(xcom[4])
        self.errmsg.set("")

    def close(self):
        self.clr()
        self.controller.show_frame(StartPage)
        self.controller.focus_set()


class JobPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        frame2 = tk.Frame(self, bg='white')
        self.field0 = tk.StringVar()
        self.field1 = tk.StringVar()
        self.field2 = tk.StringVar()
        self.field3 = tk.StringVar()
        self.field4 = tk.StringVar()
        self.controller = controller
        self.errmsg = tk.StringVar()

        
        err_font = Font(family="Arquitecta", size=10)
        Label1_font = Font(family="Arquitecta", size=14)
        field_font = Font(family="Arquitecta", size=12)

        self.errorlabel = tk.Label(frame2, width=25, height=1, textvariable=self.errmsg, fg="red", bg='white',
                                   font=err_font)
        self.errorlabel.grid(row=11, column=0, padx=1, pady=1, columnspan=3)
        self.field_2_label = tk.Label(frame2, text="ID :", fg="black", bg='white', font=Label1_font)
        self.field_2_label.grid(row=0, column=0, padx=0, pady=2, sticky='w')
        self.field_2_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field2, highlightthickness=2,state="disabled")
        self.field_2_value.grid(row=0, column=1, padx=1, pady=2, sticky='w')
        self.field_0_label = tk.Label(frame2, text="Variety:", fg="black", bg='white', font=Label1_font).grid(row=1,
                                                                                                             column=0,
                                                                                                             padx=0,
                                                                                                             pady=2,
                                                                                                             sticky='w')
        self.feild_0_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field0, highlightthickness=2,
                                      highlightcolor='yellow',width=50, font=field_font, justify='center', exportselection=0)

        self.feild_0_value.grid(row=1, column=1, padx=1, pady=2, columnspan=4)
        self.feild_0_value.bind("<KeyRelease>", self.on_entry_key)
        self.feild_0_value.bind("<Return>", lambda e:self.asktosave())

        self.field_1_label= tk.Label(frame2, text="Start Roll No.", fg="black", bg='white', font=Label1_font)
        self.field_1_label.grid(row=2, column=0, padx=0, pady=2, sticky='w')
        self.field_1_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field1, highlightthickness=2,state="disabled")
        self.field_1_value.grid(row=2, column=1, padx=1, pady=2, sticky='w')

        self.save_button = tk.Button(frame2, text="Save", fg="black", bg='white', font=field_font,command=lambda : self.asktosave())
        self.save_button.grid(row=2, column=4, padx=1, pady=2, sticky='w')



        treeview_width =500
        self.treeview = ttk.Treeview(frame2,  height=15, selectmode="extended",show="headings",columns=("ID","Variety","RollNo"))
        self.treeview.grid(row=4, column=0, padx=1, pady=2, columnspan=5)
        self.treeview.column("ID", minwidth=int(treeview_width * 0.05), width=int(treeview_width * 0.05), stretch=False, anchor="center")
        self.treeview.column("Variety", minwidth=int(treeview_width * 0.85), width=int(treeview_width * 0.85), stretch=False, anchor="center")
        self.treeview.column("RollNo", minwidth=int(treeview_width * 0.10), width=int(treeview_width * 0.10), stretch=False, anchor="center")
        self.treeview.heading("Variety", text="Variety")
        self.treeview.heading("RollNo", text="RollNo")
        self.treeview.heading("ID", text="ID")
        frame2.pack(fill='both', expand=True)
        self.treeview.bind("<Double-1>", self.onselect)
        self.reload_data()
        


    def on_entry_key(self, event):
        search_term = self.field0.get().lower()
        data=[]
        for row in self.variety_data:
            if search_term in row[1].lower():
                data.append(row)
        self.refresh_data(data)
        

    def reload_data(self):
        self.variety_data=db.loadVariety()
        self.refresh_data(self.variety_data)
        self.id=[]
        for row in self.variety_data:
            self.id.append(int(row[0]))

    def refresh_data(self, data):
        self.treeview.delete(*self.treeview.get_children())
        data=data[::-1]
        for row in data:
            self.treeview.insert(parent="", index="end", values=list(row))
            

    def onselect(self, event):
        w=self.treeview.selection()
        for item in w:
            self.field2.set(self.treeview.item(item, "values")[0])
            self.field0.set(self.treeview.item(item, "values")[1])
            self.field1.set(self.treeview.item(item, "values")[2])



    def asktosave(self):

        
        if (len(self.field0.get()) != 0):
            if (int(self.field2.get()) in self.id):
                MsgBox = tk.messagebox.askquestion('Ask To UPDATE', 'Do you want to UPDATE?', icon='question')
                if MsgBox=='yes':
                    db.update_Variety(self.field2.get(),self.field0.get(),self.field1.get())
                    self.reload_data()
                    self.clr()
                else:
                    pass
                
            else:
                MsgBox = tk.messagebox.askquestion('Ask To Save', 'Do you want to save?', icon='question')
                if MsgBox == 'yes':
                    self.save()
                else:
                    pass
        else:
            self.errmsg.set("enter valid data")

        # except:
        #     self.errmsg.set("error saving")

    def save(self):
        variety=self.field0.get()
        rollNo=self.field1.get()
        db.saveVariety(variety,rollNo)
        self.reload_data()
        self.clr()

    def clr(self):
        self.field0.set("")
        self.field1.set("0")
        self.field2.set(self.variety_data[-1][0]+1)
 
        self.errmsg.set("")

    def close(self):
        self.clr()
        self.controller.show_frame(StartPage)
        self.controller.focus_set()


class PasswordPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        frame2 = tk.Frame(self, bg='white')
        icon = Font(family="Web Symbols", size=12)

        Label1_font = Font(family="Arquitecta", size=20)

        field_font = Font(family="Arquitecta", size=25)

        self.field1 = tk.StringVar()
        self.err = tk.StringVar()

        self.controller = controller

        self.errlb = tk.Label(frame2, textvariable=self.err, fg="red", bg='white', height=1, width=20,
                              font=Label1_font).grid(row=3, column=1, padx=6, pady=5)

        self.field_1_label = tk.Label(frame2, text='PASSWORD', fg="black", bg='white', font=Label1_font).grid(row=4,
                                                                                                              column=0,
                                                                                                              padx=6,
                                                                                                              pady=5)
        self.feild_1_value = tk.Entry(frame2, show="*", fg="black", bg='white', textvariable=self.field1,
                                      highlightthickness=2, highlightcolor='yellow', font=field_font, justify='center',
                                      exportselection=0)
        self.feild_1_value.bind("<Return>", lambda e: self.submit())
        self.feild_1_value.grid(row=4, column=1, padx=6, pady=5)




        frame2.pack(fill='both', expand=True)

        controller.bind("<Alt_L>" + "<F8>", lambda e: self.F1())

    def F1(self):
        try:
            if (self.controller.hero.get() == "<class '__main__.StartPage'>"):
                self.controller.show_frame(PasswordPage)
                self.clr()
                self.feild_1_value.focus_set()

        except:
            pass

    def submit(self):
        if (str(self.field1.get()) == "setst" or str(self.field1.get()) == "SETST"):
            self.clr()
            self.controller.show_frame(StkSetPage)
            self.controller.frames[StkSetPage].feild_1_value.focus_set()
            self.controller.frames[StkSetPage].clear()

        elif (str(self.field1.get()) == "setcom" or str(self.field1.get()) == "SETCOM"):
            self.clr()
            self.controller.show_frame(ComPage)
            self.controller.frames[ComPage].feild_0_value.focus_set()
            self.controller.frames[ComPage].clr()

        elif (str(self.field1.get())=="jaishreeram" or str(self.field1.get())=="JAISHREERAM"):
            data=db.Update_lic()
            tk.messagebox.showinfo("LICENCE",f"VALUE {data} SAVED... PLEASE RESTART SOFTWARE")
            self.close()

        elif (str(self.field1.get()) == "delall" or str(self.field1.get()) == "DELALL"):
            self.clr()
            self.delall()


        elif (str(self.field1.get()) == "4011"):
            self.clr()
            self.controller.show_frame(JobPage)
            self.controller.frames[JobPage].feild_0_value.focus_set()
            self.controller.frames[JobPage].clr()



        else:
            self.field1.set("")
            self.err.set("incorrect password")

    def close(self):
        self.clr()
        self.controller.show_frame(StartPage)
        self.controller.focus_set()

    def clr(self):
        self.field1.set("")
        self.err.set("")

    def setLic(self):
        #self.save()
        try:
            if (len(self.field1.get())!=0):
                MsgBox = tk.messagebox.askquestion ('Are You Sure','Do you want to update licence?',icon = 'question')
                if MsgBox == 'yes':
                    rec=uuid.getnode()
                    db.suid(rec)
                    self.close()
                    MsgBox = tk.messagebox.showinfo("Done", str(rec)+" Licence activated")
                else:
                    pass
            else:
                self.err.set("enter valid data")

        except:
            self.err.set("error saving")



    def delall(self):
        #self.save()
        try:
            if (len(self.field1.get())!=0):
                MsgBox = tk.messagebox.askquestion ('Are You Sure','Do you want to Delete all record?',icon = 'question')
                if MsgBox == 'yes':
                    rec=db.reset()
                    self.close()
                    MsgBox = tk.messagebox.showinfo("Done", str(rec)+" Records Deleted Successfully")
                else:
                    pass
            else:
                self.err.set("enter valid data")

        except:
            self.err.set("error saving")


class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        frame2 = tk.Frame(self, bg='white')

        self.field0 = tk.StringVar()
        self.field1 = tk.StringVar()
        self.field2 = tk.StringVar()
        self.field3 = tk.StringVar()
        self.field4 = tk.StringVar()
        self.field5 = tk.StringVar()
        self.controller = controller
        self.errmsg = tk.StringVar()

        err_font = Font(family="Arquitecta", size=10)
        Label1_font = Font(family="Arquitecta", size=14)
        field_font = Font(family="Arquitecta", size=12)

        self.option_add('*TCombobox*Listbox.font', field_font)

        self.valid = self.register(self.only_int)
        self.validation = self.register(self.only_number)

        self.errorlabel = tk.Label(frame2, width=25, height=1, textvariable=self.errmsg, fg="red", bg='white',
                                   font=err_font)
        self.errorlabel.grid(row=11, column=0, padx=1, pady=1, columnspan=3)

        self.field_0_label = tk.Label(frame2, text="Lot No..:", fg="black", bg='white', font=Label1_font)
        self.field_0_label.grid(row=3, column=0, padx=0, pady=5, sticky='e')

        self.feild_0_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field0, state='disabled',
                                      highlightthickness=2, highlightcolor='yellow', font=field_font, justify='center',
                                      exportselection=0)
        self.feild_0_value.bind("<Return>", lambda e: self.feild_2_value.entry.focus_set())
        self.feild_0_value.grid(row=3, column=1, padx=1, pady=5, columnspan=2, sticky='w')

        self.field_1_label = tk.Label(frame2, text="Party Name:", fg="black", bg='white', font=Label1_font, height=1)
        self.field_1_label.grid(row=4, column=0, padx=0, pady=5, sticky='e')

        self.feild_1_value = tk.Entry(frame2, width=50, textvariable=self.field1)
        self.feild_1_value.bind("<KeyRelease>", self.on_entry_key1)
        self.feild_1_value.bind("<FocusIn>", self.show_dropdown1)
        self.feild_1_value.bind("<Return>", lambda e: self.feild_2_value.focus_set())
        self.feild_1_value.bind("<FocusOut>", self.hide_dropdown1)  # Bind focus out event
        self.feild_1_value.grid(row=4, column=1, padx=1, pady=5, columnspan=2, sticky='w')
        


        self.listbox1_popup = tk.Toplevel(parent)
        self.listbox1_popup.wm_overrideredirect(True)  # Remove window decorations
        self.listbox1_popup.withdraw()  # Hide initially

        self.listbox1 = tk.Listbox(self.listbox1_popup, height=5, width=50)
        self.listbox1.pack()
        self.listbox1.bind("<<ListboxSelect>>", self.on_select1)
        self.listbox1.bind("<FocusOut>", self.hide_dropdown1)
 

        self.field_2_label = tk.Label(frame2, text="Job Name:", fg="black", bg='white', font=Label1_font)
        self.field_2_label.grid(row=6, column=0, padx=0, pady=5, sticky='e')

        self.feild_2_value = tk.Entry(frame2, width=50, textvariable=self.field2)
        self.feild_2_value.bind("<KeyRelease>", self.on_entry_key2)
        self.feild_2_value.bind("<FocusIn>", self.show_dropdown2)
        self.feild_2_value.bind("<Return>", lambda e: self.feild_3_value.focus_set())
        self.feild_2_value.bind("<FocusOut>", self.hide_dropdown2)  # Bind focus out event
        self.feild_2_value.grid(row=6, column=1, padx=1, pady=5, columnspan=2, sticky='w')


        self.listbox2_popup = tk.Toplevel(parent)
        self.listbox2_popup.wm_overrideredirect(True)  # Remove window decorations
        self.listbox2_popup.withdraw()  # Hide initially

        self.listbox2 = tk.Listbox(self.listbox2_popup, height=5, width=50)
        self.listbox2.pack()
        self.listbox2.bind("<<ListboxSelect>>", self.on_select2)
        self.listbox2.bind("<FocusOut>", self.hide_dropdown2)
        

        self.field_3_label = tk.Label(frame2, text="Core wt.:", fg="black", bg='white', font=Label1_font)
        self.field_3_label.grid(row=7, column=0, padx=0, pady=0, sticky='e')

        self.feild_3_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field3, validate='key',
                                      validatecommand=(self.validation, '%P'), highlightthickness=2,
                                      highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.feild_3_value.bind("<Return>", lambda e: self.feild_4_value.focus_set())
        self.feild_3_value.grid(row=7, column=1, padx=1, pady=10, columnspan=2, sticky='w')

        self.field_4_label = tk.Label(frame2, text="Tare wt.:", fg="black", bg='white', font=Label1_font)
        self.field_4_label.grid(row=8, column=0, padx=0, pady=5, sticky='e')

        self.feild_4_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field4, validate='key',
                                      validatecommand=(self.validation, '%P'), highlightthickness=2,
                                      highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.feild_4_value.bind("<Return>", lambda e: self.asktosave())
        self.feild_4_value.grid(row=8, column=1, padx=1, pady=5, columnspan=2, sticky='w')

        self.field_5_label = tk.Label(frame2, text="Start Roll No..:", fg="black", bg='white', font=Label1_font)
        self.field_5_label.grid(row=9, column=0, padx=0, pady=5, sticky='e')

        self.feild_5_value = tk.Entry(frame2, fg="black", bg='white', textvariable=self.field5, validate='key',state='disabled',
                                      validatecommand=(self.valid, '%P'), highlightthickness=2,
                                      highlightcolor='yellow', font=field_font, justify='center', exportselection=0)
        self.feild_5_value.bind("<Return>", lambda e: self.savebut.focus_set())
        self.feild_5_value.grid(row=9, column=1, padx=1, pady=5, columnspan=2, sticky='w')

        self.savebut = tk.Button(frame2, text='Save', width=10, font=field_font, bg='lightgrey',
                                 activebackground='lightgrey', activeforeground='black', command=lambda: self.asktosave())
        self.savebut.bind("<Return>", lambda e: self.asktosave())
        self.savebut.grid(row=10, column=1, pady=1)

        self.field_41_label = tk.Label(frame2, text=" \" Save data \" ", fg="green", bg='white', font=err_font)
        self.field_41_label.grid(row=12, column=0, padx=0, pady=0, sticky='w', columnspan=3)

        frame2.pack(fill='both', expand=True)

        controller.bind("<F1>", lambda e: self.F1())
        controller.bind("<Alt_L>" + "<m>", lambda e: self.enf0())


    def enf0(self):
        if (self.controller.hero.get() == "<class '__main__.PageThree'>"):
            self.feild_0_value.configure(state="normal")
            #self.feild_5_value.configure(state="normal")


    def only_int(self,char):
        if char.isdigit():
            return True
        elif char == "":
            return True
        else:
            return False




    def only_number(self,char):
        if char=="":
            return True

        else:
            try:
                float(char)
            except:
                return False

        return True

    def F1(self):


        try:
            if (self.controller.hero.get() == "<class '__main__.StartPage'>"):
                self.controller.show_frame(PageThree)

                with open('PartyName.txt') as p:
                    self.options1=self.load_options('PartyName.txt')
                    for option in self.options1:
                        self.listbox1.insert(tk.END, option)
                    self.field1.set(self.listbox1.get(0))


                
                self.options2=db.loadVariety()

                    
                for option in self.options2:
                    self.listbox2.insert(tk.END, option[1])
                self.field2.set(self.listbox2.get(0))

                self.clr()





        except:
            pass

    def asktosave(self):
        
        try:
            if (len(self.field1.get()) != 0):
                MsgBox = tk.messagebox.askquestion('Ask To Save', 'Do you want to save?', icon='question')
                if MsgBox == 'yes':
                    self.save()
                else:
                    pass
            else:
                self.errmsg.set("enter valid data")

        except:
            self.errmsg.set("error saving")

    def save(self):
        today=datetime.datetime.today()
        xdate=today.strftime("%d-%m-%y")
        db.SaveData(str(self.field1.get()), str(self.field2.get()), self.field3.get(), self.field4.get(), xdate)
        
        db.splno(self.field0.get())

        self.controller.frames[StartPage].refresh()
        self.close()

    def clr(self):
        c=db.loadData()

        RollNo=db.lrst(c[1])
        plno=db.lplno()
        self.field0.set(plno)
        self.field1.set(c[0])
        self.field2.set(c[1])
        self.field3.set(c[2])
        self.field4.set(c[3])
        self.field5.set(RollNo)
        self.feild_0_value.configure(state="disabled")
        self.errmsg.set("")
        

    def close(self):
        self.clr()
        self.controller.show_frame(StartPage)
        self.controller.focus_set()


    def load_options(self,filename):
        x=[]
        with open(filename) as f:
            for data in f.readlines():
                x.append(data.strip())

        return x
    
    def on_entry_key1(self, event):
        search_term = self.field1.get().lower()
        self.listbox1.delete(0, tk.END)
        for option in self.options1:
            if search_term in option.lower():
                self.listbox1.insert(tk.END, option)
        self.show_dropdown1()

    def on_select1(self, event):
        if self.listbox1.curselection():
            self.current_selection1 = self.listbox1.get(self.listbox1.curselection()[0])
            self.field1.set(self.current_selection1)
            self.listbox1.delete(0, tk.END)
            self.listbox1.insert(tk.END, self.current_selection1)
            self.hide_dropdown1()
              # Move focus to entry1 to trigger FocusOut on listbox1
            self.controller.focus_set()
        else:
            self.hide_dropdown1()
        

        
        

    def show_dropdown1(self, event=None):
        if not self.listbox1_popup.winfo_viewable():
            x = self.feild_1_value.winfo_rootx()
            y = self.feild_1_value.winfo_rooty() + self.feild_1_value.winfo_height()
            self.listbox1_popup.geometry(f"+{x}+{y}")
            self.listbox1_popup.deiconify()  # Show the Toplevel
            
    def hide_dropdown1(self, event=None):
        self.listbox1_popup.withdraw()
        if self.feild_1_value.get().strip() == "" or self.listbox1.get(0)=="":
            self.field1.set(self.options1[0])
        else:
            self.listbox1_popup.withdraw() 
            self.field1.set(self.listbox1.get(0))
        

    def on_entry_key2(self, event):
        search_term = self.field2.get().lower()
        self.listbox2.delete(0, tk.END)
        for option in self.options2:
            if search_term in option[1].lower():
                self.listbox2.insert(tk.END, option[1])
                
        self.show_dropdown2()

    def on_select2(self, event):
        if self.listbox2.curselection():
            self.current_selection2 = self.listbox2.get(self.listbox2.curselection()[0])
            self.field2.set(self.current_selection2)
            self.listbox2.delete(0, tk.END)
            self.listbox2.insert(tk.END, self.current_selection2)
            
            self.hide_dropdown2()
              # Move focus to entry2 to trigger FocusOut on listbox2
            self.controller.focus_set()
        else:
            self.hide_dropdown2()
            
            
        
        

    def show_dropdown2(self, event=None):
        if not self.listbox2_popup.winfo_viewable():
            x = self.feild_2_value.winfo_rootx()
            y = self.feild_2_value.winfo_rooty() + self.feild_2_value.winfo_height()
            self.listbox2_popup.geometry(f"+{x}+{y}")
            self.listbox2_popup.deiconify()  # Show the Toplevel
        
            
    def hide_dropdown2(self, event=None):
        self.listbox2_popup.withdraw()

        if self.feild_2_value.get().strip() == "" or self.listbox2.get(0)=="":
            self.field2.set(self.options2[0][1])
        else:
            self.listbox2_popup.withdraw() 
            self.field2.set(self.listbox2.get(0))
        
        rollno=db.lrst(self.field2.get())
        self.field5.set(rollno)
               
        



        




if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = MainApp()
    app.mainloop()
    SerialThread.daemon=True









