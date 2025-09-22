Smart File Organizer 📂

A command-line Python script to automatically organize files in a directory into categorized subfolders. This tool helps you declutter folders like your "Downloads" directory with ease. It also includes a powerful undo feature to reverse any changes.

Features ✨

    Automatic Categorization: Sorts files into predefined categories like Images, Documents, Videos, Music, Archives, etc.

    Undo Functionality: Made a mistake? Easily undo the last file move or all previous moves with a simple command.

    Recursive Organization: Option to clean up not just a single folder, but all of its subfolders as well.

    Duplicate File Handling: Automatically renames files if a file with the same name already exists in the destination, preventing data loss.

    Move History: Keeps a move_history.json log of all file movements for tracking and undoing purposes.

    CLI Based: Simple and efficient to use directly from your terminal.

Requirements

    Python 3.x

    No external libraries are needed. The script uses standard Python libraries (os, shutil, json, argparse).

How to Use

    Save the code as a Python file (e.g., organizer.py).

    Open your terminal or command prompt.

    Navigate to the directory where you saved organizer.py.

    Run the script using the following commands.

The script operates using three main actions: organize, undo_last, and undo_all.

1. Organize a Folder

This is the main function to sort your files.

    Organize the current directory:
    Bash

python organizer.py organize

Organize a specific directory:
Bash

python organizer.py organize --path "/path/to/your/folder"

(Replace /path/to/your/folder with the actual path, e.g., C:\Users\YourUser\Downloads)

Organize a directory and all its subfolders (recursively):
Bash

    python organizer.py organize --path "/path/to/your/folder" --recursive

2. Undo the Last Move

This command will revert the most recent file move.
Bash

python organizer.py undo_last

3. Undo All Moves

This command will revert all file moves recorded in the move_history.json file.
Bash

python organizer.py undo_all

File Categories

Files are organized based on their extension into the following default categories.
Category	File Extensions
Images	.png, .jpg, .jpeg, .gif, .webp, .svg
Documents	.pdf, .docx, .txt, .xlsx, .pptx, .csv
Videos	.mp4, .mkv, .mov, .avi, .flv
Music	.mp3, .wav, .flac, .aac
Archives	.zip, .rar, .tar, .gz, .7z
Code	.py, .js, .html, .css, .java, .cpp, .c, .php
Executables	.exe, .msi, .dmg
Others	Any other file type

Customization 🔧

You can easily customize the file categories or add new ones. Just edit the FILE_CATEGORIES dictionary at the beginning of the script:
Python

FILE_CATEGORIES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    # Add a new category
    "Fonts": [".ttf", ".otf"],
    ...
}
