"""
Created on Apr 17, 2014

@author: Jens Luebben

Module for filtering atom data. The module interprets
cmd line input to select atoms based on their attributes.
"""


def _set_filter(config, arg1, arg2):
    """
    Function to define which atom pairs are used for the
    calculation of Uiso.

    The filter a list of lists. Every list is one
    filter critereon consisting of an attribute, a value
    a truth criteron and a function.
    For every list the value of the specified attribute is
    compared to the value specified. Only if the comparison of
    both values is equal to the specified truth criterion,
    the Uiso value is calculated.
    If a function is specified, the attribute is passed to
    the function and the return value is compared to
    the truth criterion.
    The latter three parameters default to 'True', True', None
    if not specified.

    To define the filter the commandline argument 'atomfilter' is
    used.
    Example:
    '... atomfilter invariom_name=O2c:name=2=False=len
    will generate:
    [['invariom_name', 'O2c', True, None],
    ['name', 2 , False, len]]
    This filter defines that only those atoms with the invariom
    name 'O2c' and an name hat is not 2 characters long are let through.

    A second filter is defined for neighbor atoms. It follows the
    same syntax except its commanline keyword is 'partnerfilter'
    and is applied to all atoms returned by crystgeom.get_framework\
    _neighbors().
    """
    try:
        # =======================================================================
        # isofilter=[arg.partition('=')[-1] for arg in argv if 'atomfilter=' in arg][0][1:-1].split(',')
        #=======================================================================
        isofilter = config.arg(arg1)
        isofilter = [f.split('=') for f in isofilter]

        for f in isofilter:
            if len(f) < 2:
                f.append('True')
            if len(f) < 3:
                f.append('True')
            if len(f) < 4:
                f.append('None')
    except:
        isofilter = [['element', 'H', 'True', 'None']]
    try:
        # =======================================================================
        # isopartnerfilter=[arg.partition('=')[-1] for arg in argv if 'partnerfilter=' in arg][0][1:-1].split(',')
        #=======================================================================
        # isopartnerfilter = config.arg('partnerfilter')[1:-1].split(',')
        isopartnerfilter = config.arg(arg2)
        isopartnerfilter = [f.split('=') for f in isopartnerfilter]
        # isopartnerfilter = [f.split(':') for f in isopartnerfilter]
        for f in isopartnerfilter:
            if len(f) < 2:
                f.append('True')
            if len(f) < 3:
                f.append('True')
            if len(f) < 4:
                f.append('None')
    except:
        isopartnerfilter = [['None', 'None', 'None', 'None']]
    return isofilter, isopartnerfilter
    isofilterlist = []
    isopartnerfilterlist = []
    for i in range(len(isofilter) / 2):
        isofilterlist.append(tuple(isofilter[2 * i:2 * i + 2]))
    for i in range(len(isopartnerfilter) / 2):
        isopartnerfilterlist.append(tuple(isopartnerfilter[2 * i:2 * i + 2]))

    return [isofilterlist, isopartnerfilterlist]


def _apply_filter(atom, isofilters):
    """
    Evaluates the filter expression. Returns True
    if the the filter value is equal to the
    corresponding attribute for all filters.
    """
    if 'None' in isofilters[0][0]:
        return True

    functionfilters = [isofilter for isofilter in isofilters if not isofilter[-1] == 'None']
    functionfilters = ['{}(atom.{}){}={}'.format(f[3], f[0], f[2], f[1]).replace('True', '=').replace('False', '!') for
                       f in functionfilters]
    functionfilters = [functionfilter if not functionfilter[-1] == '=' else functionfilter[:-1]+'True'
                       for functionfilter in functionfilters]
    if all(getattr(atom, isofilter[0]) == isofilter[1] for isofilter in isofilters if
           isofilter[2] == 'True' and isofilter[-1] == 'None'):
        if all(getattr(atom, isofilter[0]) != isofilter[1] for isofilter in isofilters if
               isofilter[2] == 'False' and isofilter[-1] == 'None'):
            for functionfilter in functionfilters:
                if not eval(functionfilter):
                    return False
            return True
    else:
        return False


def filter_atom_pair(pluginManager, atom1, atom2, arg1='atomfilter', arg2='partnerfilter'):
    """
    Tests atom against the filter expresseion referenced by 'arg'.
    :param pluginManager: Reference to the running instance of the PluginManager.
    :param atom1: Atom instance that is supposed to be tested.
    :param atom2: Second Atom instance that is supposed to be tested.
    :param arg1: Commandline keyword that is used for this filter for atom1.
    :param arg2: Commandline keyword that is used for this filter for atom2.
    :return: True/False
    """
    atomfilter, partnerfilter = _set_filter(pluginManager, arg1, arg2)
    if _apply_filter(atom1, atomfilter) and _apply_filter(atom2, partnerfilter):
        return True


def filter_atom(pluginManager, atom, arg='atomfilter'):
    """
    Tests atom against the filter expresseion referenced by 'arg'.
    :param pluginManager: Reference to the running instance of the PluginManager.
    :param atom: Atom instance that is supposed to be tested.
    :param arg: Commandline keyword that is used for this filter.
    :return: True/False
    """
    atomfilter, _ = _set_filter(pluginManager, arg, 'partnerfilter')
    if _apply_filter(atom, atomfilter):
        return True


def register_custom_fuction(name, function):
    """
    Registers a custom function that can be used with the filter language.
    This is a somewhat dirty way of doing this but it works and the module is
    not using too many names itself. If someone asks, tell them 'practicality
    beats purity'.
    :param name: String that is used to by the filtering language.
    :param function: function that will be associated with that name.
    :return: None
    """
    if name in globals().keys():
        raise NameInUseError
    globals()[name] = function


class NameInUseError(Exception):
    pass