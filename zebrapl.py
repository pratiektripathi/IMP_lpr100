from simple_zpl2 import ZPLDocument, Code128_Barcode, QR_Barcode
import db_pg as db
import sys
import win32print
from datetime import datetime



def zeepl(wt):
    itrow = db.loadData()

    plno = db.lplno()
    Party = itrow[0]
    Variety = itrow[1]
    RollNo = int(db.lrst(Variety))
    CoreWt = itrow[2]
    TareWt = itrow[3]
    xdate = itrow[4]
    mac_id = itrow[5]
  
    Variety_id = itrow[6]
    party_id = itrow[7]
    tktno = db.loadtktno()
    current_date = datetime.now()
    current_date_str = current_date.strftime("%Y-%m-%d")

    weight = str(format(round(float(wt), 2), ".3f"))
    SubWt = float(CoreWt) + float(TareWt)
    NetWt = format(round((float(wt) - float(SubWt)), 2), ".3f")

    PrintData = db.loadPrint()
    PrinterName = PrintData[0].strip("\n")
    Copy = int(PrintData[1].strip("\n"))

    stats = {'$Party': Party, '$Variety': Variety, '$CoreWt': CoreWt, '$TareWt': TareWt, '$GWt': weight,
             '$NetWt': NetWt, '$RollNo': RollNo, '$xdate': xdate, '$plno':plno,'$macid':mac_id,'$partyid':party_id,'$varid':Variety_id,'$tktno':tktno}
    fixrow = []
    fixrow = db.getfix()

    logodata=db.loadLogo()
    logo=logodata[0].strip("\n")
    lx = int(logodata[1].strip("\n"))
    ly = int(logodata[2].strip("\n"))



    #     print(fixrow)
    f1 = fixrow[1].format(**stats)

    f1s = int(fixrow[2])
    x1 = int(fixrow[3])
    y1 = int(fixrow[4])
    f2 = fixrow[5].format(**stats)
    f2s = int(fixrow[6])
    x2 = int(fixrow[7])
    y2 = int(fixrow[8])
    f3 = fixrow[9].format(**stats)
    f3s = int(fixrow[10])
    x3 = int(fixrow[11])
    y3 = int(fixrow[12])

    f4 = fixrow[13].format(**stats)
    f4s = int(fixrow[14])
    x4 = int(fixrow[15])
    y4 = int(fixrow[16])
    f5 = fixrow[17].format(**stats)
    f5s = int(fixrow[18])
    x5 = int(fixrow[19])
    y5 = int(fixrow[20])

    f6 = fixrow[21].format(**stats)

    f6s = int(fixrow[22])
    x6 = int(fixrow[23])
    y6 = int(fixrow[24])
    f7 = fixrow[25].format(**stats)
    f7s = int(fixrow[26])
    x7 = int(fixrow[27])
    y7 = int(fixrow[28])
    f8 = fixrow[29].format(**stats)
    f8s = int(fixrow[30])
    x8 = int(fixrow[31])
    y8 = int(fixrow[32])
    f9 = fixrow[33].format(**stats)
    f9s = int(fixrow[34])
    x9 = int(fixrow[35])
    y9 = int(fixrow[36])
    f10 = fixrow[37].format(**stats)
    f10s = int(fixrow[38])
    x10 = int(fixrow[39])
    y10 = int(fixrow[40])

    bar = fixrow[41].format(**stats)
    bars = int(fixrow[42])
    baro = fixrow[43]
    barx = int(fixrow[44])
    bary = int(fixrow[45])

    barcode = bar

    zdoc = ZPLDocument()

    zdoc.add_comment('Now some text')
    zdoc.add_field_origin(lx, ly)
    zdoc.add_font('0', zdoc._ORIENTATION_NORMAL, f1s)
    zdoc.add_field_data(logo)

    zdoc.add_comment('Now some text')
    zdoc.add_field_origin(x1, y1)
    zdoc.add_font('0', zdoc._ORIENTATION_NORMAL, f1s)
    zdoc.add_field_data(f1)

    zdoc.add_comment('Now some text')
    zdoc.add_field_origin(x2, y2)
    zdoc.add_font('0', zdoc._ORIENTATION_NORMAL, f2s)
    zdoc.add_field_data(f2)

    zdoc.add_comment('Now some text')
    zdoc.add_field_origin(x3, y3)
    zdoc.add_font('0', zdoc._ORIENTATION_NORMAL, f3s)
    zdoc.add_field_data(f3)

    zdoc.add_comment('Now some text')
    zdoc.add_field_origin(x4, y4)
    zdoc.add_font('0', zdoc._ORIENTATION_NORMAL, f4s)
    zdoc.add_field_data(f4)

    zdoc.add_comment('Now some text')
    zdoc.add_field_origin(x5, y5)
    zdoc.add_font('0', zdoc._ORIENTATION_NORMAL, f5s)
    zdoc.add_field_data(f5)

    zdoc.add_comment('Now some text')
    zdoc.add_field_origin(x6, y6)
    zdoc.add_font('0', zdoc._ORIENTATION_NORMAL, f6s)
    zdoc.add_field_data(f6)

    zdoc.add_comment('Now some text')
    zdoc.add_field_origin(x7, y7)
    zdoc.add_font('0', zdoc._ORIENTATION_NORMAL, f7s)
    zdoc.add_field_data(f7)

    zdoc.add_comment('Now some text')
    zdoc.add_field_origin(x8, y8)
    zdoc.add_font('0', zdoc._ORIENTATION_NORMAL, f8s)
    zdoc.add_field_data(f8)

    zdoc.add_comment('Now some text')
    zdoc.add_field_origin(x9, y9)
    zdoc.add_font('0', zdoc._ORIENTATION_NORMAL, f9s)
    zdoc.add_field_block(450,2,0,'L',0)
    zdoc.add_field_data(f9)

    zdoc.add_comment('Now some text')
    zdoc.add_field_origin(x10, y10)
    zdoc.add_font('0', zdoc._ORIENTATION_NORMAL, f10s)
    zdoc.add_field_block(140, 1, 0, 'C', 0)
    zdoc.add_field_data(f10)

    if baro == 'Y':
        zdoc.add_comment("Barcode and text")
        zdoc.add_field_origin(barx, bary)
        code128_data = barcode
        bc = QR_Barcode(code128_data, 2,bars, 'M')
        zdoc.add_barcode(bc)
    else:
        pass



    message = zdoc.zpl_text
    f = open('zebra.zpl', 'w')
    f.write(message)
    f.close()

    if sys.version_info >= (3,):
        raw_data = bytes(message, "utf-8")
    else:
        raw_data = message
   
    if len(PrinterName) != 0:
        hprinter = win32print.OpenPrinter(PrinterName)
        try:
            win32print.StartDocPrinter(hprinter, 1, ("ticket", None, "RAW"))
            try:
                win32print.StartPagePrinter(hprinter)
                for i in range(0, Copy):
                    win32print.WritePrinter(hprinter, raw_data)
                db.SaveBatching(plno,RollNo, party_id, Variety_id,  weight,  TareWt,CoreWt, NetWt,current_date_str,"Pending",mac_id,barcode)
                db.tktno(int(tktno)+1)
                
# LotNo,RollNo,Party, Variety,GrossWt, TareWt,CoreWt, NetWt,Date,Status
                win32print.EndPagePrinter(hprinter)
            finally:
                win32print.EndDocPrinter(hprinter)
        finally:
            win32print.ClosePrinter(hprinter)



    db.srst(Variety,int(RollNo + 1))


