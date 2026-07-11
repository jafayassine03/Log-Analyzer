import os
import shutil
import hashlib
import json
from datetime import datetime

history_file = "organizer_history.json"

categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".svg", ".ico"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"],
    "Audio": [".mp3", ".wav", ".aac", ".ogg", ".flac", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Programs": [".exe", ".msi", ".apk", ".iso"],
    "Code": [".py", ".c", ".cpp", ".java", ".js", ".html", ".css", ".php", ".json", ".xml", ".sql"],
    "Fonts": [".ttf", ".otf"],
    "Books": [".epub", ".mobi"],
    "Others": []
}

history = []


def save_history():
    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)


def load_history():
    global history
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history = json.load(f)


def line():
    print("=" * 60)


def title(text):
    line()
    print(text.center(60))
    line()


def get_category(filename):
    ext = os.path.splitext(filename)[1].lower()

    for category, extensions in categories.items():
        if ext in extensions:
            return category

    return "Others"


def preview(path):
    if not os.path.isdir(path):
        print("Invalid folder.")
        return

    title("Preview")

    files = 0

    for file in os.listdir(path):
        full = os.path.join(path, file)

        if os.path.isfile(full):
            print(f"{file}  -->  {get_category(file)}")
            files += 1

    print()
    print("Files Found:", files)


def organize(path):
    global history

    if not os.path.isdir(path):
        print("Invalid folder.")
        return

    moved = 0

    for file in os.listdir(path):

        source = os.path.join(path, file)

        if not os.path.isfile(source):
            continue

        category = get_category(file)

        destination_folder = os.path.join(path, category)

        os.makedirs(destination_folder, exist_ok=True)

        destination = os.path.join(destination_folder, file)

        if os.path.exists(destination):
            name, ext = os.path.splitext(file)
            destination = os.path.join(
                destination_folder,
                f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
            )

        shutil.move(source, destination)

        history.append({
            "old": source,
            "new": destination
        })

        moved += 1

    save_history()

    title("Finished")
    print("Moved Files:", moved)


def undo():
    global history

    if len(history) == 0:
        print("Nothing to undo.")
        return

    restored = 0

    for item in reversed(history):

        if os.path.exists(item["new"]):
            shutil.move(item["new"], item["old"])
            restored += 1

    history = []
    save_history()

    title("Undo Complete")
    print("Restored Files:", restored)


def hash_file(path):

    sha = hashlib.sha256()

    with open(path, "rb") as f:

        while True:

            data = f.read(8192)

            if not data:
                break

            sha.update(data)

    return sha.hexdigest()


def duplicate_scan(path):

    if not os.path.isdir(path):
        print("Invalid folder.")
        return

    hashes = {}

    duplicates = []

    for root, dirs, files in os.walk(path):

        for file in files:

            full = os.path.join(root, file)

            try:

                h = hash_file(full)

                if h in hashes:

                    duplicates.append((hashes[h], full))

                else:

                    hashes[h] = full

            except:

                pass

    title("Duplicate Files")

    if len(duplicates) == 0:
        print("No duplicates found.")
        return

    for original, duplicate in duplicates:

        print("Original :", original)
        print("Duplicate:", duplicate)
        print("-" * 60)


def statistics(path):

    if not os.path.isdir(path):
        print("Invalid folder.")
        return

    total_files = 0
    total_size = 0

    extensions = {}

    for root, dirs, files in os.walk(path):

        for file in files:

            full = os.path.join(root, file)

            try:

                total_files += 1

                size = os.path.getsize(full)

                total_size += size

                ext = os.path.splitext(file)[1].lower()

                if ext == "":
                    ext = "No Extension"

                extensions[ext] = extensions.get(ext, 0) + 1

            except:

                pass

    title("Statistics")

    print("Files:", total_files)
    print("Folders:", sum(len(d) for _, d, _ in os.walk(path)))
    print("Total Size:", round(total_size / 1024 / 1024, 2), "MB")
    print()

    for ext in sorted(extensions):
        print(f"{ext:<15}{extensions[ext]}")
        def search_files(path):

    if not os.path.isdir(path):
        print("Invalid folder.")
        return

    keyword = input("Search: ").lower()

    results = []

    for root, dirs, files in os.walk(path):

        for file in files:

            if keyword in file.lower():
                results.append(os.path.join(root, file))

    title("Search Results")

    if len(results) == 0:
        print("No matching files found.")
        return

    for i, file in enumerate(results, 1):
        print(f"{i}. {file}")

    print()
    print("Found:", len(results))


