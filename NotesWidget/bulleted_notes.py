import tkinter as tk
from tkinter import ttk
from tkinter import messagebox



class BulletedNotes(ttk.Treeview):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<ButtonPress-1>", self.b_down)
        self.bind("<ButtonRelease-1>", self.b_up, add='+')
        self.bind("<B1-Motion>", self.b_move, add='+')
        self.bind("<Shift-ButtonPress-1>", self.b_down_shift, add='+')
        self.bind("<Shift-ButtonRelease-1>", self.b_up_shift, add='+')
        self.bind("<Shift-KeyPress-Up>", lambda e: self.move_note(e, "up"))
        self.bind("<Shift-KeyPress-Down>", lambda e: self.move_note(e, "down"))
        self.bind("<Shift-Left>", lambda e: self.move_note(e, "left"))
        self.bind("<Shift-Right>", lambda e: self.move_note(e, "right"))
        self.bind("<Delete>", self.note_delete)

    def b_down_shift(self, event):
        tv = event.widget
        select = [tv.index(s) for s in tv.selection()]
        select.append(tv.index(tv.identify_row(event.y)))
        select.sort()
        for i in range(select[0], select[-1] + 1, 1):
            tv.selection_add(tv.get_children()[i])

    def b_down(self, event):
        tv = event.widget
        if tv.identify_row(event.y) not in tv.selection():
            tv.selection_set(tv.identify_row(event.y))

    def b_up(self, event):
        tv = event.widget
        if tv.identify_row(event.y) in tv.selection():
            tv.selection_set(tv.identify_row(event.y))

    def b_up_shift(self, event):
        pass

    def b_move(self, event):
        tv = event.widget
        moveto = tv.index(tv.identify_row(event.y))
        for s in tv.selection():
            tv.move(s, '', moveto)

    def move_note(self, event, d):
        tv = event.widget
        focused = tv.focus()
        selected = self.selection()
        first_selected_index = tv.index(selected[0])
        last_selected_index = tv.index(selected[-1])
        if d.lower() == "up":
            for item in selected:
                index = tv.index(item)
                tv.move(item, tv.parent(tv.prev(item)), index-1)
            #tv.focus(tv.next(focused))
        elif d.lower() == "down":
            for item in selected:
                index = tv.index(item)
                tv.move(item, tv.parent(tv.next(item)), last_selected_index+1)
            #tv.focus(tv.prev(focused))
        elif d.lower() == "left":
            for item in selected:
                index = tv.index(tv.parent(item)) + 1
                if tv.parent(item) is not '':
                    tv.move(item, tv.parent(tv.parent(item)), index)
        elif d.lower() == "right":
            for item in selected:
                index = tv.index(item)
                if tv.prev(item) is not '':
                    tv.move(item, tv.prev(item), index)
        #selected = tv.selection()
        tv.after_idle(lambda: tv.selection_set(selected))
        tv.after_idle(lambda: tv.focus(focused))
        return None

    def note_delete(self, event):
        tv = event.widget
        if messagebox.askokcancel("Confirm Deletion", "This will delete the selected notes and all subnotes!",
                                  parent=self):
            selected = tv.selection()
            for item in selected:
                try:
                    tv.delete(item)
                except tk.TclError as err:
                    pass
# TODO: Figure out way to link an entry box and text in a treeview item. Maybe need to subclass stringvar?
# TODO: Make double-click on item in Treeview spawn an Entry over the item and update the item text from the Entry
# TODO: Bind Enter to Create New Child
# TODO: Right click menu
# TODO: Top Menu Bar? Best done in outer window
#        view options: Expand/collapse all, search, themes?
# TODO: Save/Load or it's all useless
# TODO: Potentially create a overload of the insert function to allow inserting direct from entry?
#       would need to associate text to both stringvar and item
