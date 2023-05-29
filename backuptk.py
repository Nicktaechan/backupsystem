import shutil
import os
import time
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import schedule
import threading
import logging

# Set up logging
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Define colors
BG_COLOR = '#000000'  # Black
FG_COLOR = '#FFFFFF'  # White
BTN_COLOR = '#0000FF'  # Blue

def select_source_dir():
    source_dir = filedialog.askdirectory(title='Select Source Directory')
    source_entry.delete(0, tk.END)
    source_entry.insert(tk.END, source_dir)

def select_destination_dir():
    destination_dir = filedialog.askdirectory(title='Select Destination Directory')
    destination_entry.delete(0, tk.END)
    destination_entry.insert(tk.END, destination_dir)

def backup():
    source_dir = source_entry.get()
    destination_dir = destination_entry.get()

    # Check if source directory exists
    if not os.path.exists(source_dir):
        messagebox.showerror('Error', 'Source directory does not exist.')
        logging.error(f'Source directory "{source_dir}" does not exist.')
        return

    # Check if destination directory exists
    if not os.path.exists(destination_dir):
        messagebox.showerror('Error', 'Destination directory does not exist.')
        logging.error(f'Destination directory "{destination_dir}" does not exist.')
        return

    try:
        # Create a timestamped folder in the destination directory
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        backup_dir = os.path.join(destination_dir, f'backup_{timestamp}')
        os.makedirs(backup_dir)

        # Copy files from source to backup directory
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                source_path = os.path.join(root, file)
                rel_path = os.path.relpath(source_path, source_dir)
                dest_path = os.path.join(backup_dir, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(source_path, dest_path)

        messagebox.showinfo('Backup', 'Backup completed successfully.')
        logging.info('Backup completed successfully.')
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred during the backup process: {str(e)}')
        logging.exception('An error occurred during the backup process.')

def perform_auto_backup():
    backup()
    frequency = frequency_var.get()

    if frequency == 'daily':
        schedule.every().day.at('00:00').do(backup)
    elif frequency == 'weekly':
        schedule.every().monday.at('00:00').do(backup)
    elif frequency == 'monthly':
        schedule.every().day.at('00:00').do(backup)
    elif frequency == 'hourly':
        schedule.every().hour.do(backup)

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_auto_backup():
    frequency = frequency_var.get()

    if frequency == 'never':
        messagebox.showinfo('Auto Backup', 'Auto backup is set to never.')
        return

    messagebox.showinfo('Auto Backup', f'Auto backup is set to {frequency}.')
    threading.Thread(target=perform_auto_backup).start()

def close_app():
    # Close the application window
    window.destroy()

window = tk.Tk()
window.title('Backup Script')
window.configure(bg=BG_COLOR)

# Logo
logo_path = 'C:/Users/nosiemo/Desktop/backup/logo.png'  # Replace with the path to your logo image
logo_img = Image.open(logo_path)
logo_resized = logo_img.resize((200, 100))  # Adjust the size of the logo as needed
logo_tk = ImageTk.PhotoImage(logo_resized)
logo_label = tk.Label(window, image=logo_tk, bg=BG_COLOR)
logo_label.pack(pady=10)

# Source Directory Selection
source_label = tk.Label(window, text='Source Directory:', bg=BG_COLOR, fg=FG_COLOR)
source_label.pack()
source_entry = tk.Entry(window, width=50)
source_entry.pack(pady=5)
source_button = tk.Button(window, text='Select Source', command=select_source_dir, bg=BTN_COLOR, fg=FG_COLOR)
source_button.pack(pady=5)

# Destination Directory Selection
destination_label = tk.Label(window, text='Destination Directory:', bg=BG_COLOR, fg=FG_COLOR)
destination_label.pack()
destination_entry = tk.Entry(window, width=50)
destination_entry.pack(pady=5)
destination_button = tk.Button(window, text='Select Destination', command=select_destination_dir, bg=BTN_COLOR, fg=FG_COLOR)
destination_button.pack(pady=5)

# Backup Button
backup_button = tk.Button(window, text='Backup', command=backup, bg=BTN_COLOR, fg=FG_COLOR)
backup_button.pack(pady=10)

# Auto Backup Section
auto_backup_label = tk.Label(window, text='Auto Backup:', bg=BG_COLOR, fg=FG_COLOR)
auto_backup_label.pack(pady=10)
frequency_label = tk.Label(window, text='Backup Frequency:', bg=BG_COLOR, fg=FG_COLOR)
frequency_label.pack(pady=5)

frequency_var = tk.StringVar()
frequency_options = ['Never', 'Daily', 'Weekly', 'Monthly', 'Hourly']
frequency_var.set(frequency_options[0])  # Default option: Never

frequency_menu = tk.OptionMenu(window, frequency_var, *frequency_options)
frequency_menu.configure(bg=BTN_COLOR, fg=FG_COLOR)
frequency_menu.pack(pady=5)

# Start Auto Backup Button
start_auto_backup_button = tk.Button(window, text='Start Auto Backup', command=start_auto_backup, bg=BTN_COLOR, fg=FG_COLOR)
start_auto_backup_button.pack(pady=5)

# Close Button
close_button = tk.Button(window, text='Close', command=close_app, bg=BTN_COLOR, fg=FG_COLOR)
close_button.pack(pady=10)

window.mainloop()