def largest_files(path):

    if not os.path.isdir(path):
        print("Invalid folder.")
        return

    files_data = []

    for root, dirs, files in os.walk(path):

        for file in files:

            full = os.path.join(root, file)

            try:

                size = os.path.getsize(full)

                files_data.append((size, full))

            except:

                pass

    files_data.sort(reverse=True)

    title("Largest Files")

    if len(files_data) == 0:
        print("No files found.")
        return

    for size, file in files_data[:10]:

        print(f"{round(size / 1024 / 1024,2):>8} MB   {file}")


def delete_empty_folders(path):

    if not os.path.isdir(path):
        print("Invalid folder.")
        return

    removed = 0

    for root, dirs, files in os.walk(path, topdown=False):

        for directory in dirs:

            folder = os.path.join(root, directory)

            try:

                if len(os.listdir(folder)) == 0:

                    os.rmdir(folder)

                    removed += 1

            except:

                pass

    title("Cleanup")

    print("Removed Empty Folders:", removed)


def bulk_rename(path):

    if not os.path.isdir(path):
        print("Invalid folder.")
        return

    prefix = input("Prefix: ")

    renamed = 0

    for file in os.listdir(path):

        full = os.path.join(path, file)

        if os.path.isfile(full):

            ext = os.path.splitext(file)[1]

            new_name = f"{prefix}_{renamed + 1}{ext}"

            destination = os.path.join(path, new_name)

            try:

                os.rename(full, destination)

                renamed += 1

            except:

                pass

    title("Bulk Rename")

    print("Renamed:", renamed)


def recent_files(path):

    if not os.path.isdir(path):
        print("Invalid folder.")
        return

    data = []

    for root, dirs, files in os.walk(path):

        for file in files:

            full = os.path.join(root, file)

            try:

                modified = os.path.getmtime(full)

                data.append((modified, full))

            except:

                pass

    data.sort(reverse=True)

    title("Recently Modified Files")

    if len(data) == 0:
        print("No files found.")
        return

    for modified, file in data[:10]:

        print(
            datetime.fromtimestamp(modified).strftime("%Y-%m-%d %H:%M:%S"),
            file
        )


def folder_sizes(path):

    if not os.path.isdir(path):
        print("Invalid folder.")
        return

    title("Folder Sizes")

    for item in os.listdir(path):

        folder = os.path.join(path, item)

        if os.path.isdir(folder):

            total = 0

            for root, dirs, files in os.walk(folder):

                for file in files:

                    full = os.path.join(root, file)

                    try:

                        total += os.path.getsize(full)

                    except:

                        pass

            print(f"{item:<25}{round(total/1024/1024,2)} MB")


def file_type_report(path):

    if not os.path.isdir(path):
        print("Invalid folder.")
        return

    report = {}

    for root, dirs, files in os.walk(path):

        for file in files:

            ext = os.path.splitext(file)[1].lower()

            if ext == "":
                ext = "No Extension"

            report[ext] = report.get(ext, 0) + 1

    title("File Type Report")

    for ext, count in sorted(report.items()):

        print(f"{ext:<15}{count}")


