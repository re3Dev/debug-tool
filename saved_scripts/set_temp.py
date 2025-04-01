import requests
import sys

PRINTER_IP = "192.168.4.2"

def set_temp(temp, name, index):
    if name == 'Heater':  # Bed
        response = requests.post(f"http://{PRINTER_IP}/printer/gcode/script?script=M140 S{temp}")
    elif name.startswith('E'):  # Extruder
        response = requests.post(f"http://{PRINTER_IP}/printer/gcode/script?script=M104 T{index} S{temp}")
    else:
        print("Invalid component type.")
        return

    if response.status_code == 200:
        print(f"Successfully set {name} {index} to {temp}°C")
    else:
        print(f"Failed to set temperature: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print(sys.argv[1])
    print(sys.argv[2])
    if len(sys.argv) != 4:
        print("Usage: python set_temp.py <temperature> <component>")
        sys.exit(1)

    name = sys.argv[1]
    index = sys.argv[2]
    index = str(int(index) - 1)

    temp = sys.argv[3]
    set_temp(temp, name, index)