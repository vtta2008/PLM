def check_charge( charged, printer ):

    "Checks if user declared the molecule as charged by typing charged somewhere behind the plugin call If so the user is prompted to supply the charge. And reading it in"

    ### Checking if molecule is charged and reading in the charge if  the argument charged is given.
    ### If so the user is prompted to supply the charge
    if charged:
       userinput=printer.ask('What is the charge of your molecule? (Eg.> +1, 2 or -2)')
       printer('\n So your molecule has a charge of {}.'.format(userinput))
       return(float(userinput))
    else:
       printer('\nThe following procedure is suited for molecules that are neutral.\n' \
            "In case your molecule is charged, \nplease write behind the resp option the keyword 'charged'.")
       return(0.0)

    #return [returnvalue]

def check_charges(j, atomcounts, charged, printer ):

    "Checks if user declared the molecule as charged by typing charged somewhere behind the plugin call If so the user is prompted to supply the charge. And reading it in"

    ### Checking if molecule is charged and reading in the charge if  the argument charged is given.
    ### If so the user is prompted to supply the charge
    if charged:
       printer('\nWhat is the charge of molecule number {}, which has {} atoms.'.format(j, atomcounts[j]))
       userinput=printer.ask('Please enter in format +1, 2 or -2')
       printer('The charge of the molecule is set to {}.'.format(userinput))
       return(float(userinput))
    else:
       printer('\nThe following procedure is suited for molecules that are neutral.\n' \
            "In case your molecule is charged, \nplease write behind the resp option the keyword 'charged'.")
       return(0.0)



def build_resp_arrays( atom, resp_arrays, chargedict ):

    #------- alternative invarioms block
    if atom.invarioms.keys()[0] in list(chargedict.keys()):
        resp = chargedict[atom.invarioms.keys()[0]]
        resp_arrays[atom.molecule_id].append(resp)
        atom.set_active_invariom(atom.invarioms.keys()[0])

    else:
        if 1 < len(atom.invarioms.keys()):
            if atom.invarioms.keys()[1] in list(chargedict.keys()):
                resp = chargedict[atom.invarioms.keys()[1]]
                resp_arrays[atom.molecule_id].append(resp)
                atom.set_active_invariom(atom.invarioms.keys()[1])
            else:
                if 2 < len(atom.invarioms.keys()):
                    if atom.invarioms.keys()[2] in list(chargedict.keys()):
                        resp = chargedict[atom.invarioms.keys()[2]]
                        resp_arrays[atom.molecule_id].append(resp)
                        atom.set_active_invariom(atom.invarioms.keys()[2])
                    else: print 'PROBLEM: Found no match for invarioms,', atom.invarioms.keys()[0], atom.invarioms.keys()[1], atom.invarioms.keys()[2], ' of atom ', atom.name, "in charge database."
                else: print 'PROBLEM: Found no match for invarioms ', atom.invarioms.keys()[0],atom.invarioms.keys()[1],' of atom ', atom.name, "in charge database."
        else: print'PROBLEM: FOUND no match for invariom of atom ', atom.invarioms.keys()[0], "in charge database."
    #--------- end of alternative invarioms block

#class resp_arrays:
#    def __init__(self):
#        self.mol_id = 0
#        self.resp_array = {}