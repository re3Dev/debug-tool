import re
import os
import sys
from textwrap import indent
from parse_extruders import parse_klippy_log

# ANSI escape codes for color formatting
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def parse_open_file(filePath):
    try:
        with open(filePath, 'r') as file:
            klippy = file.read()
    except FileNotFoundError:
        print(f"{RED}File not found: {filePath}{RESET}")
        return
    except Exception as e:
        print(f"{RED}Error opening file {filePath}: {e}{RESET}")
        return

    error_patterns = {
    "thermocouple reader fault": """
    Look for max31856 [ERROR TYPE] in later errors for detailed solutions.
""",
    
    "thermocouple out of range": """
It read temperatures that were higher or lower than the allowed range.

Fire Hazard!
Safety Feature, so it shouldn't happen. Check heater wiring.

Machine is now a fire risk, be careful!

""", "max31856: over/under voltage fault" : """
Check the grounding cables on the trolley plate and the bed plate.

Quick Fix: 
1. Turn off the machine.
2. Unplug the yellow thermocouple connectors.
3. Turn the machine back on.
4. Press ‘Restart’ on the touchscreen when booted up.
5. Plug the yellow thermocouple connectors back in.
6. Press ‘Firmware_Restart’ on the touchscreen.
""", "max31856: thermocouple open fault" : """
    The thermocouple wiring is faulty or the thermocouple is bad. 

    Solution: 
    Replace thermocouple or check wiring.
""",
    "shutdown due to webhooks request": """
This error occurs when the emergency stop button is pressed in the software.

Solution:
1. Press ‘Firmware_Restart’ to restore normal operation.
""",

    "move out of range": """
The printer attempted to move beyond its allowed range, often due to incorrect movement mode settings.

Solution:
1. Check the console output for the coordinates that caused the error.
2. If the error involves X or Y movement, ensure the axis is set to absolute mode.
   
   - Relative Mode: `G1 X10` moves the X axis **+10 from its last position**.
   - Absolute Mode: `G1 X10` moves the X axis **to coordinate (10, 10)**.

3. To fix the issue, add `G90` to your start G-code to enforce absolute positioning.
""",

    "move exceeds maximum extrusion": """
This error is often caused by a slicer issue where an excessive extrusion amount is requested.

Solution:
1. Ensure your start G-code includes `G92 E0` before any extrusion commands.
2. Verify that your slicer’s flow settings are correct.
3. If the problem persists, adjust safety limits in the configuration:
   - Copy `/build/fff_extruders.cfg` and paste it into `standalone.cfg`.
   - Increase `max_extrude_cross_section` and `max_extrude_only_distance`.
   - Save the changes and restart the printer.
""", "no trigger on": """
No trigger on z after full movement
We tried to home that motor and it never reached the home position
Solution: Check the motor and limit switches for the corresponding axis.
""", "got eof": """

Check the USB connection between the Raspberry Pi (or host machine) and the mainboard. Over time, vibrations can loosen the connectors.

Solution:
1. Power off the printer.
2. Unplug and replug the USB cable connecting the Raspberry Pi to the mainboard.
3. Power the printer back on.
4. If the issue persists, try using a different USB cable or port.
""", "unable to open serial port": """
The serial id on the archimajor board isn't being read properly. So the raspberry pi and the board can't communication.

Solution:
Check the serial id using ls /dev/serial/by-id to see the actual serial id of the archimajor board
If no file found: Check USB connection from raspberry pi to archimajor and reboot
If file found and number is given: Check the config file in the bulid (_serial.cfg), and then in there we need to specify the serial (from the first ls command).
""", "not heating at expected rate" : """
    Either the heating error parameters are too strict, or the thermocouple is not reading correctly. 
    
    Solution:
    You can view heating error parameters in the fff/fgf_heaters.cfg file under [verify_heater] - you can modify these parameters in the standalone.cfg file.
""", "timeout with mcu" : "GCode was intensive. Try a different gcode file to see if error persists.",
"max31856: cold junction range fault" : "Export this log and check back with software engineer.", 
"max31856: thermocouple range fault" : "Check the thermocouple wiring and if error persists, export this log and check back with software engineer.\n", 
"max31856: cold junction high fault" : "Export this log and check back with software engineer.", 
"max31856: cold junction low fault" : "Export this log and check back with software engineer.", 
"max31856: thermocouple high fault" : "Export this log and check back with software engineer.", 
"max31856: thermocouple low fault" : "Export this log and check back with software engineer."
    }


    # Puts all of the error_patterns in a group regex (|)
    # Uses re.escape to ensure esc characters (.*+) are handled like normal chars
    pattern = re.compile("|".join(map(re.escape, error_patterns.keys())), re.IGNORECASE)

    error_matches = []
    fileName = os.path.basename(filePath)

    for match in pattern.finditer(klippy):
        if match.group() not in error_matches:
            error_matches.append(match.group())

    if error_matches:
        print(f"\n{BOLD}{CYAN}Errors found in {fileName}:{RESET}")
        for error in error_matches:
            help_message = indent(error_patterns[error.lower()], "  ")
            print(f"{RED}  ⚠️  Error Detected:{RESET} {BOLD}{error}{RESET} \n")
            print(f"{GREEN}  💡  Possible Solution:{RESET}\n{help_message}")
            if error.lower() == "thermocouple reader fault":
                print(parse_klippy_log(filePath))
                print("\n")
            print(f"{YELLOW}{'-' * 58}{RESET}")

            
    else:
        print(f"\n{BOLD}{GREEN}No errors found in {fileName}.{RESET}")

def main():
    if len(sys.argv) != 2:
        print(f"{RED}Usage: python script.py <log_file>{RESET}")
        sys.exit(1)

    file = sys.argv[1]
    parse_open_file(file)

if __name__ == "__main__":
    main()
