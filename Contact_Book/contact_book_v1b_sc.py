import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys

class ContactBookApp:

    ## Startup awal
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book Application")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # File to store contacts and settings (saved next to the exe or script)
        # When running as exe, sys.executable is the exe path
        # When running as script, __file__ is the script path
        if getattr(sys, 'frozen', False):
            # Running as compiled exe
            app_dir = os.path.dirname(sys.executable)
        else:
            # Running as script
            app_dir = os.path.dirname(os.path.abspath(__file__))
        self.contacts_file = os.path.join(app_dir, "contacts.json")
        self.settings_file = os.path.join(app_dir, "contact_book_settings.json")
        self.pinned_contacts = set()  # Store pinned contact names (initialized before load_contacts)
        self.contacts = self.load_contacts()

        # Theme color schemes with hex codes
        self.themes = {
            "Default Blue": {
                "header": "#2c3e50",
                "subheader": "#34495e",
                "background": "#ecf0f1",
                "add_button": "#27ae60",
                "edit_button": "#f39c12",
                "delete_button": "#e74c3c",
                "clear_button": "#95a5a6",
                "exit_button": "#c0392b"
            },
            "Ocean Breeze": {
                "header": "#006994",
                "subheader": "#0099cc",
                "background": "#e6f7ff",
                "add_button": "#00bfa5",
                "edit_button": "#ffa726",
                "delete_button": "#ef5350",
                "clear_button": "#90a4ae",
                "exit_button": "#d32f2f"
            },
            "Forest Green": {
                "header": "#1b5e20",
                "subheader": "#2e7d32",
                "background": "#e8f5e9",
                "add_button": "#4caf50",
                "edit_button": "#ff9800",
                "delete_button": "#f44336",
                "clear_button": "#9e9e9e",
                "exit_button": "#c62828"
            },
            "Purple Sunset": {
                "header": "#4a148c",
                "subheader": "#6a1b9a",
                "background": "#f3e5f5",
                "add_button": "#9c27b0",
                "edit_button": "#ff6f00",
                "delete_button": "#d32f2f",
                "clear_button": "#757575",
                "exit_button": "#b71c1c"
            },
            "Dark Mode": {
                "header": "#1a1a1a",
                "subheader": "#2d2d2d",
                "background": "#2b2b2b",
                "text_color": "#e0e0e0",
                "add_button": "#66bb6a",
                "edit_button": "#ffa726",
                "delete_button": "#ef5350",
                "clear_button": "#757575",
                "exit_button": "#e53935"
            },
            "Sunset Orange": {
                "header": "#e65100",
                "subheader": "#f57c00",
                "background": "#fff3e0",
                "add_button": "#66bb6a",
                "edit_button": "#fdd835",
                "delete_button": "#e53935",
                "clear_button": "#9e9e9e",
                "exit_button": "#c62828"
            },
            "Pink Blossom": {
                "header": "#880e4f",
                "subheader": "#ad1457",
                "background": "#fce4ec",
                "add_button": "#ec407a",
                "edit_button": "#ffa726",
                "delete_button": "#ef5350",
                "clear_button": "#9e9e9e",
                "exit_button": "#c62828"
            },
            "Teal Dream": {
                "header": "#004d40",
                "subheader": "#00695c",
                "background": "#e0f2f1",
                "add_button": "#26a69a",
                "edit_button": "#ffb74d",
                "delete_button": "#ef5350",
                "clear_button": "#90a4ae",
                "exit_button": "#d32f2f"
            }
        }

        # Load theme settings
        self.current_theme = self.load_settings()

        # Create GUI
        self.create_widgets()
        self.refresh_contact_list()

    ## Loading isi kontak
    def load_contacts(self): ## Load contacts from JSON file
        if os.path.exists(self.contacts_file):
            try:
                with open(self.contacts_file, 'r') as f:
                    data = json.load(f)
                    # Handle both old format (dict) and new format (dict with contacts and pinned)
                    if isinstance(data, dict) and 'contacts' in data:
                        self.pinned_contacts = set(data.get('pinned', []))
                        return data['contacts']
                    else:
                        # Old format, just contacts
                        return data
            except:
                return {}
        return {}

    ## Simpan kontak
    def save_contacts(self): ## Save contacts to JSON file
        data = {
            'contacts': self.contacts,
            'pinned': list(self.pinned_contacts)
        }
        with open(self.contacts_file, 'w') as f:
            json.dump(data, f, indent=4)

    ## Loading settingan
    def load_settings(self): ## Load theme settings from JSON file
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    return settings.get('theme', 'Default Blue')
            except:
                return 'Default Blue'
        return 'Default Blue'

    ## Simpan settingan
    def save_settings(self): ## Save theme settings to JSON file
        settings = {'theme': self.current_theme}
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f, indent=4)

    ## Buat widget GUI app
    def create_widgets(self): ## Create all GUI widgets
        # Get current theme colors
        theme = self.themes[self.current_theme]

        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Theme menu
        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Themes", menu=theme_menu)

        for theme_name in self.themes.keys():
            theme_menu.add_command(label=theme_name, command=lambda t=theme_name: self.change_theme(t))

        # Title
        self.title_label = tk.Label(
            self.root,
            text="Contact Book",
            font=("Arial", 24, "bold"),
            bg=theme["header"],
            fg="white",
            pady=15
        )
        self.title_label.pack(fill=tk.X)

        # Main container
        self.main_frame = tk.Frame(self.root, bg=theme["background"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel - Contact list
        self.left_frame = tk.Frame(self.main_frame, bg=theme["background"])
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Search bar
        self.search_frame = tk.Frame(self.left_frame, bg=theme["background"])
        self.search_frame.pack(fill=tk.X, pady=(0, 10))

        text_fg = theme.get("text_color", "black")
        self.search_label = tk.Label(self.search_frame, text="Search:", font=("Arial", 10), bg=theme["background"], fg=text_fg)
        self.search_label.pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.search_contacts())
        search_entry = tk.Entry(self.search_frame, textvariable=self.search_var, font=("Arial", 10), width=30)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Contact listbox with scrollbar
        list_frame = tk.Frame(self.left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.contact_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 10),
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE
        )
        self.contact_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.contact_listbox.yview)

        self.contact_listbox.bind('<<ListboxSelect>>', self.on_contact_select)

        # Right panel - Contact details and actions
        self.right_frame = tk.Frame(self.main_frame, bg=theme["background"], width=400)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        self.right_frame.pack_propagate(False)

        # Contact details section
        self.details_label = tk.Label(
            self.right_frame,
            text="Contact Details",
            font=("Arial", 14, "bold"),
            bg=theme["subheader"],
            fg="white",
            pady=10
        )
        self.details_label.pack(fill=tk.X)

        # Form frame
        self.form_frame = tk.Frame(self.right_frame, bg=theme["background"], pady=20)
        self.form_frame.pack(fill=tk.X, padx=20)

        # Name
        self.name_label = tk.Label(self.form_frame, text="Name:", font=("Arial", 10, "bold"), bg=theme["background"], fg=text_fg)
        self.name_label.grid(row=0, column=0, sticky="w", pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(self.form_frame, textvariable=self.name_var, font=("Arial", 10), width=30)
        self.name_entry.grid(row=0, column=1, pady=5)

        # Phone Number
        self.phone_label = tk.Label(self.form_frame, text="Phone:", font=("Arial", 10, "bold"), bg=theme["background"], fg=text_fg)
        self.phone_label.grid(row=1, column=0, sticky="w", pady=5)
        self.phone_var = tk.StringVar()
        self.phone_entry = tk.Entry(self.form_frame, textvariable=self.phone_var, font=("Arial", 10), width=30)
        self.phone_entry.grid(row=1, column=1, pady=5)

        # Email
        self.email_label = tk.Label(self.form_frame, text="Email:", font=("Arial", 10, "bold"), bg=theme["background"], fg=text_fg)
        self.email_label.grid(row=2, column=0, sticky="w", pady=5)
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(self.form_frame, textvariable=self.email_var, font=("Arial", 10), width=30)
        self.email_entry.grid(row=2, column=1, pady=5)

        # Buttons frame
        self.button_frame = tk.Frame(self.right_frame, bg=theme["background"])
        self.button_frame.pack(fill=tk.X, padx=20, pady=20)

        # Button style
        button_config = {
            'font': ("Arial", 10, "bold"),
            'width': 10,
            'height': 2
        }

        # Add button
        self.add_btn = tk.Button(
            self.button_frame,
            text="Add",
            bg=theme["add_button"],
            fg="white",
            command=self.add_contact,
            **button_config
        )
        self.add_btn.grid(row=0, column=0, padx=5, pady=5)

        # Edit button
        self.edit_btn = tk.Button(
            self.button_frame,
            text="Edit",
            bg=theme["edit_button"],
            fg="white",
            command=self.edit_contact,
            **button_config
        )
        self.edit_btn.grid(row=0, column=1, padx=5, pady=5)

        # Delete button
        self.delete_btn = tk.Button(
            self.button_frame,
            text="Delete",
            bg=theme["delete_button"],
            fg="white",
            command=self.delete_contact,
            **button_config
        )
        self.delete_btn.grid(row=1, column=0, padx=5, pady=5)

        # Clear button
        self.clear_btn = tk.Button(
            self.button_frame,
            text="Clear",
            bg=theme["clear_button"],
            fg="white",
            command=self.clear_fields,
            **button_config
        )
        self.clear_btn.grid(row=1, column=1, padx=5, pady=5)

        # Pin/Unpin button
        self.pin_btn = tk.Button(
            self.button_frame,
            text="Pin",
            bg="#3498db",
            fg="white",
            command=self.toggle_pin_contact,
            **button_config
        )
        self.pin_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Exit button
        self.exit_btn = tk.Button(
            self.button_frame,
            text="Exit",
            bg=theme["exit_button"],
            fg="white",
            command=self.exit_app,
            **button_config
        )
        self.exit_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    ## Refresh app jika ada kontak baru di list
    def refresh_contact_list(self, filtered_contacts=None): # Refresh the contact listbox
        self.contact_listbox.delete(0, tk.END)

        contacts_to_display = filtered_contacts if filtered_contacts is not None else self.contacts

        # Separate pinned and unpinned contacts
        pinned = []
        unpinned = []

        for name in contacts_to_display.keys():
            if name in self.pinned_contacts:
                pinned.append(name)
            else:
                unpinned.append(name)

        # Sort both lists alphabetically
        pinned.sort(key=str.lower)
        unpinned.sort(key=str.lower)

        # Add pinned contacts first with star symbol
        for name in pinned:
            self.contact_listbox.insert(tk.END, f"★ {name}")

        # Add unpinned contacts
        for name in unpinned:
            self.contact_listbox.insert(tk.END, name)

    ## Fitur Search
    def search_contacts(self): # Search contacts by name, phone, or email
        search_term = self.search_var.get().lower()

        if not search_term:
            self.refresh_contact_list()
            return

        filtered = {}
        for name, details in self.contacts.items():
            if (search_term in name.lower() or
                search_term in details.get('phone', '').lower() or
                search_term in details.get('email', '').lower()):
                filtered[name] = details

        self.refresh_contact_list(filtered)

    ## Select kontak
    def on_contact_select(self, event): # Handle contact selection from listbox
        selection = self.contact_listbox.curselection()
        if selection:
            name = self.contact_listbox.get(selection[0])
            # Remove star prefix if present
            if name.startswith("★ "):
                name = name[2:]
            contact = self.contacts.get(name, {})

            self.name_var.set(name)
            self.phone_var.set(contact.get('phone', ''))
            self.email_var.set(contact.get('email', ''))

            # Update pin button text
            if name in self.pinned_contacts:
                self.pin_btn.config(text="Unpin")
            else:
                self.pin_btn.config(text="Pin")

    ## Tambah kontak baru
    def add_contact(self): # Add a new contact
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()

        if not name:
            messagebox.showerror("Error", "Name is required!")
            return

        if not phone and not email:
            messagebox.showerror("Error", "At least one contact method (phone or email) is required!")
            return

        if name in self.contacts:
            messagebox.showerror("Error", f"Contact '{name}' already exists!")
            return

        self.contacts[name] = {
            'phone': phone,
            'email': email
        }

        self.save_contacts()
        self.refresh_contact_list()
        self.clear_fields()
        messagebox.showinfo("Success", f"Contact '{name}' added successfully!")

    ## Edit isi kontak
    def edit_contact(self): # Edit an existing contact
        selection = self.contact_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a contact to edit!")
            return

        old_name = self.contact_listbox.get(selection[0])
        # Remove star prefix if present
        if old_name.startswith("★ "):
            old_name = old_name[2:]

        new_name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()

        if not new_name:
            messagebox.showerror("Error", "Name is required!")
            return

        if not phone and not email:
            messagebox.showerror("Error", "At least one contact method (phone or email) is required!")
            return

        # If name changed, check if new name already exists
        if new_name != old_name and new_name in self.contacts:
            messagebox.showerror("Error", f"Contact '{new_name}' already exists!")
            return

        # Delete old contact if name changed
        if new_name != old_name:
            del self.contacts[old_name]
            # Update pinned contacts if name changed
            if old_name in self.pinned_contacts:
                self.pinned_contacts.remove(old_name)
                self.pinned_contacts.add(new_name)

        # Update contact
        self.contacts[new_name] = {
            'phone': phone,
            'email': email
        }

        self.save_contacts()
        self.refresh_contact_list()
        self.clear_fields()
        messagebox.showinfo("Success", f"Contact updated successfully!")

    ## Fitur Delete Kontak
    def delete_contact(self): # Delete a contact
        selection = self.contact_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a contact to delete!")
            return

        name = self.contact_listbox.get(selection[0])
        # Remove star prefix if present
        if name.startswith("★ "):
            name = name[2:]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{name}'?"
        )

        if confirm:
            del self.contacts[name]
            # Remove from pinned if it was pinned
            if name in self.pinned_contacts:
                self.pinned_contacts.remove(name)
            self.save_contacts()
            self.refresh_contact_list()
            self.clear_fields()
            messagebox.showinfo("Success", f"Contact '{name}' deleted successfully!")

    ## Fitur clear
    def clear_fields(self): # Clear all input fields
        self.name_var.set('')
        self.phone_var.set('')
        self.email_var.set('')
        self.contact_listbox.selection_clear(0, tk.END)

    ## Fitur ubah warna theme
    def change_theme(self, theme_name): # Change the application theme
        self.current_theme = theme_name
        self.save_settings()

        # Get new theme colors
        theme = self.themes[theme_name]
        text_fg = theme.get("text_color", "black")

        # Update all widget colors
        self.title_label.config(bg=theme["header"])
        self.main_frame.config(bg=theme["background"])
        self.left_frame.config(bg=theme["background"])
        self.search_frame.config(bg=theme["background"])
        self.search_label.config(bg=theme["background"], fg=text_fg)
        self.right_frame.config(bg=theme["background"])
        self.details_label.config(bg=theme["subheader"])
        self.form_frame.config(bg=theme["background"])
        self.name_label.config(bg=theme["background"], fg=text_fg)
        self.phone_label.config(bg=theme["background"], fg=text_fg)
        self.email_label.config(bg=theme["background"], fg=text_fg)
        self.button_frame.config(bg=theme["background"])

        # Update button colors
        self.add_btn.config(bg=theme["add_button"])
        self.edit_btn.config(bg=theme["edit_button"])
        self.delete_btn.config(bg=theme["delete_button"])
        self.clear_btn.config(bg=theme["clear_button"])
        self.exit_btn.config(bg=theme["exit_button"])

        messagebox.showinfo("Theme Changed", f"Theme changed to '{theme_name}' successfully!")

    ## Fitur untuk pin beberapa kontak (max = 5 kontak)
    def toggle_pin_contact(self): # Pin or unpin a contact
        selection = self.contact_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a contact to pin/unpin!")
            return

        name = self.contact_listbox.get(selection[0])
        # Remove star prefix if present
        if name.startswith("★ "):
            name = name[2:]

        if name in self.pinned_contacts:
            # Unpin contact
            self.pinned_contacts.remove(name)
            self.save_contacts()
            self.refresh_contact_list()
            self.pin_btn.config(text="Pin")
            messagebox.showinfo("Success", f"Contact '{name}' unpinned!")
        else:
            # Check if limit reached
            if len(self.pinned_contacts) >= 5:
                messagebox.showerror("Error", "You can only pin up to 5 contacts! Please unpin a contact first.")
                return

            # Pin contact
            self.pinned_contacts.add(name)
            self.save_contacts()
            self.refresh_contact_list()
            self.pin_btn.config(text="Unpin")
            messagebox.showinfo("Success", f"Contact '{name}' pinned to top!")

    ## Untuk exit
    def exit_app(self): # Exit application
        confirm = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if confirm:
            self.root.quit()

def main():
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()


####################################################
####################################################
### MEET OUR TEAM:                               ###
### -- FAGA IMAM WICAKSONO (Developer)           ###
### -- ABULLAH AFFAN (Concept creator)           ###
### -- SABRIAN HARTO WINATA (Tester)             ###
### -- FATAHUL FADLAN (Tester)                   ###
####################################################
####################################################