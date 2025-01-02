import tkinter as tk
from tkinter import ttk

import pandas as pd
import udfs as prereq

class PreReqDetect:
    def __init__(self, root):
        self.root = root
        self.root.title("PreReqDetect")

        # Intialize Separated Data Storage
        self.separated = pd.DataFrame()

        # Initialze list
        self.data_list = []

        # Intialize Main Frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Initialize Textbox
        self.textbox = tk.Entry(root, width=50, font=('Arial', 16))
        self.textbox.pack(pady=10)

        # Initialize Add Button
        self.add_button = tk.Button(root, text="Add Class", font=('Arial', 16), command=self.add_to_list)
        self.add_button.pack(pady=5)

        # Initialize Submit Button
        self.submit_button = tk.Button(root, text="Submit Classes",font=('Arial', 16), command=self.submit_list)
        self.submit_button.pack(pady=5)

        # Initialize Second Frame
        self.second_frame = tk.Frame(root)

        # Initialize Reset Button
        #self.reset_button = tk.Button(self.second_frame, text="Reset", command=self.reset_app)
        #self.reset_button.pack(pady=5)

    def add_to_list(self):
        # Extract Text
        item = self.textbox.get()
        if item:
            # Add Text To List
            self.data_list.append(item)
            print(f"Added: {item}")
            
            # Clear Textbox
            self.textbox.delete(0, tk.END)
        else:
            print("Textbox is empty. Nothing to add.")

    def submit_list(self):
        if self.data_list:
            print(f"Submitting list: {self.data_list}")

            # Collected Separated Dataset
            self.separated = prereq.prereq_lister(self.data_list)
            print(self.separated)

            # Hide Buttons and Textbox
            self.textbox.pack_forget()
            self.add_button.pack_forget()
            self.submit_button.pack_forget()
            
            # Load Second Frame
            self.second_frame.pack(fill=tk.BOTH, expand=True)

            # Load sample DataFrame
            self.load_dataframe()
        else:
            print("List is empty. Nothing to submit.")

    def load_dataframe(self):

        for widget in self.second_frame.winfo_children():
            widget.destroy()

        # Example DataFrame
        df = prereq.prereq_lister(self.data_list)

        # Create a Notebook (tabbed interface)
        notebook = ttk.Notebook(self.second_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Create the 'Reset' button below the tabs
        self.reset_button = tk.Button(self.second_frame, text="Reset", command=self.reset_app)
        self.reset_button.pack(side=tk.BOTTOM, pady=10)

        for _, row in df.iterrows():
            # Create a new tab for each title
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=row['title'])

            for col in ['required_courses','choice_list_1','choice_list_2','choice_list_3','choice_list_4','choice_list_5']:
                if col == 'required_courses':
                    if len(row['remaining_'+col]) > 0:
                        list_label = tk.Label(frame, text=str(col.replace('_', ' ') + ' - ' + str(len(row['remaining_'+col])) + ' Remaining').title())
                        list_label.pack(anchor="w", pady=2)

                        for item in row['remaining_'+col]:
                            item_label = tk.Label(frame, text=(f"- {item}").replace('_', ' ').upper(), anchor="w")
                            item_label.pack(anchor="w", padx=10)
                elif row[col+'_num_remaining'] != 0:
                    list_label = tk.Label(frame, text= str(col.replace('_', ' ') + ' - ' + str(row[col+'_num_remaining']) + ' Remaining').title())
                    list_label.pack(anchor="w", pady=2)
                    for item in row['remaining_'+col]:
                        item_label = tk.Label(frame, text=(f"- {item}").replace('_', ' ').upper(), anchor="w")
                        item_label.pack(anchor="w", padx=10)
        

    def reset_app(self):
        # Clear list
        self.data_list.clear()
        print("Resetting app. List cleared.")

        # Clear Separation
        self.separated = pd.DataFrame()

        # Remove Second Frame
        self.second_frame.pack_forget()

        # Return Buttons and Textbox
        self.textbox.pack(pady=10)
        self.add_button.pack(pady=5)
        self.submit_button.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = PreReqDetect(root)
    root.mainloop()

PreReqDetect