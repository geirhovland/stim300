# stim300

Python code to read the STIM300 sensor over RS422.

Example output:

Received datagram from STIM300:  
Gyro X,Y,Z (deg/s): 0.017822265625 -0.0806884765625 0.05242919921875  
Acc  X,Y,Z (g)    : -0.011890411376953125 -0.016986846923828125 1.0138282775878906  
Incl X,Y,Z (g)    : -0.007907867431640625 -0.01989459991455078 0.999640703201294  
Gyro Temp (deg C) : 35.625 35.75 35.625  
Acc  Temp (deg C) : 35.09765625 35.0390625 35.109375  
Incl Temp (deg C) : 35.58203125 35.7109375 35.58203125  
AUX Data          : 255 239 2  
Counter [0-255]   : 225  
Latency (us)      : 506  
CRC32             : 3326689990  

In this example the RedCOM USB-COMi - USB to RS422/RS485 was used. The RS422 cable from SensoNor was used, but the two signals RX+ and RX- had to be swapped as shown in the image. Since only data is received from the sensor in Normal Mode, only the two RX signals are needed. The size of the datagram (Rate,Acc,Incl,Temp,AUX) and the baud rate on the sensor was set to 115,200 bits/s using the USB cable from SensoNor and the Windows application "STIM300_Evaluation Kit".

![RedCom USB-RS422 adater](https://raw.githubusercontent.com/geirhovland/stim300/main/STIM300_RS422.jpg)
