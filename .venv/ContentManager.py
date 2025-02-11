import tkinter as tk
from tkinter import ttk
import programNames

program_names = programNames.program_names

# Track items added to the left pane
added_items = set()

def search_function(event=None):
    """Update search results in real time.
    When no text is entered, show all program names."""
    query = search_entry.get().lower()
    results_listbox.delete(0, tk.END)
    if not query:
        for item in program_names:
            results_listbox.insert(tk.END, item)
    else:
        for item in program_names:
            if query in item.lower():
                results_listbox.insert(tk.END, item)

def add_selected_item():
    """Add the selected program from the search results to the left pane list."""
    selection = results_listbox.curselection()
    if not selection:
        return
    item = results_listbox.get(selection[0])
    if item in added_items:
        return  # Skip if already added
    added_items.add(item)
    left_listbox.insert(tk.END, item)

def remove_selected_item():
    """Remove the currently selected item from the left pane list."""
    selection = left_listbox.curselection()
    if not selection:
        return
    index = selection[0]
    item = left_listbox.get(index)
    left_listbox.delete(index)
    added_items.remove(item)

def show_progress_bar():
    """Display a progress bar that fills over 10 seconds then closes the program."""
    progress_window = tk.Toplevel(root)
    progress_window.title("Finishing...")
    progress_label = tk.Label(progress_window, text="Installing...")
    progress_label.pack(pady=10)

    progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)
    progress_bar["maximum"] = 100
    progress_bar["value"] = 0

    def update_progress(current=0):
        progress_bar["value"] = current
        if current < 100:
            # Update every 100ms; 100 * 100ms = 10 seconds total
            progress_window.after(100, update_progress, current+1)
        else:
            root.destroy()  # Close the entire application

    update_progress()

def finish_action():
    """Show a confirmation window listing selected programs and profiles.
    If confirmed, show the progress bar; otherwise, do nothing."""
    # Gather selected programs from the left pane
    selected_programs = left_listbox.get(0, tk.END)
    # Gather selected profiles from the right pane checkboxes
    selected_profiles = [profile for profile, var in profile_vars.items() if var.get()]

    # Build the summary message
    summary_text = "You have selected the following programs:\n"
    if selected_programs:
        for program in selected_programs:
            summary_text += f" - {program}\n"
    else:
        summary_text += " None\n"

    summary_text += "\nAnd the following profiles:\n"
    if selected_profiles:
        for profile in selected_profiles:
            summary_text += f" - {profile}\n"
    else:
        summary_text += " None\n"

    summary_text += "\nDo you want to proceed with the installation?"

    # Create the confirmation window
    confirm_window = tk.Toplevel(root)
    confirm_window.title("Confirm Installation")
    confirm_label = tk.Label(confirm_window, text=summary_text, justify="left")
    confirm_label.pack(padx=10, pady=10)

    def on_confirm():
        confirm_window.destroy()
        show_progress_bar()

    def on_cancel():
        confirm_window.destroy()

    button_frame = tk.Frame(confirm_window)
    button_frame.pack(pady=10)
    confirm_button = tk.Button(button_frame, text="Confirm", command=on_confirm)
    confirm_button.pack(side="left", padx=5)
    cancel_button = tk.Button(button_frame, text="Cancel", command=on_cancel)
    cancel_button.pack(side="right", padx=5)

def quit_action():
    """Close the program immediately."""
    root.quit()

# Create the main window
root = tk.Tk()
root.title("Content Manager")
root.geometry("800x600")

# Create a PanedWindow for horizontal resizing of the three panes
panes_pane = tk.PanedWindow(root, orient=tk.HORIZONTAL)
panes_pane.pack(side="top", fill="both", expand=True)

# ----------------- Left Pane -----------------
left_frame = tk.Frame(panes_pane, bd=2, relief="sunken")
tk.Label(left_frame, text="Programs to Install:", anchor="w").pack(fill="x", padx=5, pady=5)

left_listbox = tk.Listbox(left_frame)
left_listbox.pack(side="left", fill="both", expand=True)

left_scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=left_listbox.yview)
left_scrollbar.pack(side="right", fill="y")
left_listbox.config(yscrollcommand=left_scrollbar.set)

panes_pane.add(left_frame, minsize=150)

# ----------------- Middle Pane -----------------
middle_frame = tk.Frame(panes_pane, bd=2, relief="sunken")
tk.Label(middle_frame, text="Search Programs:").pack(pady=5)

search_entry = tk.Entry(middle_frame)
search_entry.pack(pady=5, padx=5)

results_listbox = tk.Listbox(middle_frame)
results_listbox.pack(pady=5, padx=5, fill="both", expand=True)

add_button = tk.Button(middle_frame, text="Add Selected", command=add_selected_item)
add_button.pack(pady=5)

remove_button = tk.Button(middle_frame, text="Remove Selected", command=remove_selected_item)
remove_button.pack(pady=5)

# Bind key releases in the search entry to update the search results in real time.
search_entry.bind("<KeyRelease>", search_function)
# Populate the list initially.
search_function()

panes_pane.add(middle_frame, minsize=200)

# ----------------- Right Pane -----------------
right_frame = tk.Frame(panes_pane, bd=2, relief="sunken")
tk.Label(right_frame, text="Profile Options:").pack(pady=5)

# Create profile checkboxes with updated names
profile_names = [
    "Gaming", "Productivity", "Workstation", "Content Creation",
    "Developer", "Education", "Server", "Corporate"
]

profile_vars = {}
for name in profile_names:
    var = tk.BooleanVar(value=False)
    profile_vars[name] = var
    cb = tk.Checkbutton(right_frame, text=name, variable=var)
    cb.pack(anchor="w", padx=5, pady=2)

panes_pane.add(right_frame, minsize=250)

# ----------------- Bottom Button Bar -----------------
bottom_frame = tk.Frame(root)
bottom_frame.pack(side="bottom", fill="x", pady=10)

finish_button = tk.Button(bottom_frame, text="Finish", command=finish_action)
finish_button.pack(side="left", padx=20)

quit_button = tk.Button(bottom_frame, text="Quit", command=quit_action)
quit_button.pack(side="right", padx=20)

# Start the Tkinter event loop.
root.mainloop()
