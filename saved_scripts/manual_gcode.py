import requests
import sys

PRINTER_IP = "IP HERE"

def send_gcode(cmd_line):
    # Ensure the command is a string
    cmd_str = " ".join(cmd_line)  # Convert list to space-separated string
    response = requests.post(f"http://{PRINTER_IP}/printer/gcode/script?script={cmd_str}")

    if response.status_code == 200:
        print(f"Successfully sent G-code: {cmd_str}")
    else:
        print(f"Failed to send G-code: {response.status_code} - {response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <GCODE_COMMAND>")
        sys.exit(1)

    send_gcode(sys.argv[1:])
