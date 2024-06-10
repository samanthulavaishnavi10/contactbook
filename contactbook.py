import tkinter as tk
from tkinter import messagebox, simpledialog
import pickle

class ContactManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")

        self.contacts = {}
        self.load_contacts()
        self.create_widgets()

    def create_widgets(self):
        details_frame = tk.Frame(self.root)
        details_frame.pack(pady=10)

        tk.Label(details_frame, text='Name:').grid(row=0, column=0)
        self.name_entry = tk.Entry(details_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(details_frame, text="Phone:").grid(row=1, column=0)
        self.phone_entry = tk.Entry(details_frame)
        self.phone_entry.grid(row=1, column=1)

        tk.Label(details_frame, text="Email:").grid(row=2, column=0)
        self.email_entry = tk.Entry(details_frame)
        self.email_entry.grid(row=2, column=1)

        tk.Label(details_frame, text="Address:").grid(row=3, column=0)
        self.address_entry = tk.Entry(details_frame)
        self.address_entry.grid(row=3, column=1)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Contact", command=self.add_contact).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="View Contact", command=self.view_contacts).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Search Contact", command=self.search_contact).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Update Contact", command=self.update_contact).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Delete Contact", command=self.delete_contact).grid(row=0, column=4, padx=5)
        
        self.contact_listbox = tk.Listbox(self.root, width=50, height=10)
        self.contact_listbox.pack(pady=0)
        self.contact_listbox.bind('<<ListboxSelect>>', self.on_contact_select)

    def load_contacts(self):
        try:
            with open('contacts.pkl', 'rb') as f:
                self.contacts = pickle.load(f)
        except FileNotFoundError:
            self.contacts = {}

    def save_contacts(self):
        with open('contacts.pkl', 'wb') as f:
            pickle.dump(self.contacts, f)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if name and phone:
            self.contacts[phone] = {"name": name, "phone": phone, "email": email, "address": address}
            self.save_contacts()
            self.view_contacts()
            self.clear_entries()                      
            messagebox.showinfo("Succcess", "Contact added successfully!")
        else:
            messagebox.showerror("Error", "Name and phone number are required.")

    def view_contacts(self):
        self.contact_listbox.delete(0, tk.END)
        for contact in self.contacts.values():
            self.contact_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")   

    def search_contact(self):
        search_query = simpledialog.askstring("Search Contact", "Enter name or phone number:")
        if search_query:
            self.contact_listbox.delete(0, tk.END)
            for contact in self.contacts.values():
                if search_query.lower() in contact['name'].lower() or search_query in contact['phone']:
                    self.contact_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

    def update_contact(self):
        selected_contact = self.contact_listbox.curselection()
        if selected_contact:
            phone = self.contact_listbox.get(selected_contact).split(' - ')[1]
            if phone in self.contacts:
                name = self.name_entry.get()
                email = self.email_entry.get()
                address = self.address_entry.get()
                if name:
                    self.contacts[phone]['name'] = name
                if email:
                    self.contacts[phone]['email'] = email
                if address:
                    self.contacts[phone]['address'] = address
                self.save_contacts()
                self.view_contacts()
                self.clear_entries()
                messagebox.showinfo("Success", "Contact updated successfully1")  
            else:
                messagebox.showerror("Error", "Contact not found.")
        else:
            messagebox.showerror("Eroor", "Please select a contact to update.")

    def delete_contact(self):
        selected_contact = self.contact_listbox.curselection()
        if selected_contact:
            phone = self.contact_listbox.get(selected_contact).split(' - ')[1]
            if phone in self.contacts:
                del self.contacts[phone]
                self.save_contacts()
                self.view_contacts()
                self.clear_entries()
                messagebox.showinfo("Success", "Contact deleted successfully!")
            else:
                messagebox.showerror("Error", "Contact not found.")
        else:
            messagebox.showerror("Error", "Please selet a contact to delete.")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END) 
        self.phone_entry.delete(0, tk.END)  
        self.email_entry.delete(0, tk.END)  
        self.address_entry.delete(0, tk.END)  

    def on_contact_select(self, event):
        selected_contact = self.contact_listbox.curselection()
        if selected_contact:
            phone = self.contact_listbox.get(selected_contact).split(' - ')[1]
            contact = self.contacts.get(phone)
            if contact:
                self.name.entry.delete(0, tk.END)
                self.name_entry.insert(0, contact['name'])
                self.phone.entry.delete(0, tk.END)
                self.phone_entry.insert(0, contact['phone'])
                self.email.entry.delete(0, tk.END)
                self.name_entry.insert(0, contact['email'])
                self.address.entry.delete(0, tk.END)
                self.address_entry.insert(0, contact['address'])

if __name__ == "__main__":
    root =tk.Tk()
    app = ContactManagerApp(root)
    root.mainloop()