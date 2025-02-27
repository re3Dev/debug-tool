import requests
import json
import time

PRINTER_IP = "http://192.168.4.2"
SYSTEM_FILE = "/etc/OliveTin/entities/system_data.json"
TEMPS_FILE = "/etc/OliveTin/entities/printer_temps.json"

def get_printer_temps():
    data = {}
    components = ["extruder", "extruder1", "extruder2", "heater_bed"]

    for component in components:
        response = requests.get(f"{PRINTER_IP}/printer/objects/query?{component}=target,temperature")
        if response.status_code == 200:
            json_data = response.json().get("result", {})
            if component in json_data.get("status", {}):
                target = json_data["status"][component]["target"]
                current = json_data["status"][component]["temperature"]
                if target is not None and current is not None:
                    data[component] = {"target": target, "current": current}
    
    return data

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

def write_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def update_static_data():
    system_info = get_system_data()
    printer_info = get_printer_data()

    static_data = {
        "system": system_info,
        "printer": printer_info
    }

    write_json(SYSTEM_FILE, static_data)
    print("Updated system_data.json")

def update_dynamic_data():
    while True:
        printer_temps = get_printer_temps()
        write_json(TEMPS_FILE, {"temps": printer_temps})
        print("Updated printer_temps.json")
        time.sleep(1)

if __name__ == "__main__":
    update_static_data()  # Run once at startup
    update_dynamic_data()  # Run loop for real-time temps
