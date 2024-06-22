#!/usr/bin/env python3
import datetime
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
import db
import exel
from tkcalendar import DateEntry
import report2
import templete as temp
import zebrapl
import sqlite3 as lite


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

        for F in (StartPage, ComPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame(StartPage)





        self.queue = multiprocessing.Queue()
        self.thread = SerialThread(self.queue)
        self.thread.start()

        self.process_serial()
        self.checkbt()



    def ext(self):
        self.frames[PageOne].close()
        self.frames[PageTwo].close()
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

        framec4.grid(row=0, column=0,padx=3,sticky='ew',columnspan=5)


        framec2= tk.Frame(frame2, bg='yellow')

        self.field_0b_label = tk.Label(framec2, text='Lot No.:', fg="black", bg='yellow',  font=Label1_font)
        self.field_0b_label.grid(row=0, column=0,padx=3, pady=1,sticky='n')

        self.field_1b_label = tk.Label(framec2, textvariable=self.field1b, fg="black", bg='yellow', font=Label1_font)
        self.field_1b_label.grid(row=0, column=1,padx=3)

        self.field_0_label = tk.Label(framec2, text='Party.:', fg="black", bg='yellow',  font=Label1_font)
        self.field_0_label.grid(row=1, column=0,padx=3, pady=1,sticky='n')

        self.field_1_label = tk.Label(framec2, textvariable=self.field1, fg="black", bg='yellow', font=Label1_font)
        self.field_1_label.grid(row=1, column=1,padx=3)

        framec2.grid(row=1, column=0,padx=3,columnspan=5,sticky='ew')


        framec1 = tk.Frame(frame2,bg='white')

        itrow = temp.loadData()
        Variety=str(itrow[1])
        weight=str(itrow[2])
        CoreWt=str(itrow[3])
        TareWt = str(itrow[4])
        NetWt = str(itrow[5])
        Rollno = str(itrow[6])
        xdate=str(itrow[7])



        self.f1.set("PIONEER PACKAGERS")
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


        framec1.grid(row=2,column=0,   padx = 10, pady = 5)






        framec3= tk.Frame(frame2, bg='yellow')

        self.savebut = tk.Button(framec3, text='Change', width=10, bg='lightgrey',font=icon, activebackground='lightgrey',
                                 activeforeground='black', command=lambda: self.Change())

        self.savebut.bind("<Return>", lambda e: self.Change())
        self.savebut.grid(row=1, column=0, padx=5, pady=5 )

        self.reportbut = tk.Button(framec3, text='Packing list', width=15, bg='lightgrey',font=icon, activebackground='lightgrey',
                                 activeforeground='black', command=lambda: self.reporter())

        self.reportbut.bind("<Return>", lambda e: self.reporter())
        self.reportbut.grid(row=1, column=3, padx=5, pady=5 )


        framec3.grid(row=3, column=0,padx=3,sticky='ew',columnspan=5)








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

                self.f1.set("PIONEER PACKAGERS")
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
        self.controller.frames[PageThree].feild_1_value.focus_set()


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



        self.f1.set("PIONEER PACKAGERS")
        self.f2.set("Job Name.:"+Variety)
        self.f3.set("Gross wt.:"+weight)
        self.f4.set("Core wt.:"+CoreWt)
        self.f4.set("Tare wt.:" + TareWt)
        self.f5.set("Net wt.:" + NetWt)
        self.f6.set("Roll No..:" + Rollno)
        self.f7.set(xdate)

    def reporter(self):
        window=Window(self)
        window.grab_set()

class Window(tk.Toplevel):

    def __init__(self, parent, **kwargs):
        tk.Toplevel.__init__(self, parent, **kwargs)

        self.geometry(str(self.winfo_screenwidth()) + "x" + str(self.winfo_screenheight()))
        self.state('zoomed')
        self.iconbitmap('myicon.ico')
        self.focus_set()
        self.allrows = db.GetAll()
        self.title("Packing List Database")
        self.frame_but = tk.Frame(self, bg='white')
        self.frame_top = tk.Frame(self, bg='white')
        self.count = tk.StringVar()
        self.cc = 0
        count_font = Font(family="Arquitecta", size=8)
        self.count.set(str(self.cc) + " data marked")

        data = self.allrows
        self.rows = len(data)
        self.columns = len(data[0])
        data = [[0] + list(row) for row in data]

        self.errlb = tk.Label(self.frame_but, textvariable=self.count, fg="black", bg='white', width=30, font=count_font)
        self.errlb.grid(row=0, column=0)

        self.savebut = tk.Button(self.frame_but, text='Packing list', width=20, bg='lightgrey', activebackground='lightgrey',
                                 activeforeground='black', command=lambda: self.printing())
        self.savebut.grid(row=0, column=1)

        self.markall = tk.Button(self.frame_but, text='mark all', width=20, bg='lightgrey', activebackground='lightgrey',
                                 activeforeground='black', command=lambda: self.mall())
        self.markall.grid(row=0, column=2)

        self.umarkall = tk.Button(self.frame_but, text='unmark all', width=20, bg='lightgrey', activebackground='lightgrey',
                                  activeforeground='black', command=lambda: self.umall())
        self.umarkall.grid(row=0, column=3)

        self.delbut = tk.Button(self.frame_but, text='delete marked', width=20, bg='lightgrey', activebackground='lightgrey',
                                activeforeground='black', command=lambda: self.delcheck())
        self.delbut.grid(row=0, column=4)

        self.gen_excel_but = tk.Button(self.frame_but, text='Generate Excel', width=20, bg='lightgrey', activebackground='lightgrey',
                                       activeforeground='black', command=lambda: self.generate_excel())
        self.gen_excel_but.grid(row=0, column=5)

        # Dropdown widget for filtering
        self.status_filter = tk.StringVar()
        self.status_filter.set("All")
        self.filter_options = ["Pending", "Done", "All"]
        self.filter_dropdown = tk.OptionMenu(self.frame_but, self.status_filter, *self.filter_options, command=self.filter_data)
        self.filter_dropdown.grid(row=0, column=6)

        self.frame_but.pack()

        self.tree = ttk.Treeview(self.frame_top, columns=list(range(self.columns + 1)), show="headings")

        # Set up the table headings
        self.tree.heading(0, text="")
        self.tree.heading(1, text="SNo.")
        self.tree.heading(2, text="P.L. No.")
        self.tree.heading(3, text="Party")
        self.tree.heading(4, text="Job Name")
        self.tree.heading(5, text="Roll No.")
        self.tree.heading(6, text="Gross Wt.")
        self.tree.heading(7, text="Tare Wt.")
        self.tree.heading(8, text="Core Wt.")
        self.tree.heading(9, text="Net Wt.")
        self.tree.heading(10, text="Status")  # New status column

        self.tree.column(0, width=10, stretch=True)
        self.tree.column(1, width=20, stretch=True)
        self.tree.column(2, width=20, stretch=True)
        self.tree.column(3, width=300, stretch=True)
        self.tree.column(4, width=300, stretch=True)
        self.tree.column(5, width=30, stretch=True)
        self.tree.column(6, width=30, stretch=True)
        self.tree.column(7, width=30, stretch=True)
        self.tree.column(8, width=30, stretch=True)
        self.tree.column(9, width=30, stretch=True)
        self.tree.column(10, width=100, stretch=True)  # New status column width

        # Populate the table with the data
        self.tree_data = [[0] + list(row) for row in self.allrows]
        for i in range(self.rows):
            self.tree.insert("", "end", values=self.tree_data[i], tags=("readonly",))
        self.tree.tag_configure("readonly", background="#f0f0f0")

        # Bind keys '1' and '0' to toggle the value of the first column in the currently focused row
        self.tree.bind("<KeyPress-1>", self.toggle_value)
        self.tree.bind("<KeyPress-0>", self.toggle_value)

        # Set the focus on the first cell of the second column
        self.tree.focus_set()
        # self.tree.selection_add(self.tree.get_children()[0])
        # self.tree.focus(self.tree.get_children()[0])
        # self.tree.selection_remove(self.tree.selection())

        vsb = ttk.Scrollbar(self.frame_top, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.frame_top.pack(fill="both", expand=True, padx=10, pady=10)

    def mall(self):
        for item in self.tree.get_children():
            self.tree.item(item, values=[1 if i == 0 else val for i, val in enumerate(self.tree.item(item)["values"])])
        self.cc = len(self.tree.get_children())
        self.count.set(str(self.cc) + " data marked")

    def umall(self):
        for item in self.tree.get_children():
            self.tree.item(item, values=[0 if i == 0 else val for i, val in enumerate(self.tree.item(item)["values"])])
        self.cc = 0
        self.count.set(str(self.cc) + " data marked")

    def generate_excel(self):
        con=lite.connect("batch.db")
        cur=con.cursor()
        for data in self.get():
            cur.execute("""UPDATE bat SET Status=:Status WHERE id=:id""",{'id':data[1],'Status':"Done"})
        con.commit()
        con.close()

        exel.create_report(self.get())
        self.print_exel()
        
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.allrows = db.GetAll()
        self.tree_data = [[0] + list(row) for row in self.allrows]
        for i in range(len(self.tree_data)):
            self.tree.insert("", "end", values=self.tree_data[i], tags=("readonly",))

    def toggle_value(self, event):
        selected_items = self.tree.selection()
        for selected_item in selected_items:
            values = self.tree.item(selected_item, 'values')
            f_value = values[0]
            if event.char == "1" and f_value == "0":
                value = "1"
                self.cc = self.cc + 1
            elif event.char == "0" and f_value == "1":
                value = "0"
                self.cc = self.cc - 1
            else:
                continue
            self.tree.set(selected_item, 0, value)
        
        self.count.set(str(self.cc) + " data marked")

    def get(self):
        # Return the values in the table as a list of lists
        values = []
        for child in self.tree.get_children():
            row = self.tree.item(child)["values"]
            if row[0] == 1:
                values.append(row)
        return values

    def printing(self):
        con=lite.connect("batch.db")
        cur=con.cursor()
        for data in self.get():
            cur.execute("""UPDATE bat SET Status=:Status WHERE id=:id""",{'id':data[1],'Status':"Done"})
        con.commit()
        con.close()

        report2.create_report(self.get())
        self.print_pdf()
        self.allrows = db.GetAll()
        
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.tree_data = [[0] + list(row) for row in self.allrows]
        for i in range(len(self.tree_data)):
            self.tree.insert("", "end", values=self.tree_data[i], tags=("readonly",))

    def delcheck(self):
        nos = len([x[1] for x in self.get()])
        try:
            if nos != 0:
                MsgBox = tk.messagebox.askquestion('Are You Sure', 'Do you want to delete ' + str(nos) + ' number of data', icon='question')
                if MsgBox == 'yes':
                    self.delsel()
                    MsgBox = tk.messagebox.showinfo("Done", str(nos) + " number of data deleted")
                else:
                    pass
            else:
                pass
        except:
            pass

    def delsel(self):
        db.delid([x[1] for x in self.get()])

        for row in self.tree.get_children():
            self.tree.delete(row)

        # Reload all rows
        self.allrows = db.GetAll()
        self.tree_data = [[0] + list(row) for row in self.allrows]

        for i in range(len(self.tree_data)):
            self.tree.insert("", "end", values=self.tree_data[i], tags=("readonly",))
        self.tree.tag_configure("readonly", background="#f0f0f0")
        self.cc = 0
        self.count.set(str(self.cc) + " data marked")

    def print_exel(self):
        filename = "packing_list.xlsx"
        # Open the PDF file using the default PDF viewer
        subprocess.run(["start", filename], shell=True)

    def print_pdf(self):
        filename = "packing_list.pdf"
        # Open the PDF file using the default PDF viewer
        subprocess.run(["start", filename], shell=True)

    def filter_data(self, selection):
        # Save the current values of the first column (checkbox column)
        checkbox_values = {self.tree.item(row)["values"][1]: self.tree.item(row)["values"][0] for row in self.tree.get_children()}

        # Clear the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Filter rows based on selection
        if selection == "All":
            filtered_data = self.allrows
        else:
            filtered_data = [row for row in self.allrows if row[-1] == selection]

        # Add filtered rows and restore checkbox values
        self.tree_data = [[0] + list(row) for row in filtered_data]
        for row in self.tree_data:
            row[0] = checkbox_values.get(row[1], 0)  # Restore checkbox value or default to 0
            self.tree.insert("", "end", values=row, tags=("readonly",))
        self.tree.tag_configure("readonly", background="#f0f0f0")



class PageOne(tk.Frame):

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
        fixrow = db.getfix(fixrow)

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
        self.feild_41_value["values"]=('4','6','8','10','12','14','16','18','20','22','24','28')
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


class PageTwo(tk.Frame):

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
                self.controller.show_frame(PageTwo)
                self.clr()
                self.feild_1_value.focus_set()

        except:
            pass

    def submit(self):
        if (str(self.field1.get()) == "setst" or str(self.field1.get()) == "SETST"):
            self.clr()
            self.controller.show_frame(PageOne)
            self.controller.frames[PageOne].feild_1_value.focus_set()
            self.controller.frames[PageOne].clear()

        elif (str(self.field1.get()) == "setcom" or str(self.field1.get()) == "SETCOM"):
            self.clr()
            self.controller.show_frame(ComPage)
            self.controller.frames[ComPage].feild_0_value.focus_set()
            self.controller.frames[ComPage].clr()

        elif (str(self.field1.get())=="jaishreeram" or str(self.field1.get())=="JAISHREERAM"):
            data=db.Update_lic()
            tk.messagebox.showinfo("LICENCE",f"VALUE {data} SAVED... PLEASE RESTART SOFTWARE")
            self.close()

        if (str(self.field1.get()) == "delall" or str(self.field1.get()) == "DELALL"):
            self.delall()




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
        self.validation=self.register(self.only_number)




        self.errorlabel = tk.Label(frame2, width=25, height=1, textvariable=self.errmsg, fg="red", bg='white',
                                   font=err_font)
        self.errorlabel.grid(row=11, column=0, padx=1, pady=1, columnspan=3)


        self.field_0_label = tk.Label(frame2, text="Lot No..:",fg="black",bg='white',font=Label1_font).grid(row=3,column=0, padx=0,pady=5,sticky='e')
        #
        self.feild_0_value = tk.Entry(frame2,fg="black",bg='white', textvariable=self.field0,state='disabled',highlightthickness=2,highlightcolor='yellow',font=field_font,justify='center',exportselection=0)
        self.feild_0_value.bind("<Return>", lambda e: self.feild_2_value.focus_set())
        self.feild_0_value.grid(row=3,column=1, padx=1,pady=5,columnspan=2,sticky='w')





        self.field_1_label = tk.Label(frame2, text="Party Name:", fg="black", bg='white', font=Label1_font, height=1).grid(
            row=4, column=0, padx=0, pady=5, sticky='e')



        self.feild_1_value= ttk.Combobox(frame2,background='white',height=15,width=45,textvariable=self.field1,font=field_font,state='readonly',exportselection=0)

        self.feild_1_value.bind("<Return>", lambda e: self.feild_2_value.focus_set())
        self.feild_1_value.grid(row=4,column=1, padx=5,pady=5,columnspan=2,sticky='w')

        # field3
        self.field_2_label = tk.Label(frame2, text="Job Name:", fg="black", bg='white', font=Label1_font).grid(row=6,
                                                                                                             column=0,
                                                                                                             padx=0,
                                                                                                             pady=5,
                                                                                                             sticky='e')


        self.feild_2_value=ttk.Combobox(frame2,background='white',height=15,width=45,textvariable=self.field2,state='readonly',font=field_font,exportselection=0)
        self.feild_2_value.bind("<Return>", lambda e: self.feild_3_value.focus_set())
        self.feild_2_value.grid(row=6,column=1, padx=1,pady=5,columnspan=2)







        self.field_3_label = tk.Label(frame2, text="Core wt.:",fg="black",bg='white',font=Label1_font).grid(row=7,column=0, padx=0,pady=0,sticky='e')

        self.feild_3_value = tk.Entry(frame2,fg="black",bg='white', textvariable=self.field3,validate='key',validatecommand=(self.validation,'%P'), highlightthickness=2,highlightcolor='yellow',font=field_font,justify='center',exportselection=0)
        self.feild_3_value.bind("<Return>", lambda e: self.feild_4_value.focus_set())
        self.feild_3_value.grid(row=7,column=1, padx=1,pady=10,columnspan=2,sticky='w')


        self.field_4_label = tk.Label(frame2, text="Tare wt.:",fg="black",bg='white',font=Label1_font).grid(row=8,column=0, padx=0,pady=5,sticky='e')
        #
        self.feild_4_value = tk.Entry(frame2,fg="black",bg='white', textvariable=self.field4,validate='key',validatecommand=(self.validation,'%P'), highlightthickness=2,highlightcolor='yellow',font=field_font,justify='center',exportselection=0)
        self.feild_4_value.bind("<Return>", lambda e: self.feild_5_value.focus_set())
        self.feild_4_value.grid(row=8,column=1, padx=1,pady=5,columnspan=2,sticky='w')


        self.field_5_label = tk.Label(frame2, text="Start Roll No..:",fg="black",bg='white',font=Label1_font).grid(row=9,column=0, padx=0,pady=5,sticky='e')
        #
        self.feild_5_value = tk.Entry(frame2,fg="black",bg='white', textvariable=self.field5, validate='key',validatecommand=(self.valid,'%P'),highlightthickness=2,highlightcolor='yellow',font=field_font,justify='center',exportselection=0)
        self.feild_5_value.bind("<Return>", lambda e: self.savebut.focus_set())
        self.feild_5_value.grid(row=9,column=1, padx=1,pady=5,columnspan=2,sticky='w')

        self.savebut = tk.Button(frame2, text='Save', width=10,font=field_font, bg='lightgrey', activebackground='lightgrey',
                                 activeforeground='black', command=lambda: self.asktosave())

        self.savebut.bind("<Return>", lambda e: self.asktosave())
        self.savebut.grid(row=10, column=1, pady=1)

        self.field_41_label = tk.Label(frame2, text=" \" Save data \" ", fg="green", bg='white',
                                      font=err_font).grid(row=12, column=0, padx=0, pady=0, sticky='w',columnspan=3)

        frame2.pack(fill='both', expand=True)


        controller.bind("<F1>", lambda e: self.F1())
        controller.bind("<Alt_L>" + "<m>", lambda e: self.enf0())


    def enf0(self):
        if (self.controller.hero.get() == "<class '__main__.PageThree'>"):
            self.feild_0_value.configure(state="normal")


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
                    self.feild_1_value["values"]=p.readlines()
                    self.feild_1_value.current(0)
                with open('JobName.txt') as v:
                    self.feild_2_value["values"] = v.readlines()
                    self.feild_2_value.current(0)
                self.clr()

                self.feild_1_value.focus_set()




        except:
            pass

    def asktosave(self):
        #        self.save()
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
        db.srst(self.field5.get())
        db.splno(self.field0.get())

        self.controller.frames[StartPage].refresh()
        self.close()

    def clr(self):
        c=db.loadData()
        RollNo=db.lrst()
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





if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = MainApp()
    app.mainloop()
    SerialThread.daemon=True









