# RSA_Read.py - RSA Device Memory Read
#  Author: Taylor JL Whitaker - SmartES Lab
#  Date: 13 June 2017

#  This file is made to read device memory for BasicRSA IPs from Trust-Hub.org
#   utilized for trojan evaluations with embedded linux applications.

#  RSA Device Memory (Eight 32 bit registers, 28 bytes used)
#    [0] Reset     (0)
#    [1] SWReady   (0)
#    [2] Exponent  (31 downto 0)
#    [3] Modulus   (31 downto 0)
#    [4] DataIn    (31 downto 0)
#    [5] HWReady   (0)
#    [6] DataOut   (31 downto 0)
#    [8] Empty


# Main
with open('/dev/rsa', 'r+b') as f:

    # Read device state
    NoPrint = f.seek(0,0)
    registers = f.read(28)
    print('Reset\t\t' + str(int.from_bytes(registers[0:4], byteorder='little')))
    print('SWReady\t\t' + str(int.from_bytes(registers[4:8], byteorder='little')))
    print('Exponent\t' + str(int.from_bytes(registers[8:12], byteorder='little')))
    print('Modulus\t\t' + str(int.from_bytes(registers[12:16], byteorder='little')))
    print('DataIn\t\t' + str(int.from_bytes(registers[16:20], byteorder='little')))
    print('HWReady\t\t' + str(int.from_bytes(registers[20:24], byteorder='little')))
    print('DataOut\t\t' + str(int.from_bytes(registers[24:28], byteorder='little')))

    # Release file
    f.close()
