#!/usr/bin/env python3
"""
rmtea - Remove Empty Directories

A simple GUI application to recursively find and delete empty directories.
Uses Tkinter with ttkbootstrap for modern themes.
"""

import os
import shutil
from pathlib import Path
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class EmptyDirRemover(ttk.Window):
    """Main application window for removing empty directories."""
    
    # Common files that are auto-generated and can be ignored
    IGNORABLE_FILES = {
        '.DS_Store',      # macOS
        'Thumbs.db',      # Windows
        'desktop.ini',    # Windows
        '.localized',     # macOS
        'Icon\r',         # macOS custom folder icons
        '._.DS_Store',    # macOS resource fork
        '._*',            # macOS resource fork files (pattern)
    }
    
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("rmtea - Remove Empty Directories")
        self.geometry("800x600")
        
        self.selected_path = None
        self.empty_dirs = []
        self.ignore_auto_files = ttk.BooleanVar(value=True)
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # Directory selection section
        dir_frame = ttk.LabelFrame(main_frame, text="Directory Selection")
        dir_frame.pack(fill=X, pady=(0, 10), padx=5, ipady=5)
        
        self.path_label = ttk.Label(dir_frame, text="No directory selected", 
                                    foreground="gray")
        self.path_label.pack(side=LEFT, fill=X, expand=YES, padx=10, pady=10)
        
        browse_btn = ttk.Button(dir_frame, text="Browse...", 
                               command=self.browse_directory, bootstyle=PRIMARY)
        browse_btn.pack(side=RIGHT, padx=10, pady=10)
        
        # Options section
        options_frame = ttk.LabelFrame(main_frame, text="Options")
        options_frame.pack(fill=X, pady=(0, 10), padx=5, ipady=5)
        
        ignore_check = ttk.Checkbutton(
            options_frame, 
            text="Ignore auto-generated files (.DS_Store, Thumbs.db, etc.)",
            variable=self.ignore_auto_files,
            bootstyle="round-toggle"
        )
        ignore_check.pack(anchor=W, padx=10, pady=10)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, pady=(0, 10))
        
        scan_btn = ttk.Button(button_frame, text="Scan for Empty Directories", 
                             command=self.scan_directories, bootstyle=INFO)
        scan_btn.pack(side=LEFT, padx=(0, 5))
        
        self.delete_btn = ttk.Button(button_frame, text="Delete Empty Directories", 
                                     command=self.delete_directories, 
                                     bootstyle=DANGER, state=DISABLED)
        self.delete_btn.pack(side=LEFT)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Empty Directories Found")
        results_frame.pack(fill=BOTH, expand=YES, padx=5, ipady=5)
        
        # Create scrolled text widget
        scroll_frame = ttk.Frame(results_frame)
        scroll_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.results_text = ttk.Text(scroll_frame, wrap=NONE, 
                                     yscrollcommand=scrollbar.set,
                                     height=15)
        self.results_text.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.config(command=self.results_text.yview)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready", 
                                     relief=SUNKEN, anchor=W)
        self.status_label.pack(fill=X, pady=(10, 0))
        
    def browse_directory(self):
        """Open directory selection dialog."""
        directory = filedialog.askdirectory(title="Select Directory to Scan")
        if directory:
            self.selected_path = Path(directory)
            self.path_label.config(text=str(self.selected_path), foreground="")
            self.empty_dirs = []
            self.results_text.delete(1.0, END)
            self.delete_btn.config(state=DISABLED)
            self.status_label.config(text=f"Selected: {self.selected_path}")
            
    def is_ignorable_file(self, filename):
        """Check if a file should be ignored based on ignore settings."""
        if not self.ignore_auto_files.get():
            return False
            
        # Check exact matches
        if filename in self.IGNORABLE_FILES:
            return True
            
        # Check pattern matches (like ._* for macOS resource forks)
        if filename.startswith('._'):
            return True
            
        return False
        
    def is_directory_empty(self, path):
        """
        Check if a directory is empty or contains only ignorable files.
        
        Args:
            path: Path object representing the directory
            
        Returns:
            bool: True if directory is empty or contains only ignorable files
        """
        try:
            items = list(path.iterdir())
            
            # If no items at all, it's empty
            if not items:
                return True
                
            # Check if all items are ignorable files
            for item in items:
                if item.is_file() and self.is_ignorable_file(item.name):
                    continue
                else:
                    # Found a non-ignorable file or a directory
                    return False
                    
            # All items were ignorable files
            return True
            
        except (PermissionError, OSError) as e:
            # Can't access directory, treat as non-empty
            return False
            
    def find_empty_directories(self, root_path):
        """
        Recursively find all empty directories.
        
        Args:
            root_path: Path object representing the root directory to scan
            
        Returns:
            list: List of Path objects representing empty directories
        """
        empty_dirs = []
        
        try:
            # Walk directory tree bottom-up to check subdirectories first
            for dirpath, dirnames, filenames in os.walk(str(root_path), topdown=False):
                dir_path = Path(dirpath)
                
                # Skip the root directory itself
                if dir_path == root_path:
                    continue
                    
                if self.is_directory_empty(dir_path):
                    empty_dirs.append(dir_path)
                    
        except (PermissionError, OSError) as e:
            self.status_label.config(text=f"Error scanning: {e}")
            
        return empty_dirs
        
    def scan_directories(self):
        """Scan selected directory for empty directories."""
        if not self.selected_path:
            messagebox.showwarning("No Directory", 
                                  "Please select a directory to scan.")
            return
            
        if not self.selected_path.exists():
            messagebox.showerror("Invalid Directory", 
                               "The selected directory does not exist.")
            return
            
        self.status_label.config(text="Scanning...")
        self.update()
        
        self.empty_dirs = self.find_empty_directories(self.selected_path)
        
        # Display results
        self.results_text.delete(1.0, END)
        
        if self.empty_dirs:
            for dir_path in sorted(self.empty_dirs):
                self.results_text.insert(END, f"{dir_path}\n")
                
            self.status_label.config(
                text=f"Found {len(self.empty_dirs)} empty director{'y' if len(self.empty_dirs) == 1 else 'ies'}"
            )
            self.delete_btn.config(state=NORMAL)
        else:
            self.results_text.insert(END, "No empty directories found.")
            self.status_label.config(text="No empty directories found")
            self.delete_btn.config(state=DISABLED)
            
    def delete_directories(self):
        """Delete all found empty directories after confirmation."""
        if not self.empty_dirs:
            return
            
        count = len(self.empty_dirs)
        response = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {count} empty director{'y' if count == 1 else 'ies'}?\n\n"
            "This action cannot be undone."
        )
        
        if not response:
            return
            
        deleted_count = 0
        failed_count = 0
        
        for dir_path in self.empty_dirs:
            try:
                # Double-check it's still empty before deleting
                if self.is_directory_empty(dir_path) and dir_path.exists():
                    # Remove any ignorable files first
                    if self.ignore_auto_files.get():
                        for item in dir_path.iterdir():
                            if item.is_file() and self.is_ignorable_file(item.name):
                                item.unlink()
                    
                    # Remove the directory
                    dir_path.rmdir()
                    deleted_count += 1
            except (PermissionError, OSError) as e:
                failed_count += 1
                
        # Show results
        message = f"Successfully deleted {deleted_count} director{'y' if deleted_count == 1 else 'ies'}."
        if failed_count > 0:
            message += f"\nFailed to delete {failed_count} director{'y' if failed_count == 1 else 'ies'} (permission denied or in use)."
            
        messagebox.showinfo("Deletion Complete", message)
        
        # Clear results and rescan if there might be more empty directories
        self.empty_dirs = []
        self.results_text.delete(1.0, END)
        self.delete_btn.config(state=DISABLED)
        self.status_label.config(text="Deletion complete")


def main():
    """Main entry point for the application."""
    app = EmptyDirRemover()
    app.mainloop()


if __name__ == "__main__":
    main()
