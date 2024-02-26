from skidl import Pin, Part, Alias, SchLib, SKIDL, TEMPLATE

SKIDL_lib_version = '0.0.1'

runpy_lib = SchLib(tool=SKIDL).add_parts(*[
        Part(**{ 'name':'R', 'dest':TEMPLATE, 'tool':SKIDL, 'reference':'R', '_aliases':Alias({'R'}), 'ki_fp_filters':'R_*', 'datasheet':'~', 'ki_description':'Resistor', 'ki_keywords':'R res resistor', '_match_pin_regex':False, 'description':'Resistor', 'keywords':'R res resistor', '_name':'R', 'ref_prefix':'R', 'num_units':None, 'fplist':[''], 'do_erc':True, 'aliases':Alias({'R'}), 'pin':None, 'footprint':'Resistor_SMD:R_0603_1608Metric', 'pins':[
            Pin(num='1',name='~',func=Pin.types.PASSIVE,do_erc=True),
            Pin(num='2',name='~',func=Pin.types.PASSIVE,do_erc=True)] })])