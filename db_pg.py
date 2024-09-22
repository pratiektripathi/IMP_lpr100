import sqlite3 as lite
import pickle
import psutil
import datetime
import psycopg2 as pg
import json
import requests


parms=json.load(open('db_parms.json'))

    
def getfix():

    con=lite.connect("wb.db")
    cur=con.cursor()
    cur.execute("""SELECT * FROM "fix" WHERE id=1 """)
    row=cur.fetchone()
    con.close()
    return row



def UpdatefixData(f1,f1fs,x1,y1,f2,f2fs,x2,y2,f3,f3fs,x3,y3,f4,f4fs,x4,y4,f5,f5fs,x5,y5,f6,f6fs,x6,y6,f7,f7fs,x7,y7,f8,f8fs,x8,y8,f9,f9fs,x9,y9,f10,f10fs,x10,y10,b,bfs,bcode,barx,bary):

    
    con=lite.connect("wb.db")
    cur=con.cursor()
    cur.execute("""UPDATE fix SET f1=:f1, f1fs=:f1fs, x1=:x1, y1=:y1, f2=:f2, f2fs=:f2fs, x2=:x2, y2=:y2, f3=:f3, f3fs=:f3fs, x3=:x3, y3=:y3, f4=:f4, f4fs=:f4fs, x4=:x4, y4=:y4, f5=:f5, f5fs=:f5fs, x5=:x5, y5=:y5,f6=:f6, f6fs=:f6fs, x6=:x6, y6=:y6, f7=:f7, f7fs=:f7fs, x7=:x7, y7=:y7, f8=:f8, f8fs=:f8fs, x8=:x8, y8=:y8, f9=:f9, f9fs=:f9fs, x9=:x9, y9=:y9, f10=:f10, f10fs=:f10fs, x10=:x10, y10=:y10, b=:b, bfs=:bfs, bcode=:bcode ,barx=:barx, bary=:bary WHERE id=1""",{'f1':f1,'f1fs':f1fs,'x1':x1,'y1':y1,'f2':f2,'f2fs':f2fs,'x2':x2,'y2':y2,'f3':f3,'f3fs':f3fs,'x3':x3,'y3':y3,'f4':f4,'f4fs':f4fs,'x4':x4,'y4':y4,'f5':f5,'f5fs':f5fs,'x5':x5,'y5':y5,'f6':f6,'f6fs':f6fs,'x6':x6,'y6':y6,'f7':f7,'f7fs':f7fs,'x7':x7,'y7':y7,'f8':f8,'f8fs':f8fs,'x8':x8,'y8':y8,'f9':f9,'f9fs':f9fs,'x9':x9,'y9':y9,'f10':f10,'f10fs':f10fs,'x10':x10,'y10':y10,'b':b,'bfs':bfs,'bcode':bcode,'barx':barx,'bary':bary })
    con.commit()
    con.close()



def SaveData(Party,Variety,CoreWt,TareWt,Date):
   
    # initializing data to be stored in db 
    
    master = {'Party':Party.strip('\n'),'Variety':Variety.strip('\n'),'CoreWt':CoreWt,'TareWt':TareWt,'Date':Date}
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
    d4 = dat.get("Date", "")
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
    con=pg.connect(**parms)
    cur=con.cursor()
    cur.execute('''SELECT "Variety_id" FROM "Variety" WHERE "Variety" = %s ;''',(Variety,))
    result=cur.fetchone()
    Variety_id=result[0]
    cur.execute('''INSERT INTO bat ("LotNo","RollNo","Party","Variety_id","GrossWt","TareWt","CoreWt","NetWt","Date","Status") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ;''',(LotNo,RollNo,Party, Variety_id,GrossWt, TareWt,CoreWt, NetWt,Date,Status,))
    con.commit()
    con.close()




