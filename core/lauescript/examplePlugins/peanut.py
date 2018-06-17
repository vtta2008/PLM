__author__ = 'jens'

from lauescript.cryst.crystgeom import Uiso
from lauescript.cryst.transformations import cart2frac_ADP
from lauescript.laueio.loader import Loader

KEY = 'peanut'  # Edit this to control which cmd line keyword starts the plugin.
OPTION_ARGUMENTS = {'load': 'myFile.txt',
                    'use': 'cart_meas'}  # Edit this to define cmd line options for
# the plugin and their default values.


def run(pluginManager):
    """
    This is the entry point for the plugin manager.
    The plugin manager will pass a reference to itself
    to the function.
    Use the APD_Printer instance returned by
    pluginManager.setup() instead of the 'print'
    statement to generate autoformated cmd line output.
    :param pluginManager: Reference to the plugin manager
    instance.
    """
    printer = pluginManager.setup()
    data = pluginManager.get_variable('data')
    cell = data['exp'].get_cell()
    filecontent = ''
    filecontent += 'TITLE\n' \
                   '*   *  X-Ray*\n' \
                   '\n' \
                   'TITLE\n' \
                   '*\n' \
                   'COMMENTS\n' \
                   ' EXPT     Please insert comment here.\n' \
                   ' EXPT     Model to compare:\n' \
                   ' EXPT     Referecne Model:\n' \
                   '*EOS\n' \
                   '\n' \
                   'CELL DIMENSION  A         B         C       ALPHA     BETA      GAMMA    Z\n' \
                   ' CELL        {a:7.4f}   {b:7.4f}   {c:7.4f}  {aa:8.4f}  {bb:8.4f}  {cc:8.4f}  {z:3.1f}\n' \
                   '*EOS\n' \
                   '\n' \
                   'SYMMETRY\n' \
                   ' SYOP      1 0 0 0.0000000     0 1 0 0.0000000     0 0 1 0.0000000\n' \
                   '*EOS\n' \
                   '\n' \
                   'ATOMS               X       Y       Z       U(EQ)    OCC    OXID WYCK AT DT\n'.format(a=cell[0],
                                                                                                          b=cell[1],
                                                                                                          c=cell[2],
                                                                                                          aa=cell[3],
                                                                                                          bb=cell[4],
                                                                                                          cc=cell[5],
                                                                                                          z=1)
    molecule2 = load(pluginManager)
    global use
    use = pluginManager.arg('use')
    printer('\nUsing differences between \'{}\' of \'exp\' model\nand \'cart_meas\' of loaded model.\n'.format(use))
    for atom in data.iter_atoms():
        atom2 = molecule2[atom.get_name()]
        filecontent += add_atom_data(atom, atom2)
    filecontent += '\n' \
                   '*EOS\n' \
                   '\n' \
                   'END\n'
    printer(filecontent)
    filepointer = open('OUTPUT.SCFS', 'w')
    filepointer.write(filecontent)


def add_atom_data(atom, atom2):
    """
    Creates atom specific lines for equivalent atoms of different models.
    :param atom: Atom object from model 1.
    :param atom2: Atom object from model 2.
    :return: String ready to be written to a peanut input file.
    """
    n = atom.get_name().lstrip(atom.get_element())
    frac = atom.get_frac()
    adp = cart2frac_ADP(atom.adp[use], atom.molecule.get_cell())
    eq = Uiso(adp)
    atomlines = '\n' \
                ' ATCO    {el:2s}{n:<6}{x:8.5f}{y:8.5f}{z:8.5f}{eq:8.5f}{oc:8.5f}{ox:8.5f}{s:>10}\n'\
        .format(el=atom.get_element(),
                n=n,
                x=frac[0],
                y=frac[1],
                z=frac[2],
                eq=eq,
                oc=1,
                ox=0,
                s=2)
    atomlines += ' UIJ CAL {el:2s}{n:<6}{u11:8.5f}{u22:8.5f}{u33:8.5f}{u12:8.5f}{u13:8.5f}{u23:8.5f}\n'\
        .format(el=atom.get_element(),
                n=n,
                u11=adp[0],
                u22=adp[1],
                u33=adp[2],
                u12=adp[3],
                u13=adp[4],
                u23=adp[5])
    try:
        adp = atom2.adp['frac_meas']
    except KeyError:
        adp = cart2frac_ADP(atom2.adp['cart_meas'], atom.molecule.get_cell())
    atomlines += ' UIJ     {el:2s}{n:<6}{u11:8.5f}{u22:8.5f}{u33:8.5f}{u12:8.5f}{u13:8.5f}{u23:8.5f}\n'\
        .format(el=atom.get_element(),
                n=n,
                u11=adp[0],
                u22=adp[1],
                u33=adp[2],
                u12=adp[3],
                u13=adp[4],
                u23=adp[5])
    atomlines += ' UIJE    {el:2s}{n:<6}{u11:8.5f}{u22:8.5f}{u33:8.5f}{u12:8.5f}{u13:8.5f}{u23:8.5f}\n'\
        .format(el=atom.get_element(),
                n=n,
                u11=0,
                u22=0,
                u33=0,
                u12=0,
                u13=0,
                u23=0)
    return atomlines

def load(pluginManager):
    printer = pluginManager.get_active_printer()
    loader = Loader(pluginManager.get_active_printer())
    filename = pluginManager.arg('load')
    loader.create(filename)
    mol = loader.load('compare')
    printer('Using file {} for comparison.'.format(filename))
    return mol