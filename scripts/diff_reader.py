import os
import re

SOURCE_ID = 1  # Define the source machine ID
FILENAME_PATTERN = re.compile(r"savegame_oos_machineid_(\d+)\.oos")
pattern = re.compile(
    r'(tooltip:dw_[\d\w]+),.*?,')  # Pattern needed to discard irrelevant tooltip hashes (they are different even when players are synced)


def clean_tooltip(line):
    return re.sub(pattern, '', line)


def compare_files(file1, file2):
    with open(file1, 'r', encoding='latin-1') as f1, open(file2, 'r', encoding='latin-1') as f2:
        # Read lines from both files, clean tooltip parts, and sort them
        lines1 = [clean_tooltip(line.strip()) for line in f1 if line.strip()]
        lines2 = [clean_tooltip(line.strip()) for line in f2 if line.strip()]

        # Get the maximum number of lines to avoid index errors
        max_lines = max(len(lines1), len(lines2))

        # Check if there are any differences
        differences = False
        for i in range(max_lines):
            line1 = lines1[i] if i < len(lines1) else "No line in file 1"
            line2 = lines2[i] if i < len(lines2) else "No line in file 2"

            if line1 != line2:
                if not differences:
                    print("Differences found:")
                differences = True
                print(f"Line {i + 1} differs:")
                print(f"{file1}: {line1}")
                print(f"{file2}: {line2}")

        if not differences:
            print(f"No differences found between {file1} and {file2}. Files are identical in content.")



if __name__ == "__main__":
    folder = "90a568a2dd2dc080_8" # CHANGE FOLDER NAME to relevant location
    files = os.listdir(folder)

    # Find all savegame files
    save_files = [f for f in files if FILENAME_PATTERN.match(f)]

    # Identify source file
    source_filename = f"savegame_oos_machineid_{SOURCE_ID}.oos"
    source_path = os.path.join(folder, source_filename)

    if not os.path.isfile(source_path):
        print(f"Source file {source_filename} not found in {folder}.")
        exit(1)

    # Compare each file to source
    for filename in save_files:
        match = FILENAME_PATTERN.match(filename)
        if match:
            machine_id = int(match.group(1))
            if machine_id == SOURCE_ID:
                continue  # Skip comparison with self

            target_path = os.path.join(folder, filename)
            compare_files(source_path, target_path)
