import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import font as tkfont
import csv

CONTACTS_FILE = "contacts.json"

class ContactManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")
        self.root.configure(bg="#ADD8E6")  # Light blue background

        # Load contacts
        self.contacts = self.load_contacts()

        # Set stylish font
        self.custom_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

        # Create the main frame
        self.frame = tk.Frame(root, bg="#ADD8E6")
        self.frame.pack(pady=10)

        # Search bar
        search_frame = tk.Frame(self.frame, bg="#ADD8E6")
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Search:", font=self.custom_font, bg="#ADD8E6").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, font=self.custom_font, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=10)
        self.search_button = tk.Button(search_frame, text="Search", command=self.search_contacts, font=self.custom_font, bg="#2196F3", fg="white", activebackground="#1e88e5")
        self.search_button.pack(side=tk.LEFT)
        self.search_button.bind("<Enter>", self.on_enter)
        self.search_button.bind("<Leave>", self.on_leave)
        self.show_all_button = tk.Button(search_frame, text="Show All", command=self.refresh_contacts_list, font=self.custom_font, bg="#ff9800", fg="white", activebackground="#fb8c00")
        self.show_all_button.pack(side=tk.LEFT, padx=5)
        self.show_all_button.bind("<Enter>", self.on_enter)
        self.show_all_button.bind("<Leave>", self.on_leave)

        # Create a listbox to display contacts
        self.listbox = tk.Listbox(self.frame, width=50, height=15, font=self.custom_font, bg="#FFFAF0")
        self.listbox.pack(side=tk.LEFT, padx=10)
        self.refresh_contacts_list()

        # Create a scrollbar for the listbox
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Create button frame for actions
        button_frame = tk.Frame(root, bg="#ADD8E6")
        button_frame.pack(pady=10)

        self.add_button = tk.Button(button_frame, text="Add Contact", command=self.add_contact_window, font=self.custom_font, bg="#4CAF50", fg="white", activebackground="#45a049")
        self.add_button.grid(row=0, column=0, padx=5)
        self.add_button.bind("<Enter>", self.on_enter)
        self.add_button.bind("<Leave>", self.on_leave)

        self.edit_button = tk.Button(button_frame, text="Edit Contact", command=self.edit_contact_window, font=self.custom_font, bg="#2196F3", fg="white", activebackground="#1e88e5")
        self.edit_button.grid(row=0, column=1, padx=5)
        self.edit_button.bind("<Enter>", self.on_enter)
        self.edit_button.bind("<Leave>", self.on_leave)

        self.delete_button = tk.Button(button_frame, text="Delete Contact", command=self.delete_contact, font=self.custom_font, bg="#f44336", fg="white", activebackground="#e53935")
        self.delete_button.grid(row=0, column=2, padx=5)
        self.delete_button.bind("<Enter>", self.on_enter)
        self.delete_button.bind("<Leave>", self.on_leave)

        self.sort_button = tk.Button(button_frame, text="Sort Contacts", command=self.sort_contacts, font=self.custom_font, bg="#009688", fg="white", activebackground="#00897b")
        self.sort_button.grid(row=0, column=3, padx=5)
        self.sort_button.bind("<Enter>", self.on_enter)
        self.sort_button.bind("<Leave>", self.on_leave)

        self.export_button = tk.Button(button_frame, text="Export Contacts", command=self.export_contacts, font=self.custom_font, bg="#FFEB3B", fg="black", activebackground="#fdd835")
        self.export_button.grid(row=0, column=4, padx=5)
        self.export_button.bind("<Enter>", self.on_enter)
        self.export_button.bind("<Leave>", self.on_leave)

        self.exit_button = tk.Button(button_frame, text="Exit", command=root.quit, font=self.custom_font, bg="#ff9800", fg="white", activebackground="#fb8c00")
        self.exit_button.grid(row=0, column=5, padx=5)
        self.exit_button.bind("<Enter>", self.on_enter)
        self.exit_button.bind("<Leave>", self.on_leave)

    def load_contacts(self):
        if not os.path.exists(CONTACTS_FILE):
            return []
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)

    def save_contacts(self):
        with open(CONTACTS_FILE, "w") as file:
            json.dump(self.contacts, file, indent=4)

    def refresh_contacts_list(self):
        self.listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.listbox.insert(tk.END, f"{contact['name']} - {contact['phone']} - {contact['email']}")

    def search_contacts(self):
        search_term = self.search_entry.get().lower()
        if search_term:
            filtered_contacts = [contact for contact in self.contacts if search_term in contact['name'].lower()]
            self.listbox.delete(0, tk.END)
            for contact in filtered_contacts:
                self.listbox.insert(tk.END, f"{contact['name']} - {contact['phone']} - {contact['email']}")
        else:
            self.refresh_contacts_list()

    def add_contact_window(self):
        self.open_contact_window("Add Contact")

    def edit_contact_window(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            contact = self.contacts[index]
            self.open_contact_window("Edit Contact", contact, index)
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to edit.")

    def open_contact_window(self, title, contact=None, index=None):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.configure(bg="#ADD8E6")

        tk.Label(window, text="Name:", font=self.custom_font, bg="#ADD8E6").grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(window, font=self.custom_font, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(window, text="Phone:", font=self.custom_font, bg="#ADD8E6").grid(row=1, column=0, padx=10, pady=5)
        phone_entry = tk.Entry(window, font=self.custom_font, width=30)
        phone_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(window, text="Email:", font=self.custom_font, bg="#ADD8E6").grid(row=2, column=0, padx=10, pady=5)
        email_entry = tk.Entry(window, font=self.custom_font, width=30)
        email_entry.grid(row=2, column=1, padx=10, pady=5)

        if contact:
            name_entry.insert(0, contact["name"])
            phone_entry.insert(0, contact["phone"])
            email_entry.insert(0, contact["email"])

        def save_contact():
            name = name_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()

            if not name or not phone or not email:
                messagebox.showerror("Input Error", "All fields are required.")
                return

            new_contact = {"name": name, "phone": phone, "email": email}

            if contact:
                self.contacts[index] = new_contact
            else:
                self.contacts.append(new_contact)

            self.save_contacts()
            self.refresh_contacts_list()
            window.destroy()

        save_button = tk.Button(window, text="Save", font=self.custom_font, bg="#4CAF50", fg="white", activebackground="#45a049", command=save_contact)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)
        save_button.bind("<Enter>", self.on_enter)
        save_button.bind("<Leave>", self.on_leave)

    def delete_contact(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            confirm = messagebox.askyesno("Delete Contact", "Are you sure you want to delete this contact?")
            if confirm:
                self.contacts.pop(index)
                self.save_contacts()
                self.refresh_contacts_list()
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")

    def sort_contacts(self):
        self.contacts.sort(key=lambda x: x["name"].lower())
        self.save_contacts()
        self.refresh_contacts_list()

    def export_contacts(self):
        with open("contacts.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Phone", "Email"])
            for contact in self.contacts:
                writer.writerow([contact["name"], contact["phone"], contact["email"]])
        messagebox.showinfo("Export Successful", "Contacts have been exported to contacts.csv")

    def on_enter(self, event):
        event.widget.config(fg="#FFD700")  # Change text color to gold on hover

    def on_leave(self, event):
        event.widget.config(fg="white")  # Change text color back to white when not hovered

def main():
    root = tk.Tk()
    app = ContactManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

