##############################################
#	Author data file for the invcif module   #
##############################################
"""
The names of the defined variables can be used to access
the corresponding author data via the cmdline.

To add a new author make a copy of the dummy variable and
edit the strings at the marked points.
"""

def get(name):
    return globals()[name]




jluebben=['\'Jens L\\"ubben\'',
          '\n;\nInstitute of Inorganic Chemistry,\nGeorg-August-University G\\"ottingen, Tammanstr. 4,\nD-37077 G\\"ottingen, Germany.\n;']
bdittrich=['\'Birger Dittrich\'',
           '\n;\nInstitute of Inorganic Chemistry,\nGeorg-August-University G\\"ottingen, Tammanstr. 4,\nD-37077 G\\"ottingen, Germany.\n;']
corben=['\'Claudia Orben\'',
        '\n;\nInstitute of Inorganic Chemistry,\nGeorg-August-University G\\"ottingen, Tammanstr. 4,\nD-37077 G\\"ottingen, Germany.\n;']

dummy=['\'\''
       '  Enter Name Here   '
       '\'',
       '\n;\n'
       '     Enter Adress Here       '
       '\n;']