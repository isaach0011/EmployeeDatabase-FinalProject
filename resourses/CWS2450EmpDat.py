#CS2450
#Craig Sharp
#EmpDat Project
#3/14/21
from datetime import datetime
import os
import csv
import tkinter as tk
from tkinter import ttk

#start coding here

class LabelData(tk.Frame):
    """frame widget containing label and input"""
    def __init__(self, parent, label='', input_class=ttk.Entry, input_var=None, input_args=None,
                 label_args=None, **kwargs):
        super().__init__(parent, **kwargs)
        input_args=input_args or {}
        label_args = label_args or {}
        self.variable = input_var
        
#code to handle differences between widget variable handling
#the three that we will use first and then any of the others we are using
        
        if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):          
            input_args["text"] = label
            input_args["variable"] = input_var
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))
            input_args["textvariable"] = input_var
    
        self.input = input_class(self,**input_args)
        self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))

#create a 1 wide column

        self.columnconfigure(0, weight=1)

#override the grid method for default grid settings

    def grid(self, sticky=(tk.W + tk.E), **kwargs):
        super().grid(sticky=sticky,**kwargs)
        
#implement a get() method for the LabelInput class
#include a try for some get conditions with Tkinter variables
        
    def get(self):
        #try: indent the following to use this
        if self.variable:
            return self.variable.get()
        elif type(self.input) == tk.Text:
            return self.input.get('1.0', tk.END)
        else:
            return self.input.get()
        # except(TypeError,tk.TclError):
            #happens when numeric feilds are empty
            #return ''
    
#implement a set() method that passes a value to the variable or the widget
        
    def set(self,value,*args,**kwargs):
        if type(self.variable) == tk.BooleanVar:
            self.variable.set(book(value))
        elif self.variable:
            self.variable.set(value, *args, **kwargs)
        #elif type(self.input).__name__.endswith('button'): #???
        elif type(self.input) in (ttk.Checkbutton,ttk.Radiobutton):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        #remove any existing text and replace with required text        
        elif type(self.input) == tk.Text:
            self.input.delete('1.0', tk.END)
            self.input.insert('1.0', value)
        else: #this has to be an Entry-type with no variable
            self.input.delete(0,tk.END)
            self.input.insert(0,value)
            
class AdminForm(tk.Frame):
    """Main overall input form that contains the required widgets"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
            
#dict to hold widgets
        self.inputs = {}
    
        recordAdmin = tk.LabelFrame(self, text="Admin Information")
    
        self.inputs['EmpID'] = LabelData(recordAdmin, "EmpID", input_var=tk.StringVar())
        self.inputs['EmpID'].grid(row=0,column=0)
        self.inputs['First'] = LabelData(recordAdmin, "First", input_var=tk.StringVar())
        self.inputs['First'].grid(row=0,column=1)
        self.inputs['Last'] = LabelData(recordAdmin, "Last", input_var=tk.StringVar())
        self.inputs['Last'].grid(row=0,column=2)
        self.inputs['Dept'] = LabelData(recordAdmin, "Dept", input_var=tk.StringVar())
        self.inputs['Dept'].grid(row=1,column=0)
        self.inputs['Title'] = LabelData(recordAdmin, "Title", input_var=tk.StringVar())
        self.inputs['Title'].grid(row=1,column=1)
        self.inputs['OffEmail'] = LabelData(recordAdmin, "OffEmail", input_var=tk.StringVar())
        self.inputs['OffEmail'].grid(row=1,column=2)
    
        recordAdmin.grid(row=0, column=0, sticky = (tk.W + tk.E))
        
        self.inputs['Notes'] = LabelData(self, "Notes", input_class=tk.Text, input_args={"width": 75, "height": 10})
        
        self.inputs['Notes'].grid(sticky=tk.W, row=3, column=0)
        
        self.reset()
        
    def get(self):
        """retrieve data from form as dictionary"""
        #Note: translate to final data file order
        #What to do if only updating one field
        #following works for adding a record.
        
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data
    
    def reset(self):
        """Resets the form entries"""
        
        #clear all values
        for widget in self.inputs.values():
            widget.set('')

        
class EmpDat(tk.Tk):
    """App root window"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Employee Pay Manager")
        self.resizable(width=False, height=False)
        
        ttk.Label(self, text="Employee Pay Manager", font=("TkDefaultFont", 16)).grid(row=0)
        
        self.recordform=AdminForm(self)
        self.recordform.grid(row=1, padx=10)
        self.savebutton=ttk.Button(self, text="Save", command=self.on_save)
        self.savebutton.grid(sticky=tk.E, row=2, padx=10)
        
        self.status=tk.StringVar()
        self.statusbar = ttk.Label(self,textvariable=self.status)
        self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)
        
        self.records_saved = 0
        
    def on_save(self):
        """Handles save button clicks"""
        #can save to a hardcoded file name with date
        #appends to existing file or creates one
        #might be good choice for intermediate check the content file
        
        datestring = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = "EmpPayManager_check_{}.csv".format(datestring)
        newfile = not os.path.exists(filename)
        
        data = self.recordform.get()
        
        with open(filename, 'a') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)
        
        self.record_saved +=1
        self.status.set("{} records saved this session".format(self.records_saved))
        self.recordform.reset()
        
        
        
        
if __name__ == "__main__":
    app = EmpDat()
    app.mainloop()