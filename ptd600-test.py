import binascii
import sys

# Resolution   Tape width  Print width   Offset
# dpi          mm  px      mm  px        mm  px
# 180          24  170     18  128       3   21
# 360          24  340


data = bytes.fromhex(

    # Invalidate
    "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
    "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
    "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
    "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
    "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
    "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
    "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
    "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
    
    "1B 40"         # ESC @     Initialise
    
    "1B 69 53"      # ESC i S   Request status info
    
    "1B 69 4D 40"   # ESC i M   Mode setting
                    #           40 autocut
                    #           80 mirror printing
               
                    
    "1B 69 4B 08"   # ESC i B   Advanced mode setting
                    #           01 draft
                    #           02 unused
                    #           04 half-cut
                    #           08 chain printing
                    #           10 special tape
                    #           20 unused
                    #           40 hi-res printing
                    #           80 no buffer clearing

    "1B 69 64 24 00" # ESC i d  Specify margin as 0023 = 36 dots ~ 5 mm
        
    #"1B 69 52 01"   # ESC i R   Select raster-graphics mode
                    #           Not documented in PT9700 docu, but used by many implementations
                    #           PT-9700 seems to use  ESC i a 01
    
    "1B 69 61 01"   # ESC i a   Switch dynamic command mode
                    #           00 ESC/P mode
                    #           01 Raster mode
                    #           02 P-touch template mode

    "4D 02"         # M         Select compression mode - TIFF

    "47 11 00   0F   FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF"
    "47 11 00   0F   00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF"
    "47 11 00   10   FF 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF"
    "47 11 00   10   FF FF 00 FF FF FF FF FF FF FF FF FF FF FF FF FF"
    "47 11 00   10   FF FF FF 00 FF FF FF FF FF FF FF FF FF FF FF FF"
    "47 11 00   10   FF FF FF FF 00 FF FF FF FF FF FF FF FF FF FF FF"
    "47 11 00   10   FF FF FF FF FF 00 FF FF FF FF FF FF FF FF FF FF"
    "47 11 00   10   FF FF FF FF FF FF 00 FF FF FF FF FF FF FF FF FF"
    "47 11 00   10   FF FF FF FF FF FF FF 00 FF FF FF FF FF FF FF FF"
    "47 11 00   10   FF FF FF FF FF FF FF FF 00 FF FF FF FF FF FF FF"
    "47 11 00   10   FF FF FF FF FF FF FF FF FF 00 FF FF FF FF FF FF"
    "47 11 00   10   FF FF FF FF FF FF FF FF FF FF 00 FF FF FF FF FF"
    "47 11 00   10   FF FF FF FF FF FF FF FF FF FF FF 00 FF FF FF FF"
    "47 11 00   10   FF FF FF FF FF FF FF FF FF FF FF FF 00 FF FF FF"
    "47 11 00   10   FF FF FF FF FF FF FF FF FF FF FF FF FF 00 FF FF"
    "47 11 00   10   FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 FF"
    "47 11 00   10   FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00"
    "47 11 00   10   FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF"

    #"5A"
    "1A"
)


status_labels = [
    'header',
    'size',
    'brother',
    'series',
    'model',
    'country',
    'battery',
    'extended',
    'error1',
    'error2',
    'media_width',
    'media_type',
    'colours',
    'fonts',
    'japanese_fonts',
    'mode',
    'density',
    'media_length',
    'status_type',
    'phase_type',
    'phase_number MSB',
    'phase_number LSB',
    'notification_number',
    'expansion',
    'tape colour',
    'text colour',
]

status_offsets = { status_labels[l]: l for l in range(len(status_labels)) }

with open('/dev/usb/lp4', 'wb') as f:
    f.write(data)

with open('/dev/usb/lp4', 'rb') as f:
    while(True):
        status = f.read(32)
        
        if (status):
            for i in range(len(status_labels)):
                label = status_labels[i]
                value = status[i]
                print(i, label, value, hex(value))
            print()
            
            if status[status_offsets['status_type']] == 6 and status[status_offsets['phase_type']] == 0:
                break

