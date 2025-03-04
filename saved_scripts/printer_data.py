import requests
import json
import time
import os

PRINTER_IP = "IP ADDRESS HERE"
SYSTEM_FILE = "/etc/OliveTin/entities/system_data.json"
TEMPS_FILE = "/etc/OliveTin/entities/printer_temps.json"

COMPONENT_NAMES = {
    "extruder": "Extruder 1",
    "extruder1": "Extruder 2",
    "extruder2": "Extruder 3",
    "heater_bed": "Heater Bed"
}

def get_printer_temps():
    temps_list = []  # Store each entry as a separate JSON object

    for component, name in COMPONENT_NAMES.items():
        response = requests.get(f"{PRINTER_IP}/printer/objects/query?{component}=target,temperature")
        if response.status_code == 200:
            json_data = response.json().get("result", {})
            if component in json_data.get("status", {}):
                target = json_data["status"][component]["target"]
                current = json_data["status"][component]["temperature"]
                if target is not None and current is not None:
                    temps_list.append({
                        "name": name,
                        "target": target,
                        "current": current
                    })
    
    return temps_list

def get_printer_data():
    response = requests.get(f"{PRINTER_IP}/printer/info")
    if response.status_code == 200:
        json_data = response.json().get("result", {})
        return {"hostname": json_data.get("hostname", "Unknown"), "state": json_data.get("state", "Unknown")}
    return {}

def get_system_data():
    response = requests.get(f"{PRINTER_IP}/machine/system_info")
    if response.status_code == 200:
        json_data = response.json().get("result", {})
        network_info = json_data.get("system_info", {}).get("network", {}).get("wlan0", {})
        return {"mac_address": network_info.get("mac_address", "Unknown")}
    return {}

def read_json(file_path):
    """Read JSON data from a file. Returns None if the file does not exist."""
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None

def write_json(file_path, data, newline=False):
    with open(file_path, "w") as f:
        if newline:
            for entry in data:
                json.dump(entry, f)
                f.write("\n")  # Newline to separate JSON objects
        else:
            json.dump(data, f, indent=4)

def update_static_data():
    """Updates system data only if there are changes."""
    system_info = get_system_data()
    printer_info = get_printer_data()

    static_data = {
        "system": system_info,
        "printer": printer_info
    }

    # Read current data to compare
    current_data = read_json(SYSTEM_FILE)

    # Only write if data has changed
    if current_data != static_data:
        write_json(SYSTEM_FILE, static_data)
        print("Updated system_data.json")
    else:
        print("No changes in system_data.json")

def update_dynamic_data():
    printer_temps = get_printer_temps()
    write_json(TEMPS_FILE, printer_temps, newline=True)
    print("Updated printer_temps.json")
        

if __name__ == "__main__":
    update_static_data()  # Run once at startup
    update_dynamic_data()  # Update temps
