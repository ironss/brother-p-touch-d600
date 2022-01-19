# Brother P-touch D600 Label Maker

This document details the USB communication trace between a Brother P-touch D600
label maker and the P-touch Editor program.

Upon startup, the program sends `1b 69 58 47`, which seems to be a system status
query command.

The printer responds with `71 02` which is 625 in little endian binary encoding.
This is the length of the next message which comes in 40 byte chunks with the
last one being less - not padded.

The message uses CRLF for newlines.

```ini
<<PRINTER CONFIGURATION>>
[Printer]
FormVer =1.00
Printer =PT-D600
PrintID =6430
SerialNo=D6Z608109
ProgVer =V1.01
BootVer =V1.00
FontVer =V1.00
ColorVer=V1.00
SymVer  =V1.00
EromVer =V0.010
PV      =        1,466
PN      =          202
LC      =            1
BC      =            0
FR      =            0
SB      =            5
NB      =            0
MR      =            0
LL      =            0
AF      =            0
CC      =          236

[Printer Settings]
Auto Power Off =480Minute(s)

[File Memory]
Available =2260char
Files     = 0/99

[Label Collection Memory]
Categories = 0/30

```

The program then sends `1B 69 53` and the printer responds with 32 bytes:

```hex
80 20 42 30 6a 30 00 00 00 00 09 01 00 00 00 00
00 00 00 00 00 00 00 00 01 08 00 00 00 00 00 00
```

| Offset | Size | Field               | Value      |
|--------|------|---------------------|------------|
| 0      | 1    | Print head mark     | `80` hex   |
| 1      | 1    | Size                | `20` hex   |
| 2      | 6    | Signature           | `BOjO\0\0` |
| 9      | 2    | Error               | TODO       |
| 11     | 1    | Media width         |
| 12     | 1    | Media height        |
| 13     | 5    | Reserved            | Zeroes
| 18     | 1    | Media length        |
| 19     | 1    | Status type         |
| 20     | 3    | Phase type          |
| 23     | 1    | Notification number |

Status types:

| Byte | Type                    |
|------|-------------------------|
| 0    | Reply to status request |
| 1    | Printing completed      |
| 2    | Error                   |
| 6    | Phase change            |

Error bits:

| Bit   | Error                    |
|-------|--------------------------|
| 0     | No media                 |
| 1     | End of media             |
| 2     | Tape cutter jam          | 
| 3-7   | Unused                   |
| 8     | Replace the media        |
| 9     | Expansion buffer full    |
| 10    | Transmission error       |
| 11    | Transmission buffer full |
| 12    | Cover open               |
| 13-15 | Unused                   |

## Commands

- `1B 40`: printer clear print buffer
- `1B 69 53`: status request
- `1B 69 58 47`: configuration request

## Important discoveries

- PT-D600 protocol seems to be similar to PT-P900.

- See https://download.brother.com/welcome/docp100407/cv_ptp900_eng_raster_101.pdf

- PT-D600 seems to accept only TIFF-encoded raster data. Or perhaps you have to configure things
  in a different order to get it to accept raw binary data.

- TIFF-encoding allows RLE-compression for repeated data, with a negative length byte

- TIFF-encoding allows for random (non-RLE) data, with a postivie length byte

- PT-D600 print-head seems to be 128 dots wide at 180 dpi, for a print width of 18 mm.

- PT-D600 print-head does not need 'empty' dots at the start of each raster line. The first byte
  of raster data is printed.

- Each line of raster data must give 128 dots, for a total of 16 bytes.

- Non-RLE data starts with the byte 16, then has the actual data bytes.

- When sending the raster-data packet, the number of bytes sent is 17 (length + 16 bytes of data)


## Additional Resources

http://www.undocprint.org/formats/page_description_languages/brother_p-touch

P-touch USB protocol description.

http://etc.nkadesign.com/uploads/Printers/95CRRASE.pdf

Documents the P-touch protocol.

https://github.com/cbdevnet/pt1230

Documents the P-touch communication when printing and crucially the format
the bitmap and linemap data are sent in.

https://github.com/furrtek/PTouchHH

Patches the printer on the controller level to replace firmware and then
the whole controller.

https://github.com/EtherGraf/ptouch-print, forks and copies

Copies:

- https://github.com/clarkewd/ptouch-print
- https://github.com/Nihlus/ptouch-print

https://apz.fi/blabel/