def export_report(path):

    if not os.path.isdir(path):
        print("Invalid folder.")
        return

    report = {
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "files": 0,
        "folders": 0,
        "size_mb": 0
    }

    total_size = 0

    for root, dirs, files in os.walk(path):

        report["folders"] += len(dirs)

        report["files"] += len(files)

        for file in files:

            try:

                total_size += os.path.getsize(os.path.join(root, file))

            except:

                pass

    report["size_mb"] = round(total_size / 1024 / 1024, 2)

    with open("report.json", "w") as f:

        json.dump(report, f, indent=4)

    title("Export")

    print("Saved as report.json")
    def clear_history():

    global history

    history = []

    save_history()

    title("History Cleared")

    print("Organization history deleted.")


def show_history():

    title("Organization History")

    if len(history) == 0:
        print("No history available.")
        return

    for item in history:

        print("FROM:", item["old"])
        print("TO  :", item["new"])
        print("-" * 60)


def open_folder(path):

    if not os.path.isdir(path):
        print("Invalid folder.")
        return

    try:

        if os.name == "nt":
            os.startfile(path)

        elif os.name == "posix":
            os.system(f'xdg-open "{path}"')

        else:
            print("Unsupported system.")

    except:

        print("Cannot open folder.")


def security_check(path):

    if not os.path.isdir(path):
        print("Invalid folder.")
        return

    suspicious = []

    dangerous = [
        ".exe",
        ".bat",
        ".cmd",
        ".scr",
        ".vbs",
        ".ps1"
    ]

    for root, dirs, files in os.walk(path):

        for file in files:

            ext = os.path.splitext(file)[1].lower()

            if ext in dangerous:

                suspicious.append(
                    os.path.join(root, file)
                )

    title("Security Check")

    if len(suspicious) == 0:

        print("No suspicious files found.")

    else:

        print("Suspicious files:")

        for file in suspicious:

            print(file)


def duplicate_cleanup(path):

    if not os.path.isdir(path):
        print("Invalid folder.")
        return

    hashes = {}

    deleted = 0

    for root, dirs, files in os.walk(path):

        for file in files:

            full = os.path.join(root, file)

            try:

                h = hash_file(full)

                if h in hashes:

                    os.remove(full)

                    deleted += 1

                else:

                    hashes[h] = full

            except:

                pass

    title("Duplicate Cleanup")

    print("Deleted duplicates:", deleted)


def menu():

    load_history()

    while True:

        title("SMART FILE ORGANIZER PRO")

        print("""
1. Preview Organization
2. Organize Files
3. Undo Organization
4. Find Duplicate Files
5. Delete Duplicate Files
6. Search Files
7. Show Statistics
8. File Type Report
9. Find Largest Files
10. Recently Modified Files
11. Folder Size Analyzer
12. Delete Empty Folders
13. Bulk Rename Files
14. Security Scan
15. Export Report
16. Show History
17. Clear History
18. Open Folder
0. Exit
""")

        choice = input("Select: ")

        if choice == "1":

            preview(input("Folder: "))

        elif choice == "2":

            organize(input("Folder: "))

        elif choice == "3":

            undo()

        elif choice == "4":

            duplicate_scan(input("Folder: "))

        elif choice == "5":

            duplicate_cleanup(input("Folder: "))

        elif choice == "6":

            search_files(input("Folder: "))

        elif choice == "7":

            statistics(input("Folder: "))

        elif choice == "8":

            file_type_report(input("Folder: "))

        elif choice == "9":

            largest_files(input("Folder: "))

        elif choice == "10":

            recent_files(input("Folder: "))

        elif choice == "11":

            folder_sizes(input("Folder: "))

        elif choice == "12":

            delete_empty_folders(input("Folder: "))

        elif choice == "13":

            bulk_rename(input("Folder: "))

        elif choice == "14":

            security_check(input("Folder: "))

        elif choice == "15":

            export_report(input("Folder: "))

        elif choice == "16":

            show_history()

        elif choice == "17":

            clear_history()

        elif choice == "18":

            open_folder(input("Folder: "))

        elif choice == "0":

            print("Goodbye.")
            break

        else:

            print("Invalid option.")


menu()