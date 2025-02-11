import re
import os
import sys

def parse_open_file(filePath):
    try:
        with open(filePath, 'r') as file:
            klippy = file.read()
    except FileNotFoundError:
        print(f"File not found: {filePath}")
        return
    except Exception as e:
        print(f"Error opening file {filePath}: {e}")
        return

    error_patterns = [
        "Shutdown due to Webhooks",
        "Thermocouple reader fault",
        "Move out of range"
    ]

    # Puts all of the error_patterns in a group regex (|)
    # Uses re.escape to ensure esc characters (.*+) are handled like normal chars
    pattern = re.compile("|".join(map(re.escape, error_patterns)), re.IGNORECASE)

    error_matches = []
    fileName = os.path.basename(filePath)

    for match in pattern.finditer(klippy):
        # Checks from the start until when the error was found the number of \n
        line_number = klippy[:match.start()].count("\n")
        error_matches.append((line_number, match.group()))

    if error_matches:
        print(f"\nErrors found in {fileName}:")
        for line_number, error in error_matches:
            print(f"  Line {line_number}: {error}")
    else:
        print(f"\nNo errors found in {fileName}.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)

    file = sys.argv[1]

    parse_open_file(file)

if __name__ == "__main__":
    main()