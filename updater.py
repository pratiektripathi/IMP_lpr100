import tkinter as tk




class Updater(tk.Tk):

    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)

        self.title("Updater")
        xcord=(self.winfo_screenwidth()/2)-150
        ycord=(self.winfo_screenheight()/2)-75
        

        self.geometry("300x150"+"+"+str(int(xcord))+"+"+str(int(ycord)))

        self.dot=tk.StringVar()

        self.iconbitmap('myicon.ico')
        self.resizable(False,False)

        self.frame1=tk.Frame(self,bg="#ADD8E0")
        self.label1=tk.Label(self.frame1,text="Checking For Update",font=("Arquitecta",12),bg="#ADD8E0")
        self.label1.grid(row=0,column=0,pady=5)

        self.label2=tk.Label(self.frame1,textvariable=self.dot,font=("Arquitecta",16),fg="red",bg="#ADD8E0")
        self.dot.set("")
        self.label2.grid(row=1,column=0,pady=5)

        self.frame1.pack(fill="both",expand=True)

        self.check()

    def check(self):
        if len(self.dot.get())<5:
            self.dot.set(self.dot.get()+"*")
            
        else:
            self.dot.set("")
        self.after(500,self.check)


if __name__=="__main__":
    app=Updater()
    app.mainloop()