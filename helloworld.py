import os


# Set the environment variables for the KiCad libraries.
os.environ['KICAD7_SYMBOL_DIR'] = os.path.join(os.path.dirname(__file__), '/usr/share/kicad/symbols')
os.environ['KICAD7_FOOTPRINT_DIR'] = os.path.join(os.path.dirname(__file__), '/usr/share/kicad/footprints')

# Import the skidl library.
from skidl import *
from skidl import KICAD7
set_default_tool(KICAD7)
with Group('A1:'):
    
    # Create input & output voltages and ground reference.
    vin, vout, gnd = Net('VI'), Net('VO'), Net('GND')

    # Create two resistors.
    r1, r2 = 2 * Part("Device", 'R', TEMPLATE, footprint='Resistor_SMD:R_0603_1608Metric')
    r1.value = '1K'   # Set upper resistor value.
    r2.value = '500'  # Set lower resistor value.

    # Connect the nets and resistors.
    vin += r1[1]      # Connect the input to the upper resistor.
with Group('A2:'):
    gnd += r2[2]      # Connect the lower resistor to ground.
    vout += r1[2], r2[1] # Output comes from the connection of the two resistors.

# Or you could do it with a single line of code:
# vin && r1 && vout && r2 && gnd

# Output the netlist to a file.
generate_netlist()
# generate_schematic()
generate_pcb()
