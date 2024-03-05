# -*- coding: utf-8 -*-

# The MIT License (MIT) - Copyright (c) Dave Vandenbout.

"""
Generate KiCad 5 netlist.
"""

from __future__ import (  # isort:skip
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import os.path
import time

try:
    from future import standard_library
    standard_library.install_aliases()
except ImportError:
    pass

from skidl.pckg_info import __version__
from skidl.scriptinfo import scriptinfo
from skidl.utilities import add_quotes, export_to_all



def gen_netlist_comp(part, hier_name, tstamps, tstamp):
    """Generate the netlist text describing a component.

    Args:
        part (Part): Part object.

    Returns:
        str: String containing component netlist description.
    """

    from skidl.circuit import HIER_SEP

    ref = add_quotes(part.ref)

    value = add_quotes(part.value_to_str())

    footprint = getattr(part, "footprint", "")
    footprint = add_quotes(footprint)

    lib_filename = getattr(getattr(part, "lib", ""), "filename", "NO_LIB")
    part_name = add_quotes(part.name)

    # Embed the hierarchy along with a random integer into the sheetpath for each component.
    # This enables hierarchical selection in pcbnew.
    # hierarchy = add_quotes("/" + part.hierarchical_name.replace(HIER_SEP, "/"))
    # tstamps = hierarchy
    hierarchy = add_quotes("/" + hier_name.replace(HIER_SEP, "/"))
    tstamps = add_quotes("/" + tstamps.replace(HIER_SEP, "/"))

    fields = ""
    for fld_name, fld_value in part.fields.items():
        fld_value = add_quotes(fld_value)
        if fld_value:
            fld_name = add_quotes(fld_name)
            fields += "\n        (field (name {fld_name}) {fld_value})".format(
                **locals()
            )
    if fields:
        fields = "      (fields" + fields
        fields += ")\n"

    template = (
        "    (comp (ref {ref})\n"
        + "      (value {value})\n"
        + "      (footprint {footprint})\n"
        + "{fields}"
        + "      (libsource (lib {lib_filename}) (part {part_name}))\n"
        + "      (sheetpath (names {hierarchy}) (tstamps {tstamps}))\n"
        + "      (tstamp {tstamp}))"
    )
    txt = template.format(**locals())
    return txt


def gen_netlist_net(net):
    """Generate the netlist text describing a net.

    Args:
        part (Net): Net object.

    Returns:
        str: String containing net netlist description.
    """
    code = add_quotes(net.code)
    name = add_quotes(net.name)
    txt = "    (net (code {code}) (name {name})".format(**locals())
    for p in sorted(net.pins, key=str):
        part_ref = add_quotes(p.part.ref)
        pin_num = add_quotes(p.num)
        txt += "\n      (node (ref {part_ref}) (pin {pin_num}))".format(**locals())
    txt += ")"
    return txt


@export_to_all
def gen_netlist(circuit):
    """Generate a netlist from a Circuit object.

    Args:
        circuit (Circuit): Circuit object.

    Returns:
        str: String containing netlist text.
    """
    from skidl import KICAD
    
    class SheetTimestamp:
        def __init__(self):
            self.tstamps = {}
        
        def set_sheet_tstamp(self, sheet):
        # first check if the sheet has a timestamp. if not, create one
            if sheet not in self.tstamps.keys():
                # wating for 1ms to avoid timestamp collision
                time.sleep(1)
                self.tstamps[sheet] = hex(int(time.time()))[2:].upper()
                return self.tstamps[sheet]
            else:
                return self.tstamps[sheet]

    scr_dict = scriptinfo()
    src_file = os.path.join(scr_dict["dir"], scr_dict["source"])
    date = time.strftime("%m/%d/%Y %I:%M %p")
    tool = "SKiDL (" + __version__ + ")"
    template = (
        "(export (version D)\n"
        + "  (design\n"
        + '    (source "{src_file}")\n'
        + '    (date "{date}")\n'
        + '    (tool "{tool}"))\n'
    )
    netlist = template.format(**locals())
    netlist += "  (components"
    sheet_tstamps = SheetTimestamp()
    for p in sorted(circuit.parts, key=lambda p: str(p.ref)):
        sheet_names = p.hierarchical_name.split(".")[:-1]
        hier_name = ""
        tstamps = ""
        for sheet in sheet_names:
            hier_name = hier_name + sheet + "."
            tstamps = tstamps + sheet_tstamps.set_sheet_tstamp(sheet)+"."
        hier_name = hier_name [:-1]
        tstamps =tstamps[:-1]  # remove the last dot
        tstamp = p.hierarchical_name.split(".")[-1]
        p.fields['hier_name'] = "/" + tstamps.replace(".", "/")
        
        netlist += "\n" + gen_netlist_comp(p, hier_name, tstamps, tstamp)
    netlist += ")\n"
    netlist += "  (nets"
    sorted_nets = sorted(circuit.get_nets(), key=lambda n: str(n.name))
    for code, n in enumerate(sorted_nets, 1):
        n.code = code
        netlist += "\n" + gen_netlist_net(n)
    netlist += ")\n)\n"
    return netlist
