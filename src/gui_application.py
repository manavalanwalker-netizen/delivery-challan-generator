import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import os
from src.pdf_generator import DeliveryChallanPDFGenerator

class DeliveryChallanApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Delivery Challan PDF Generator")
        self.root.geometry("800x900")
        self.root.resizable(True, True)
        
        # Initialize PDF generator
        self.pdf_generator = DeliveryChallanPDFGenerator()
        
        # Create GUI elements
        self.setup_gui()
        
        # Store form data
        self.form_data = {}
        
    def setup_gui(self):
        # Main container with scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas and scrollbar for scrolling
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Title
        title_label = ttk.Label(scrollable_frame, text="Delivery Challan Generator", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Company Information Section
        company_frame = ttk.LabelFrame(scrollable_frame, text="Company Information", padding=10)
        company_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.create_company_fields(company_frame)
        
        # Customer Information Section
        customer_frame = ttk.LabelFrame(scrollable_frame, text="Customer Information", padding=10)
        customer_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.create_customer_fields(customer_frame)
        
        # Delivery Details Section
        delivery_frame = ttk.LabelFrame(scrollable_frame, text="Delivery Details", padding=10)
        delivery_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.create_delivery_fields(delivery_frame)
        
        # Items Section
    def create_items_section(self, parent):
        # Items list
        self.items_list = []
        
        # Headers
        headers_frame = ttk.Frame(parent)
        headers_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(headers_frame, text="S.No.", width=8).pack(side=tk.LEFT, padx=2)
        ttk.Label(headers_frame, text="Description", width=40).pack(side=tk.LEFT, padx=2)
        ttk.Label(headers_frame, text="Qty", width=10).pack(side=tk.LEFT, padx=2)
        ttk.Label(headers_frame, text="Remarks", width=20).pack(side=tk.LEFT, padx=2)
        
        # Items container
        self.items_container = ttk.Frame(parent)
        self.items_container.pack(fill=tk.X)
        
        # Add item button
        ttk.Button(parent, text="Add Item", command=self.add_item).pack(pady=10)
        
        # Add first item by default
        self.add_item()
        
    def add_item(self):
        item_frame = ttk.Frame(self.items_container)
        item_frame.pack(fill=tk.X, pady=2)
        
        item_no = len(self.items_list) + 1
        
        s_no = ttk.Entry(item_frame, width=8)
        s_no.pack(side=tk.LEFT, padx=2)
        s_no.insert(0, str(item_no))
        
        description = ttk.Entry(item_frame, width=40)
        description.pack(side=tk.LEFT, padx=2)
        
        qty = ttk.Entry(item_frame, width=10)
        qty.pack(side=tk.LEFT, padx=2)
        
        remarks = ttk.Entry(item_frame, width=20)
        remarks.pack(side=tk.LEFT, padx=2)
        
        remove_btn = ttk.Button(item_frame, text="Remove", 
                               command=lambda: self.remove_item(item_frame))
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        item_data = {
            'frame': item_frame,
            's_no': s_no,
            'description': description,
            'qty': qty,
            'remarks': remarks
        }
        
        self.items_list.append(item_data)
        
    def remove_item(self, item_frame):
        for i, item in enumerate(self.items_list):
            if item['frame'] == item_frame:
                item_frame.destroy()
                self.items_list.pop(i)
                break
        
        # Update serial numbers
        for i, item in enumerate(self.items_list):
            item['s_no'].delete(0, tk.END)
            item['s_no'].insert(0, str(i + 1))
    
    def create_field(self, parent, label_text, default_value="", side=tk.TOP, width=30):
        if side == tk.LEFT:
            frame = ttk.Frame(parent)
            frame.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            ttk.Label(frame, text=label_text).pack()
            entry = ttk.Entry(frame, width=width)
            entry.pack(fill=tk.X)
        else:
            ttk.Label(parent, text=label_text).pack(anchor=tk.W, pady=(10, 0))
            entry = ttk.Entry(parent, width=width)
            entry.pack(fill=tk.X, pady=(0, 5))
        
        if default_value:
            entry.insert(0, default_value)
        
        return entry
    
    def create_text_field(self, parent, label_text, default_value=""):
        ttk.Label(parent, text=label_text).pack(anchor=tk.W, pady=(10, 0))
        text_widget = tk.Text(parent, height=3)
        text_widget.pack(fill=tk.X, pady=(0, 5))
        
        if default_value:
            text_widget.insert(tk.END, default_value)
        
        return text_widget
    
    def collect_form_data(self):
        # Collect all form data
        data = {
            'company': {
                'name': self.company_name.get(),
                'address': self.company_address.get("1.0", tk.END).strip(),
                'phone': self.company_phone.get(),
                'gstin': self.company_gstin.get()
            },
            'customer': {
                'name': self.customer_name.get(),
                'address': self.customer_address.get("1.0", tk.END).strip()
            },
            'delivery': {
                'challan_no': self.challan_no.get(),
                'date': self.challan_date.get(),
                'transporter': self.transporter.get(),
                'lr_no': self.lr_no.get(),
                'lr_date': self.lr_date.get(),
                'vehicle_no': self.vehicle_no.get(),
                'order_no': self.order_no.get(),
                'order_date': self.order_date.get()
            },
            'items': []
        }
        
        # Collect items data
        for item in self.items_list:
            if item['description'].get().strip():  # Only add non-empty items
                data['items'].append({
                    's_no': item['s_no'].get(),
                    'description': item['description'].get(),
                    'qty': item['qty'].get(),
                    'remarks': item['remarks'].get()
                })
        
        return data
    
    def generate_pdf(self):
        try:
            # Collect form data
            form_data = self.collect_form_data()
            
            # Validate required fields
            if not form_data['customer']['name']:
                messagebox.showerror("Error", "Customer name is required!")
                return
            
            if not form_data['delivery']['challan_no']:
                messagebox.showerror("Error", "Challan number is required!")
                return
            
            if not form_data['items']:
                messagebox.showerror("Error", "At least one item is required!")
                return
            
            # Ask user where to save the PDF
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save Delivery Challan PDF"
            )
            
            if filename:
                # Generate PDF
                self.pdf_generator.generate_challan_pdf(form_data, filename)
                messagebox.showinfo("Success", f"PDF generated successfully!\nSaved as: {filename}")
                
                # Ask if user wants to open the PDF
                if messagebox.askyesno("Open PDF", "Would you like to open the generated PDF?"):
                    os.startfile(filename)  # Windows
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}")
    
    def clear_form(self):
        # Clear all fields except company info
        self.customer_name.delete(0, tk.END)
        self.customer_address.delete("1.0", tk.END)
        
        self.challan_no.delete(0, tk.END)
        self.transporter.delete(0, tk.END)
        self.lr_no.delete(0, tk.END)
        self.lr_date.delete(0, tk.END)
        self.vehicle_no.delete(0, tk.END)
        self.order_no.delete(0, tk.END)
        self.order_date.delete(0, tk.END)
        
        # Clear items
        for item in self.items_list:
            item['frame'].destroy()
        self.items_list.clear()
        
        # Add one empty item
        self.add_item()
    
    def load_sample_data(self):
        # Load sample data for testing
        self.customer_name.delete(0, tk.END)
        self.customer_name.insert(0, "ABC Electronics Pvt. Ltd.")
        
        self.customer_address.delete("1.0", tk.END)
        self.customer_address.insert(tk.END, "123, Electronic City,\nBangalore - 560100,\nKarnataka")
        
        self.challan_no.delete(0, tk.END)
        self.challan_no.insert(0, "DC/2025/001")
        
        self.transporter.delete(0, tk.END)
        self.transporter.insert(0, "XYZ Transport")
        
        self.lr_no.delete(0, tk.END)
        self.lr_no.insert(0, "LR123456")
        
        self.lr_date.delete(0, tk.END)
        self.lr_date.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        self.vehicle_no.delete(0, tk.END)
        self.vehicle_no.insert(0, "MH 12 AB 1234")
        
        self.order_no.delete(0, tk.END)
        self.order_no.insert(0, "PO/2025/001")
        
        self.order_date.delete(0, tk.END)
        self.order_date.insert(0, "20/09/2025")
        
        # Add sample items
        if self.items_list:
            self.items_list[0]['description'].delete(0, tk.END)
            self.items_list[0]['description'].insert(0, "Power Supply Unit")
            self.items_list[0]['qty'].delete(0, tk.END)
            self.items_list[0]['qty'].insert(0, "2")
            self.items_list[0]['remarks'].delete(0, tk.END)
            self.items_list[0]['remarks'].insert(0, "Good condition")
    
    def run(self):
        self.root.mainloop()
