import sqlite3 as lite
import pickle
import psutil
import datetime

#backend

def wbbatchData():

    con=lite.connect("batch.db")
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS bat (id INTEGER PRIMARY KEY AUTOINCREMENT,plno TEXT,Party TEXT,Variety TEXT,RollNo TEXT,GrossWt TEXT,CoreWt TEXT,TareWt TEXT,NetWt TEXT)")
    con.commit()
    con.close()




def wbfixData():

    con=lite.connect("wb.db")
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS fix (id INTEGER PRIMARY KEY AUTOINCREMENT, f1 TEXT,f1fs INTEGER NOT NULL,x1 INTEGER,y1 INTEGER,f2 TEXT,f2fs INTEGER NOT NULL,x2 INTEGER,y2 INTEGER,f3 TEXT,f3fs INTEGER NOT NULL,x3 INTEGER,y3 INTEGER,f4 TEXT,f4fs INTEGER NOT NULL,x4 INTEGER,y4 INTEGER,f5 TEXT,f5fs INTEGER NOT NULL,x5 INTEGER,y5 INTEGER,f6 TEXT,f6fs INTEGER NOT NULL,x6 INTEGER,y6 INTEGER,f7 TEXT,f7fs INTEGER NOT NULL,x7 INTEGER,y7 INTEGER,f8 TEXT,f8fs INTEGER NOT NULL,x8 INTEGER,y8 INTEGER,f9 TEXT,f9fs INTEGER NOT NULL,x9 INTEGER,y9 INTEGER,f10 TEXT,f10fs INTEGER NOT NULL,x10 INTEGER,y10 INTEGER, b TEXT,bfs INTEGER NOT NULL,bcode TEXT NOT NULL,barx INTEGER,bary INTEGER)")
    con.commit()
    con.close()
    
def getfix(row):

    con=lite.connect("wb.db")
    cur=con.cursor()
    cur.execute("SELECT * FROM fix WHERE id=1 ")
    row=cur.fetchone()
    con.close()
    return row



def UpdatefixData(f1,f1fs,x1,y1,f2,f2fs,x2,y2,f3,f3fs,x3,y3,f4,f4fs,x4,y4,f5,f5fs,x5,y5,f6,f6fs,x6,y6,f7,f7fs,x7,y7,f8,f8fs,x8,y8,f9,f9fs,x9,y9,f10,f10fs,x10,y10,b,bfs,bcode,barx,bary):

    
    con=lite.connect("wb.db")
    cur=con.cursor()
    cur.execute("""UPDATE fix SET f1=:f1, f1fs=:f1fs, x1=:x1, y1=:y1, f2=:f2, f2fs=:f2fs, x2=:x2, y2=:y2, f3=:f3, f3fs=:f3fs, x3=:x3, y3=:y3, f4=:f4, f4fs=:f4fs, x4=:x4, y4=:y4, f5=:f5, f5fs=:f5fs, x5=:x5, y5=:y5,f6=:f6, f6fs=:f6fs, x6=:x6, y6=:y6, f7=:f7, f7fs=:f7fs, x7=:x7, y7=:y7, f8=:f8, f8fs=:f8fs, x8=:x8, y8=:y8, f9=:f9, f9fs=:f9fs, x9=:x9, y9=:y9, f10=:f10, f10fs=:f10fs, x10=:x10, y10=:y10, b=:b, bfs=:bfs, bcode=:bcode ,barx=:barx, bary=:bary WHERE id=1""",{'f1':f1,'f1fs':f1fs,'x1':x1,'y1':y1,'f2':f2,'f2fs':f2fs,'x2':x2,'y2':y2,'f3':f3,'f3fs':f3fs,'x3':x3,'y3':y3,'f4':f4,'f4fs':f4fs,'x4':x4,'y4':y4,'f5':f5,'f5fs':f5fs,'x5':x5,'y5':y5,'f6':f6,'f6fs':f6fs,'x6':x6,'y6':y6,'f7':f7,'f7fs':f7fs,'x7':x7,'y7':y7,'f8':f8,'f8fs':f8fs,'x8':x8,'y8':y8,'f9':f9,'f9fs':f9fs,'x9':x9,'y9':y9,'f10':f10,'f10fs':f10fs,'x10':x10,'y10':y10,'b':b,'bfs':bfs,'bcode':bcode,'barx':barx,'bary':bary })
    con.commit()
    con.close()



def SaveData(Party,Variety,CoreWt,TareWt,RollNo):
   
    # initializing data to be stored in db 
    
    master = {'Party':Party.strip('\n'),'Variety':Variety.strip('\n'),'CoreWt':CoreWt,'TareWt':TareWt,'RollNo':RollNo}
    # Its important to use binary mode 
    static = open('static.dat', 'wb')
    # source, destination 
    pickle.dump(master, static)                      
    static.close()


def loadData():

    # for reading also binary mode is important
    static = open('static.dat', 'rb')
    dat = pickle.load(static)
    d0 = dat.get("Party","")
    d1 = dat.get("Variety","")
    d2 = dat.get("CoreWt","")
    d3 = dat.get("TareWt","")
    d4 = dat.get("RollNo", "")
    data=[d0,d1,d2,d3,d4]
    static.close()
    return data



def loadLogo():

    # for reading also binary mode is important
    with open('logo.txt') as p:
        data = p.readlines()

    return data



def loadPrint():

    # for reading also binary mode is important
    with open('Printer.txt') as p:
        data = p.readlines()

    return data



