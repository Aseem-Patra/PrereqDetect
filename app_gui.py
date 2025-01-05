import tkinter as tk
from tkinter import ttk

import pandas as pd
from fuzzywuzzy import fuzz
import udfs as prereq

class PreReqDetect:
    def __init__(self, root):
        self.root = root
        self.root.title("PreReqDetect: Finding Your Requirements, No Matter How Minor.")

        self.title_label = tk.Label(root, text="PreReq Detect", font=("Arial", 32, "bold"))
        self.title_label.pack(pady=20)

# SCREEN 1

        # Course List
        self.data_list = []

        #  Main Frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # AutoCompleteBox Widgets
        self.suggestions = prereq.course_lister()

        self.entry = tk.Entry(root, width=50, font=('Arial', 16))
        self.entry.pack(padx=10, pady=10)
        self.entry.bind("<KeyRelease>", self.show_suggestions)
        self.entry.bind("<FocusOut>", self.hide_suggestions)

        self.listbox = None
        self.scrollbar = None

        # Add Button
        self.add_button = tk.Button(root, text="Add Class", font=('Arial', 16), command=self.add_to_list)
        self.add_button.pack(pady=5)

        # Submit Button
        self.submit_button = tk.Button(root, text="Submit Classes",font=('Arial', 16), command=self.submit_list)
        self.submit_button.pack(pady=5)

# SCREEN 2

        # Second Frame
        self.second_frame = tk.Frame(root)

        # Separated Course Data
        self.separated = pd.DataFrame()


    # AutoCompleteText Functions
    def show_suggestions(self, event=None):
        text = self.entry.get()

        if not text:  # If no input, hide suggestions
            self.hide_suggestions()
            return

        # Find matching suggestions and calculate similarity
        matching_suggestions = [(s, fuzz.ratio(text.lower(), s.lower())) for s in self.suggestions if text.lower() in s.lower()]

        # Sort by the similarity score (higher is more similar)
        matching_suggestions.sort(key=lambda x: x[1], reverse=True)

        if not matching_suggestions:  # Hide if no matches
            self.hide_suggestions()
            return

        if not self.listbox: 
            self.listbox = tk.Listbox(self.root, height=6)
            self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.listbox.yview)
            self.listbox.config(yscrollcommand=self.scrollbar.set)
            self.listbox.place(x=self.entry.winfo_x(), y=self.entry.winfo_y() + self.entry.winfo_height(), width=self.entry.winfo_width())
            self.scrollbar.place(x=self.entry.winfo_x() + self.entry.winfo_width(), y=self.entry.winfo_y() + self.entry.winfo_height(), height=100)

        self.listbox.delete(0, tk.END)

        # Insert the sorted suggestions into the listbox
        for i, (suggestion, score) in enumerate(matching_suggestions):
            self.listbox.insert(tk.END, suggestion)

            # Bind the motion event to handle hover
            self.listbox.bind("<Motion>", lambda event: self.on_hover(event))

            # Bind the click event to fill the entry with the clicked suggestion
            self.listbox.bind("<Button-1>", lambda event, index=i: self.select_suggestion(event, self.listbox.nearest(event.y)))

        # Track the current hovered index
        self.hovered_index = None

    def on_hover(self, event):
        # Get the index of the item under the mouse pointer
        index = self.listbox.nearest(event.y)  # Get the closest item index to the y-coordinate

        # Only highlight if the item has changed
        if index != self.hovered_index:
            if self.hovered_index is not None:
                # Reset the previous hovered item
                self.listbox.itemconfig(self.hovered_index, {'bg': 'white'})

            # Highlight the new hovered item
            self.listbox.itemconfig(index, {'bg': 'lightgray'})
            self.hovered_index = index  # Update the currently hovered index

    def on_leave(self, event, index):
        # Reset the item back to its normal background when leaving
        self.listbox.itemconfig(index, {'bg': 'white'})

    def hide_suggestions(self, event=None):
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None

    def select_suggestion(self, event, index):
        # Get the clicked suggestion based on the index
        selected = self.listbox.get(index)
        
        # Autofill the entry with the selected suggestion
        self.entry.delete(0, tk.END)
        self.entry.insert(0, selected)

        # Hide suggestions after selecting
        self.hide_suggestions()


    # Display Tab Functions 
    def load_dataframe(self):

        # Remove Added Widgets from Second Frame
        for widget in self.second_frame.winfo_children():
            widget.destroy()

        # Results DataFrame
        df = prereq.prereq_lister(self.data_list)

        # Create a Notebook (tabbed interface)
        notebook = ttk.Notebook(self.second_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Add Reset button below the tabs
        self.reset_button = tk.Button(self.second_frame, text="Reset", command=self.reset_app)
        self.reset_button.pack(side=tk.BOTTOM, pady=10)

        # Iterate through each row
        for _, row in df.iterrows():
            # Create a new tab for each title
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=row['title'])

            #Check through each course list
            for col in ['required_courses','choice_list_1','choice_list_2','choice_list_3','choice_list_4','choice_list_5']:
                #Check if over required courses column
                if col == 'required_courses':
                    # Check for remaining courses and add list title
                    if len(row['remaining_'+col]) > 0:
                        list_label = tk.Label(frame, text=str(col.replace('_', ' ') + ' - ' + str(len(row['remaining_'+col])) + ' Remaining').title())
                        list_label.pack(anchor="w", pady=2)

                        # List out each remaining required course
                        for item in row['remaining_'+col]:
                            item_label = tk.Label(frame, text=(f"- {item}").replace('_', ' ').upper(), anchor="w")
                            item_label.pack(anchor="w", padx=10)
                #Check other lists for remaining courses and add list titles
                elif row[col+'_num_remaining'] != 0:
                    list_label = tk.Label(frame, text= str(col.replace('_', ' ') + ' - ' + str(row[col+'_num_remaining']) + ' Remaining').title())
                    list_label.pack(anchor="w", pady=2)
                    # List out each remaining required course
                    for item in row['remaining_'+col]:
                        item_label = tk.Label(frame, text=(f"- {item}").replace('_', ' ').upper(), anchor="w")
                        item_label.pack(anchor="w", padx=10)
        
    # Button Functions
    def add_to_list(self):
        # Extract Text
        item = self.entry.get()
        if item:
            # Add Text To List
            self.data_list.append(item)
            print(f"Added: {item}")
            
            # Clear Textbox
            self.entry.delete(0, tk.END)
        else:
            print("Textbox is empty. Nothing to add.")

    def submit_list(self):
        if self.data_list:
            print(f"Submitting list: {self.data_list}")

            # Collected Separated Dataset
            self.separated = prereq.prereq_lister(self.data_list)
            print(self.separated)

            # Hide Buttons and Textbox
            self.title_label.pack_forget()
            self.entry.pack_forget()
            self.add_button.pack_forget()
            self.submit_button.pack_forget()
            
            # Load Second Frame
            self.second_frame.pack(fill=tk.BOTH, expand=True)

            # Load sample DataFrame
            self.load_dataframe()
        else:
            print("List is empty. Nothing to submit.")

    def reset_app(self):
        # Clear list
        self.data_list.clear()
        print("Resetting app. List cleared.")

        # Clear Separation
        self.separated = pd.DataFrame()

        # Remove Second Frame
        self.second_frame.pack_forget()

        # Return Buttons and Textbox
        self.title_label.pack(pady=20)
        self.entry.pack(padx=10, pady=10)
        self.add_button.pack(pady=5)
        self.submit_button.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = PreReqDetect(root)
    root.mainloop()

PreReqDetect