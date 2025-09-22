import os
import shutil
import json

FILE_CATEGORIES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv"],
    "Music": [".mp3", ".wav", ".flac", ".aac"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php"],
    "Executables": [".exe", ".msi", ".dmg"],
    "Others": []  
}

HISTORY_FILE = "move_history.json"
def load_move_history():
    global move_history
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                move_history = json.load(f)
        except json.JSONDecodeError:
            move_history = []
    else:
        move_history = []

def save_move_history():
    with open(HISTORY_FILE,"w",encoding="utf-8") as f:
        json.dump(move_history,f,indent=4)


def move_file(filepath,folderpath,category):
    try:
        category_path = os.path.join(folderpath,category)
        os.makedirs(category_path,exist_ok=True)
        filename = os.path.basename(filepath)
        destination = os.path.join(category_path,filename)

        # Handling duplicate files
        counter = 1
        while os.path.exists(destination):
            name,ext = os.path.splitext(filename)
            destination = os.path.join(category_path,f"{name}_{counter}{ext}")
            counter += 1

        # saving the moved file details
        move_history.append([filepath,destination])
        shutil.move(filepath,destination)
        save_move_history()
        print(f"Organized {os.path.basename(filepath).ljust(50)} -> {category}/{os.path.basename(destination)}")

    except PermissionError:
        print(f"Permission Denied: could not move {os.path.basename(filepath)}")
    except Exception as e:
        print(f"Error moving {os.path.basename(filepath)}: {str(e)} ")


def get_category(filename):
    ext = os.path.splitext(filename)[1].lower()

    for category,extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    
    return "Others"

def organize_folder(folder_path,recursive=False):
    if not os.path.exists(folder_path):
        print("Error : folder does not exist ❌")
        return
    if not os.path.isdir(folder_path):
        print("Error : Path is not a directory")
        return

    print(f"Organizing Folder: {folder_path}")
    print("_"*50)

    total_files = 0
    organized_files = 0

    # organizing subfolders
    if recursive:
        for root,_,files in os.walk(folder_path):
            for filename in files:
                if filename.startswith('.'):
                    continue
                total_files +=1  
                filepath = os.path.join(root,filename)
                category = get_category(filename)
                if os.path.basename(os.path.dirname(filepath)) in FILE_CATEGORIES:
                    continue
                move_file(filepath,root,category)
                organized_files += 1
                  
    else:
        # single folder mode
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path,filename)
            if not os.path.isfile(filepath) or filename.startswith('.'):
                continue   
            total_files +=1 
            category = get_category(filename)
            move_file(filepath,folder_path,category)
            organized_files += 1
               
     
    print(f"Organization completed! processed {organized_files}/{total_files} files")
    print("_" * 50)
            
def undo_last(confirm=True):
    if confirm:
        response = input("Undo last move? (y/n): ").lower()
        if response != 'y':
            return False
    
    if not move_history:
        print("Nothing to undo!")
        return False
    
    original,destination = move_history.pop()
    save_move_history()
    if not os.path.exists(destination):
        print(f"{destination} does not exist")
        return False
    
    os.makedirs(os.path.dirname(original),exist_ok=True)

    try:
        shutil.move(destination,original)
        print(f"Undid: {os.path.basename(destination)} -> {original}")

        category_dir = os.path.dirname(destination)
        if not os.listdir(category_dir):
            os.rmdir(category_dir)

        return True
    except PermissionError:
            print(f"Permission denied: Could not move {os.path.basename(destination)}")
            return False
    except Exception as e:
            print(f"Error undoing move: {str(e)}")
            return False

def undo_all():
    fail_count = 0
    success_count = 0

    response = input(f"Undo all {len(move_history)} moves? (y/n): ").lower()
    if response != 'y':
        return 
    while move_history:
        try:
            if undo_last(confirm=False):
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"Unexpected error during undo: {str(e)}")
            fail_count += 1
            continue
    print(f"Undo complete: {success_count} successful, {fail_count} failed")


if __name__ == "__main__":
    import argparse

    load_move_history()

    parser = argparse.ArgumentParser(description="File Organizer with Undo Support")
    parser.add_argument("action", choices=["organize", "undo_last", "undo_all"], help="Action to perform")
    parser.add_argument("--path", default=os.getcwd(), help="Folder path to organize (default: current directory)")
    parser.add_argument("--recursive", action="store_true", help="Organize subfolders separately")

    args = parser.parse_args()

    if args.action == "organize":
        organize_folder(args.path, recursive=args.recursive)
    elif args.action == "undo_last":
        undo_last()
    elif args.action == "undo_all":
        undo_all()