def SaveBatching(LotNo,RollNo,Party, Variety,GrossWt, TareWt,CoreWt, NetWt,Date,Status):
    con=lite.connect("batch.db")
    cur=con.cursor()
    cur.execute("""INSERT INTO bat (LotNo,RollNo,Party,Variety,GrossWt,TareWt,CoreWt,NetWt,Date,Status) VALUES (?,?,?,?,?,?,?,?,?,?)""",(LotNo,RollNo,Party, Variety,GrossWt, TareWt,CoreWt, NetWt,Date,Status))
    con.commit()
    con.close()



def GetBatchData(LotNo):
    con=lite.connect("batch.db")
    cur=con.cursor()
    cur.execute("SELECT LotNo,RollNo,Party,Variety,GrossWt,TareWt,CoreWt,NetWt,Date,Status FROM bat WHERE LotNo=:LotNo",{'plno':LotNo})
    rows=cur.fetchall()
    con.close()
    return rows


def GetAll():
    con=lite.connect("batch.db")
    cur=con.cursor()
    cur.execute("SELECT * FROM bat")
    rows=cur.fetchall()
    con.close()
    return rows






def srst(rst): 
    # initializing data to be stored in db 
    
    master = {'rst' : rst}  
    # Its important to use binary mode 
    static = open('rst.dat', 'wb')
    # source, destination 
    pickle.dump(master, static)                      
    static.close()
    


def lrst(): 
    # for reading also binary mode is important 
    static = open('rst.dat', 'rb')
    db = pickle.load(static) 
    d = db.get("rst", "")
    data=int(d)
    static.close()
    return data


def splno(plno):
    # initializing data to be stored in db

    master = {'plno': plno}
    # Its important to use binary mode
    static = open('plno.dat', 'wb')
    # source, destination
    pickle.dump(master, static)
    static.close()


def lplno():
    # for reading also binary mode is important
    static = open('plno.dat', 'rb')
    db = pickle.load(static)
    d = db.get("plno", "")
    data = d
    static.close()
    return data




def ComData(Port, Baurd, Rfind, Dp, Filter):
    # initializing data to be stored in db

    master = {'Port': Port, 'Baurd': Baurd, 'Rfind': Rfind, 'Dp': Dp, 'Filter': Filter}
    # Its important to use binary mode
    static = open('com.dat', 'wb')
    # source, destination
    pickle.dump(master, static)
    static.close()


def loadCom():

    # for reading also binary mode is important
    static = open('com.dat', 'rb')
    dat = pickle.load(static)
    d0 = dat.get("Port","")
    d1 = dat.get("Baurd","")
    d2 = dat.get("Rfind","")
    d3 = dat.get("Dp","")
    d4 = dat.get("Filter","")
    data=[d0,d1,d2,d3,d4]
    static.close()
    return data


def reset():
    srst(1)
    splno(1)
    con = lite.connect("batch.db")
    cur = con.cursor()
    cur.execute('DELETE FROM bat')
    nrows = cur.rowcount
    con.commit()
    con.close()


    return nrows


def suid(uid):
    
    master = {'uid': uid}
    # Its important to use binary mode
    static = open('uid.dat', 'wb')
    # source, destination
    pickle.dump(master, static)
    static.close()


def luid():
    # for reading also binary mode is important
    static = open('uid.dat', 'rb')
    db = pickle.load(static)
    d = db.get("uid", "")
    data = d
    static.close()
    return data

def Lcheck():

    con=lite.connect("wb.db")
    cur=con.cursor()
    cur.execute(f"SELECT * FROM cclc WHERE ID = '1' ")
    row=cur.fetchone()
    con.close()
    MAC=row[1]
    Ldate=row[2]
    today=datetime.datetime.today()
    xdate=today.strftime("%d-%m-%Y")
    xdate = datetime.datetime.strptime(xdate, "%d-%m-%Y").date() if xdate else None
    Ldate = datetime.datetime.strptime(Ldate, "%d-%m-%Y").date() if Ldate else None
    cmac=str(get_mac_address())

    if xdate<Ldate and (MAC==cmac or MAC=="JAI SHREE RAM"):
        return 1
    else:
        return 0



def get_mac_address():
    try:
        # Get a list of network interfaces
        interfaces = psutil.net_if_addrs()

        # Find the MAC address of the first Ethernet (LAN) interface available
        for interface, addresses in interfaces.items():
            for address in addresses:
                if address.family == psutil.AF_LINK:
                    return address.address
    except psutil.Error:
        pass

    return None


def Update_lic():
    mac=str(get_mac_address())
    today=datetime.datetime.today()
    xdate=today.strftime("%d-%m-%Y")
    xdate = datetime.datetime.strptime(xdate, "%d-%m-%Y").date()

    one_year_later = xdate + datetime.timedelta(days=370)
    one_year_later_str = one_year_later.strftime("%d-%m-%Y")
    data=[mac,one_year_later_str]
    con=lite.connect("wb.db")
    cur=con.cursor()
    cur.execute("""UPDATE cclc SET MAC = ?, LDATE = ? WHERE ID = '1'""",data)
    con.commit()
    con.close()
    return data





def delid(idlist):
    con=lite.connect("batch.db")
    cur=con.cursor()

    for id in idlist:
        cur.execute("DELETE FROM bat WHERE id = ?", (id,))

    con.commit()
    con.close()







# splno(1)

# srst(1)
#wbData()
# wbfixDsata()
# x=None
# x=GetBatchData(1)
# wbbatchData()

# for x in range(0,10):
#     SaveBatching(700,1,'12', '22','12345')
