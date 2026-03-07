import os
import shutil

FILE_TYPES = {
    "Pictures": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xls", ".xlsx", ".pptx", ".rtf", ".odt", ".ppt", ".csv"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", "wmv", "flv"],
    "Music": [".mp3", ".wav", ".aac", ".ogg", ".flac", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executable": [".exe", ".msi", ".iso", ".dmg"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php", ".json", ".xml", ".dart", ".cxx", ".cc", ".cs", ".rb", ".rs", ".swift", ".kt"],
    "Others": []
}

available_drives = os.listdrives()
stripped_drives = []

print("Available Drives...")
for idx,drive in enumerate(available_drives, start=1):
    strip_drive = drive.strip(r"':\'")
    print(f"{idx}. {strip_drive}")
    stripped_drives.append(strip_drive)

def main():
    disk_form = input("Enter Disk to organize: ").strip().upper()
    if disk_form in stripped_drives:
        user_profile = os.path.expanduser("~")
        if user_profile.upper().startswith(disk_form):
            general_path = user_profile
        else:
            general_path = drive

        print(f"Identified Base Path: {general_path}")
    else:
        print("Disk does not exist. No action taken.")
        return

    sub_folder = input(f"Enter the folder path inside {general_path} to organize (e.g., Downloads): ").strip()
    final_folder_path = os.path.join(general_path, sub_folder)
    if os.path.exists(final_folder_path):
        organizeFolder(final_folder_path)
        print("Folder organized successfully!✅")
    else:
        print("The path you have entered does not exist.")

def getCategory(file_name):
    ext = os.path.splitext(file_name)[1].lower()
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category
    return "Others"

def create_folder_if_missing(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def moveFile(file_path, destination_folder):
    create_folder_if_missing(destination_folder)
    file_name = os.path.basename(file_path)
    shutil.move(file_path, os.path.join(destination_folder, file_name))

def organizeFolder(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path):
            category = getCategory(file_name)
            destination = os.path.join(folder_path, category)
            moveFile(file_path, destination)

if __name__ == "__main__":
    main()
