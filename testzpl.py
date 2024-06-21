from simple_zpl2 import ZPLDocument, QR_Barcode
import db
import sys
import win32print
import random

def gensample():

    PrinterName = "TSC TE200"
    brands=["Deepali","Shatabdi"]
    size=["12x1","15x2","18x3","21x4","24x5","27x6","30x7","33x8","36x9","39x10","42x1"]
    color=["Black","White","Red","Blue","Green","Yellow","Orange","Pink","Purple","Brown","Grey","Cyan"]
    weight=["20.85","27.26","33.68","40.1","46.52","52.94","59.36","65.78","72.2","78.62","85.04","91.46","97.8"]
    zdoc = ZPLDocument()

    zdoc.add_comment("Barcode and text")
    zdoc.add_field_origin(50, 50)
    code128_data = f"***{random.randint(1,99999999)}*{random.choice(brands)}*{random.choice(size)}*{random.choice(color)}*{random.choice(weight)}*"
    bc = QR_Barcode(code128_data, 1,5, 'M')
    zdoc.add_barcode(bc)

    zdoc.add_comment("Barcode and text")
    zdoc.add_field_origin(50, 250)
    code128_data = f"***{random.randint(1,99999999)}*{random.choice(brands)}*{random.choice(size)}*{random.choice(color)}*{random.choice(weight)}*"
    bc = QR_Barcode(code128_data, 1,5, 'M')
    zdoc.add_barcode(bc)

    zdoc.add_comment("Barcode and text")
    zdoc.add_field_origin(250, 50)
    code128_data = f"***{random.randint(1,99999999)}*{random.choice(brands)}*{random.choice(size)}*{random.choice(color)}*{random.choice(weight)}*"
    bc = QR_Barcode(code128_data, 1,5, 'M')
    zdoc.add_barcode(bc)

    zdoc.add_comment("Barcode and text")
    zdoc.add_field_origin(250, 250)
    code128_data = f"***{random.randint(1,99999999)}*{random.choice(brands)}*{random.choice(size)}*{random.choice(color)}*{random.choice(weight)}*"
    bc = QR_Barcode(code128_data, 1,5, 'M')
    zdoc.add_barcode(bc)


    zdoc.add_comment("Barcode and text")
    zdoc.add_field_origin(500, 50)
    code128_data = f"***{random.randint(1,99999999)}*{random.choice(brands)}*{random.choice(size)}*{random.choice(color)}*{random.choice(weight)}*"
    bc = QR_Barcode(code128_data, 1,5, 'M')
    zdoc.add_barcode(bc)

    zdoc.add_comment("Barcode and text")
    zdoc.add_field_origin(500, 250)
    code128_data = f"***{random.randint(1,99999999)}*{random.choice(brands)}*{random.choice(size)}*{random.choice(color)}*{random.choice(weight)}*"
    bc = QR_Barcode(code128_data, 1,5, 'M')
    zdoc.add_barcode(bc)

    message = zdoc.zpl_text

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
            
                win32print.WritePrinter(hprinter, raw_data)
            

                win32print.EndPagePrinter(hprinter)
            finally:
                win32print.EndDocPrinter(hprinter)
        finally:
            win32print.ClosePrinter(hprinter)


for i in range(10):
    gensample()