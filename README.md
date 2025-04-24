# re:Bugger

## Table of Contents
- [Overview](#overview)
- [Features](#overview)
- [Installation/Setup](#installationsetup)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Roadmap](#roadmap)

## Overview
Field technicians often times don’t have the necessary tools to troubleshoot firmware issues with 3D printers onsite. The re:Bugger provides a portable, user-friendly solution designed specifically for efficient onsite diagnostics and debugging.

### Goals of re:Bugger:
- Allow for onsite offline troubleshooting through direct connection.
- Seamless integration with any of the re:3D printers.
- Provide an easy to use interface for field technicians to quickly identity issues.
- Minimize technician training with intuitive design.
- Automatically scan logs for different problems from the printers.
- Reduce average time needed to diagnose the printer’s issue.
- Enable the user to export logs to a USB for further analysis.
- Allow tracking of previous issues with saved logs.

## Features
- Getting logs from the printer
- Parsing logs for errors
- Four different graph generation modes based on log data
- Flashing the 3D printer firmware to an SD card
- Exporting logs and graphs to USB
- Printer Mainsail Interface
- Help Page
- Displaying last known printer temperatures
- Sending manual GCode
- Full printer heater control
- Deleting all logs on the re:Bugger
- Showing terminal pop-up for connected printer
- Bluetooth keyboard connection

## Installation/Setup
**Software:**
1. Download the re:Bugger’s latest firmware `.img` file.  
2. Flash the firmware onto your SD card using Raspberry Pi Imager.  
3. Insert the SD card into the Raspberry Pi and power it on.  
4. Done!

**Hardware:**
1. Print the reBugger's `.stl` file -> (File) and the Raspberry Pi Case's `.stl` file -> (File)
2. Assemble required components (Raspberry Pi, power bank, Ethernet cable, optional keyboard).
3. Using the GPIO Pins, connect a 5V fan to the raspberry Pi and mount it to the back of the Pi.
4. Mount Raspberry Pi in its case and connect power.
5. Ensure all physical connections (Ethernet, USB) are secure.

## Usage
1. **Power on re:Bugger**  
   - Using the power bank attached, click the button the side once to power on. (To turn off double click the same button) 
2. **Connect to Printer**  
   - Using a ethernet cable, connect the re:Bugger to the printer’s ethernet port located on the bottom side of the electrical box. (Make sure the printer is powered on)
3. **Ensure Connection**  
   - Click the “Check Printer Connection” button in the UI to ensure connection to printer.
4. **Debug the Printer**  
   - Using the provided buttons, carry out different checks and tests to determine the issue with the printer.

## Technologies Used
- OliveTin  
- FullPageOS  
- Moonraker API  
- Bash  
- Python  
- DHCP  

## Roadmap

### 1. UI & Theming
- **Dark-Mode Theme**  
  – Add `dark-mode` CSS file under `etc/OliveTin/custom-webui/themes/` and configure `themeName: dark-mode` in `config.yaml`.  
- **Icon Customization**  
  – Support Iconify icons (via https://icon-sets.iconify.design/) alongside Unicode codes.  
- **Help Page Enhancements**  
  – Make new action entries and descriptions to the created help page when actions are added.

### 2. Networking & Connectivity
- **DHCP Master Pi Setup**  
  – Configure `dnsmasq` on `eth0` for address `192.168.4.2` and enable `dhcp-authoritative`.   
- **Bluetooth Keyboard Reliability**  
  – Automate pairing/trust sequence so keyboards reconnect seamlessly on reboot.  
- **SSH Key Management**  
  – Use `StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null` for safe MAC addresses changes.

### 3. Boot & OS Workflow
- **FullPageOS Auto-Login Fixes**  
  – Remove stale `SingleTon*` files under `~/.config/chromium/` to restore kiosk mode.  
  – Use `raspi-config` tweaks to enable console auto-login on TTY1.  
- **Custom Splash Screens**  
  – Swap `/boot/firmware/splash.png` and `/opt/custompios/background.png` for branded visuals.

### 4. Diagnostics & Logging
- **Error Parser UI**  
  – Extend regex-based error matcher to display both error and recommended solution with ANSI coloring.  
- **Temp Extraction Integration**  
  – Embed extruder and bed temperature display within error-handling actions.  
- **SD-Card Flashing Workflow**  
  – Use `dd` command to flash the pre-loaded firmware to an inserted USB slot.

### 5. OliveTin Entities & Actions
- **Dynamic Entities Support**  
  – Load JSON entities (ex. `logs.json`) for dropdown-driven actions.   
- **Graph Customization Triggers**  
  – Allow chained triggers: after running the "generate load graph" button, automatically display or export results.  
- **Chromium Pop-Up Utility**  
  – Provide a generic wrapper (`su – pi –c "chromium-browser … file:///<name>"`) for HTML reports.

### 6. Deployment & Maintenance
- **Auto-Update Script**  
  – Bundle a helper that pulls and pushes from and to GitHub using a PAT (Personal Access Token), overwriting local files.  
- **Credential Management Docs**  
  – Use `git config credential.helper` to store/cache the PAT and keeping best practices.
