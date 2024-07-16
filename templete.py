import db_pg as db
import pickle


      
def gettkt(wt):
    


    itrow=[]
    itrow=db.loadData()
    
    # print (itrow)
    Party=itrow[0]
    Variety=itrow[1]
    CoreWt=format(float(itrow[2]),".3f")
    TareWt=format(float(itrow[3]),".3f")
    xdate=itrow[4]
    RollNo=db.lrst(Variety)



    weight=str(format(round(float(wt),2),".3f"))
    SubWt=float(CoreWt)+float(TareWt)
    NetWt=format(round((float(wt)-float(SubWt)),2),".3f")
    SaveData(Party, Variety, weight, CoreWt, TareWt, NetWt, RollNo,xdate)



def SaveData(Party, Variety,weight, CoreWt, TareWt, NetWt, RollNo,xdate):
    # initializing data to be stored in db

    master = {'Party': Party.strip('\n'), 'Variety': Variety.strip('\n'),'weight':weight, 'CoreWt': CoreWt, 'TareWt': TareWt ,'NetWt': NetWt,
              'RollNo': RollNo,'xdate':xdate}
    # Its important to use binary mode
    static = open('out.dat', 'wb')
    # source, destination
    pickle.dump(master, static)
    static.close()


def loadData():
    # for reading also binary mode is important
    static = open('out.dat', 'rb')
    dat = pickle.load(static)
    d0 = dat.get("Party", "")
    d1 = dat.get("Variety", "")
    d2 = dat.get("weight", "")
    d3 = dat.get("CoreWt", "")
    d4 = dat.get("TareWt", "")
    d5 = dat.get("NetWt", "")
    d6 = dat.get("RollNo", "")
    d7 = dat.get("xdate", "")
    data = [d0, d1, d2, d3, d4,d5,d6,d7]
    static.close()
    return data






