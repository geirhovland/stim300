import serial
import struct
from binascii import crc32

def stim300_print(label,x,y,z,status):
    if status == 0:
        print("{} {} {} {}".format(label,x,y,z))
    else:
        print("{} Status byte not OK".format(label))

def stim300_datagram(s):
    N = 64  # Assumes full datagram: rate,acc,incl,temp,aux terminated by CR/LF
    CR = 13 # Carriage Return
    LF = 10 # Linefeed
    bRead = False
    while not bRead:
        y = b''
        while y != b'\xaf': # Wait for Normal Mode Full Datagram
            y = s.read()
        x = s.read(N)
        if (x[N-2] == CR) and (x[N-1] == LF): # Check Termination
            bRead = True

    out = [0] * 31 # Initialize array
    # Rate (Gyro) X,Y,Z,Status
    out[0] = int.from_bytes(x[0:3], 'big', signed="True") / 16384
    out[1] = int.from_bytes(x[3:6], 'big', signed="True") / 16384
    out[2] = int.from_bytes(x[6:9], 'big', signed="True") / 16384
    out[3] = x[9] # Status Byte
    # Acc X,Y,Z,Status Assumes range 10g --> 2^19 = 524288
    out[4] = int.from_bytes(x[10:13], 'big', signed="True") / 524288
    out[5] = int.from_bytes(x[13:16], 'big', signed="True") / 524288
    out[6] = int.from_bytes(x[16:19], 'big', signed="True") / 524288
    out[7] = x[19] # Status Byte
    # Incl X,Y,Z,Status. 2^22 = 4194304
    out[8] = int.from_bytes(x[20:23], 'big', signed="True") / 4194304
    out[9] = int.from_bytes(x[23:26], 'big', signed="True") / 4194304
    out[10] = int.from_bytes(x[26:29], 'big', signed="True") / 4194304
    out[11] = x[29] # Status Byte
    # Gyro Temp X,Y,Z,Status. 2^8 = 256
    out[12] = int.from_bytes(x[30:32], 'big', signed="True") / 256
    out[13] = int.from_bytes(x[32:34], 'big', signed="True") / 256
    out[14] = int.from_bytes(x[34:36], 'big', signed="True") / 256
    out[15] = x[36] # Status Byte
    # Acc Temp X,Y,Z,Status. 2^8 = 256
    out[16] = int.from_bytes(x[37:39], 'big', signed="True") / 256
    out[17] = int.from_bytes(x[39:41], 'big', signed="True") / 256
    out[18] = int.from_bytes(x[41:43], 'big', signed="True") / 256
    out[19] = x[43] # Status Byte
    # Incl Temp X,Y,Z,Status. 2^8 = 256
    out[20] = int.from_bytes(x[44:46], 'big', signed="True") / 256
    out[21] = int.from_bytes(x[46:48], 'big', signed="True") / 256
    out[22] = int.from_bytes(x[48:50], 'big', signed="True") / 256
    out[23] = x[50] # Status Byte
    # AUX Output (External signal, if any)
    out[24] = x[51] # Aux Byte 1
    out[25] = x[52] # Aux Byte 2
    out[26] = x[53] # Aux Byte 3
    out[27] = x[54] # Status Byte
    # Counter, Latency and CRC
    out[28] = x[55] # Counter [0-255]
    out[29] = int.from_bytes(x[56:58], 'big') # Latency (microseconds)
    out[30] = int.from_bytes(x[58:62], 'big') # Checksum (CRC)
    return(out)

if __name__ == "__main__":
    s = serial.Serial('COM5', baudrate=115200, timeout=10)
    x = stim300_datagram(s)
    print("Received datagram from STIM300:")
    stim300_print("Gyro X,Y,Z (deg/s):",x[0],x[1],x[2],x[3])
    stim300_print("Acc  X,Y,Z (g)    :",x[4],x[5],x[6],x[7])
    stim300_print("Incl X,Y,Z (g)    :",x[8],x[9],x[10],x[11])
    stim300_print("Gyro Temp (deg C) :",x[12],x[13],x[14],x[15])
    stim300_print("Acc  Temp (deg C) :",x[16],x[17],x[18],x[19])
    stim300_print("Incl Temp (deg C) :",x[20],x[21],x[22],x[23])
    stim300_print("AUX Data          :",x[24],x[25],x[26],x[27])
    print("Counter [0-255]   : {}".format(x[28]))
    print("Latency (us)      : {}".format(x[29]))
    print("CRC32             : {}".format(x[30]))
    s.close()
