import sys
import re

# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def parse_klippy_log(file_path):
    extruder_temps = {}
    heater_bed_temp = None
    valid_extruder = False
    valid_heater_bed = False
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"{RED}Error: The specified file was not found.{RESET}")
        return
    except IOError:
        print(f"{RED}Error: An error occurred while trying to read the file.{RESET}")
        return

    for line in lines:
        # Check for print_stall before parsing extruder temperatures
        if "print_stall" in line:
            valid_extruder = True
        
        # Check for supply_voltage before parsing heater_bed temperature
        if "freq" in line:
            valid_heater_bed = True
        
        if valid_extruder:
            extruder_matches = re.findall(r'extruder(\d*): target=\d+ temp=([\d\.]+)', line)
            for match in extruder_matches:
                extruder_index = int(match[0]) if match[0] else 0  # Default to 0 if no index is found ('extruder: ...')
                extruder_temps[extruder_index] = float(match[1])
            
        if valid_heater_bed:
            heater_bed_match = re.search(r'heater_bed: target=\d+ temp=([\d\.]+)', line)
            if heater_bed_match:
                heater_bed_temp = float(heater_bed_match.group(1))

    result = f"{BOLD}{CYAN}\nLast known temperatures...{RESET}\n"
    
    for extruder_index, temp in extruder_temps.items():
        result += f"  {GREEN}Extruder {extruder_index} Temp:{RESET} {BOLD}{temp}°C{RESET}\n"

    if heater_bed_temp is not None:
        result += f"  {GREEN}Heater Bed Temp:{RESET} {BOLD}{heater_bed_temp}°C{RESET}\n"
    else:
        result += f"  {RED}Heater Bed Temp: Not Found{RESET}\n"

    return result

def main():
    if len(sys.argv) != 2:
        print(f"{RED}Usage: python parse_extruders.py <log_file>{RESET}")
        sys.exit(1)

    file = sys.argv[1]
    print(parse_klippy_log(file))

if __name__ == "__main__":
    main()
