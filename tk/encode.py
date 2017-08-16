# coding=utf-8
"""
Script name: encode.py
Author: Trinh Do - 3D artist, leader DAMG team.

Description:
    This is the script to convert a string as input to hexadecimal as output
"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import unicodedata
from tk import defaultVariable as var

# ------------------------------------------------------
# DEFAULT VARIABLES
# ------------------------------------------------------
# example of a normal string (English, readable)
STRINPUT = var.STRINPUT
# example of a string in hexadecimal code
HEXINPUT = var.HEXINPUT
# list of keywords to run script by user
OPERATION = var.OPERATION['encode']

# ----------------------------------------------------------------------------------------------------------- #
"""                        MAIN CLASS: ENDCODE - ENCODE STRING TO HEXADECIMAL                               """
# ----------------------------------------------------------------------------------------------------------- #
class Encode():
    """
    This is the main class with function to encode a string to hexadecimal or revert.
    """
    def ascii(self, rawInput):
        """
        convert another type of unicode to be compatible in python
        :param rawInput: input
        :return: unicode string
        """
        outPut = unicodedata.normalize('NFKD', rawInput).encode('ascii', 'ignore').decode('ascii')

        return outPut

    def utf8(self, rawInput):
        outPut = rawInput.encode('utf-8')
        return outPut

    def typeToStr(self, rawInput):
        """
        convert to string
        :param rawInput: input which may not be a string type
        :return: string type input
        """
        if type(rawInput) is not 'string':
            rawStr = str(rawInput)
        else:
            rawStr = rawInput

        return rawStr

    def strToHex(self, strInput):
        """
        convert string to hexadecimal
        :param strInput: string input
        :return: hexadecimal
        """
        self.outPut = ''.join ( ["%02X" % ord (x) for x in strInput] )
        return self.outPut

    def hexToStr(self, hexInput):
        """
        convert a hexadecimal string to a string which could be readable
        :param hexInput: hexadecimal string
        :return: readable string
        """
        bytes = []
        hexStr = ''.join( hexInput.split(" ") )
        for i in range(0, len(hexStr), 2):
            bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

        self.outPut = ''.join( bytes )
        return self.outPut

# ------------------------------------------------------
# FUNCTION TO OPERATE THE ENCODING
# ------------------------------------------------------
def encode(input=STRINPUT, mode=OPERATION[0]):
    """
    Base on given mode it will tells script what to do
    :param input: type of input, string by default
    :param mode: given mode to convert string to hexadecimal or revert.
    :return: string
    """
    if mode == 'hex':
       output = Encode().strToHex( input )
    elif mode == 'str':
        output = Encode().hexToStr( input )
    elif mode== 'ascii':
        output = Encode().ascii( input )
    else:
        output = Encode().utf8(input)

    return output

# --------------------------------------------------------------------------------------------------------
"""                                                END OF CODE                                         """
# --------------------------------------------------------------------------------------------------------