def GetBatchData(LotNo):
    con=pg.connect(**parms)
    cur=con.cursor()
    cur.execute('''SELECT "LotNo","RollNo","Party","Variety","GrossWt","TareWt","CoreWt","NetWt","Date","Status" FROM bat WHERE "LotNo" = %s ;''',(LotNo,))
    rows=cur.fetchall()
    con.close()
    return rows


def GetAll():
    con=pg.connect(**parms)
    cur=con.cursor()
    cur.execute('''SELECT "id","LotNo","RollNo","Party","Variety","GrossWt","TareWt","CoreWt","NetWt","Date","Status"
                FROM bat 
                INNER JOIN "Variety" 
                ON "Variety"."Variety_id" = "bat"."Variety_id" 
                ORDER BY "id" ASC''')
    rows=cur.fetchall()
    con.close()
    return rows




def GetFromDate(start,end):
    con=pg.connect(**parms)
    cur=con.cursor()
    cur.execute('''SELECT "id","LotNo","RollNo","Party","Variety","GrossWt","TareWt","CoreWt","NetWt","Date","Status"
                FROM bat INNER JOIN "Variety" 
                ON "Variety"."Variety_id" = "bat"."Variety_id" 
                WHERE "Date" BETWEEN %s AND %s
                ORDER BY "id" ASC''',(start,end))
    rows=cur.fetchall()
    con.close()
    return rows



def GetAllCount():
    con=pg.connect(**parms)
    cur=con.cursor()
    cur.execute("SELECT COUNT(*) FROM bat")
    rows=cur.fetchone()
    con.close()
    return rows



def srst(Variety,rst): 
    # initializing data to be stored in db 
    con=pg.connect(**parms)
    cur=con.cursor()
    cur.execute('''UPDATE "Variety" SET "Last_RollNo" = %s WHERE "Variety" = %s ;''',(rst,Variety,))
    con.commit()
    con.close()

    


def lrst(Variety):
    con=pg.connect(**parms)
    cur=con.cursor()
    cur.execute('''SELECT "Last_RollNo" FROM "Variety" WHERE "Variety" = %s ;''',(Variety,))
    rollNo=cur.fetchone()
    con.commit()
    con.close()
    return rollNo[0]
    # for reading also binary mode is important 


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
    
    splno(1)
    con = pg.connect(**parms)
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
    con=pg.connect(**parms)
    cur=con.cursor()

    for id in idlist:
        cur.execute("DELETE FROM bat WHERE id = %s", (id,))

    con.commit()
    con.close()



#--------------------Variety------------------

def saveVariety(Variety,Last_RollNo):
    con=pg.connect(**parms)
    cur=con.cursor()
    cur.execute('''INSERT INTO "Variety" ("Variety","Last_RollNo") VALUES (%s,%s) ;''',(Variety,Last_RollNo,))
    con.commit()
    con.close()


def loadVariety():
    con=pg.connect(**parms)
    cur=con.cursor()
    cur.execute('''SELECT * FROM "Variety" ORDER BY "Variety_id" ASC;''')
    rows=cur.fetchall()
    con.close()
    return rows

def update_Variety(id,Variety,Last_RollNo):
    con=pg.connect(**parms)
    cur=con.cursor()
    cur.execute('''UPDATE "Variety" SET "Variety" = %s, "Last_RollNo" = %s WHERE "Variety_id" = %s ;''',(Variety,Last_RollNo,id,))
    con.commit()
    con.close()


# ==================update report==================================


def update_status(ids):
    con=pg.connect(**parms)
    cur=con.cursor()
    for id in ids:       
        cur.execute("""UPDATE bat SET "Status" = %s WHERE "id" = %s""",("Done",id,))   

    con.commit()
    con.close()


    # ==================update check==================================

def update_check():
    url = "https://raw.githubusercontent.com/pratiektripathi/lpr100exe/main/version.json"
    old=json.load(open('version.json'))
    try:
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON content
            content = response.content.decode('utf-8')
            version_info = json.loads(content)
            if old['version']<version_info['version']:
                return True
        else:
            return False
    
    except:
        return False
