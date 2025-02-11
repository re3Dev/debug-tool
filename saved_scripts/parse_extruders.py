import sys
import re

def parse_klippy_log(file_path):
    extruder_temps = {}
    heater_bed_temp = None
    valid_extruder = False
    valid_heater_bed = False
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: The specified file was not found.")
        return
    except IOError:
        print("Error: An error occurred while trying to read the file.")
        return

    for line in lines:
        # Check for print_stall before parsing extruder temperatures
        if "print_stall" in line:
            valid_extruder = True
        
        # Check for supply_voltage before parsing heater_bed temperature
        if "supply_voltage" in line:
            valid_heater_bed = True
        
        if valid_extruder:
            extruder_matches = re.findall(r'extruder(\d*): target=\d+ temp=([\d\.]+)', line)
            for match in extruder_matches:
                extruder_index = int(match[0]) if match[0] else 0 # Default to 0 if no index is found ('extruder: ...')
                extruder_temps[extruder_index] = float(match[1])
            
        if valid_heater_bed:
            heater_bed_match = re.search(r'heater_bed: target=\d+ temp=([\d\.]+)', line)
            if heater_bed_match:
                heater_bed_temp = float(heater_bed_match.group(1))

    result = ""
    for extruder_index in extruder_temps:
        result += f"Extruder {extruder_index} Temp: {extruder_temps[extruder_index]} \n"

    result += f"Heater Bed Temp: {heater_bed_temp}"

    return result

def main():
    if len(sys.argv) != 2:
        print(f"{RED}Usage: python script.py <log_file>{RESET}")
        sys.exit(1)

    file = sys.argv[1]
    print(parse_klippy_log(file))

if __name__ == "__main__":
    main()