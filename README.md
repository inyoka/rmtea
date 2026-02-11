# rmtea - Remove Empty Directories

A simple GUI application to recursively find and delete empty directories in your file system.

![rmtea GUI](https://github.com/user-attachments/assets/d222aad6-ec4f-4b0e-bb52-e04d6436f90f)

## Features

- **Modern GUI**: Built with Tkinter and ttkbootstrap for a clean, themed interface
- **Recursive Scanning**: Finds all empty directories within a selected folder and its subdirectories
- **Smart Detection**: Optionally ignores common auto-generated files that you might not care about:
  - `.DS_Store` (macOS)
  - `Thumbs.db` (Windows)
  - `desktop.ini` (Windows)
  - `.localized` (macOS)
  - `._*` files (macOS resource forks)
- **Preview Before Delete**: See exactly which directories will be removed before taking action
- **Safe Deletion**: Confirmation dialog prevents accidental deletion
- **Status Updates**: Real-time feedback on scanning and deletion progress

## Installation

### Prerequisites

- Python 3.7 or higher
- tkinter (usually included with Python, but may need separate installation on Linux)

### Install Dependencies

```bash
pip install -r requirements.txt
```

On Linux, you may also need to install tkinter:

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

## Usage

### Running the Application

```bash
python3 rmtea.py
```

Or make it executable:

```bash
chmod +x rmtea.py
./rmtea.py
```

### Using the GUI

1. **Select a Directory**: Click the "Browse..." button to choose the root directory you want to scan
2. **Configure Options**: 
   - Check "Ignore auto-generated files" to treat directories containing only system files (like `.DS_Store`) as empty
   - Uncheck it if you want to only delete truly empty directories
3. **Scan**: Click "Scan for Empty Directories" to find all empty directories
4. **Review**: Check the list of directories that will be deleted
5. **Delete**: Click "Delete Empty Directories" and confirm the action

### What Counts as "Empty"?

A directory is considered empty if:
- It contains no files or subdirectories, OR
- It only contains ignorable auto-generated files (when the option is enabled)

The following files are considered auto-generated and ignorable:
- `.DS_Store` - macOS folder metadata
- `Thumbs.db` - Windows thumbnail cache
- `desktop.ini` - Windows folder customization
- `.localized` - macOS localization file
- `._*` - macOS resource fork files

## Example

Consider this directory structure:

```
my_project/
├── empty_folder/
├── has_ds_store/
│   └── .DS_Store
├── not_empty/
│   └── readme.txt
└── nested/
    └── also_empty/
```

With "Ignore auto-generated files" **enabled**:
- `empty_folder/` - Will be deleted (truly empty)
- `has_ds_store/` - Will be deleted (only contains .DS_Store)
- `nested/also_empty/` - Will be deleted (nested empty directory)
- `not_empty/` - Will NOT be deleted (contains a real file)

With "Ignore auto-generated files" **disabled**:
- `empty_folder/` - Will be deleted
- `has_ds_store/` - Will NOT be deleted (contains a file)
- `nested/also_empty/` - Will be deleted
- `not_empty/` - Will NOT be deleted

## Safety Features

- **Confirmation Dialog**: You must confirm before any directories are deleted
- **No Undo**: Deleted directories cannot be recovered - review carefully before confirming
- **Permission Handling**: Directories that cannot be accessed or deleted (due to permissions) are skipped
- **Real-time Validation**: Directories are re-checked immediately before deletion to ensure they're still empty

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
