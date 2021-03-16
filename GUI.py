import tkinter as tk
from tkinter import ttk, filedialog

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the body portion of the root frame.
"""
class Body(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        # a list of the User objects available in the active DSU file
        self._users = []
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
        self.msg_view.config(state='disabled')
    
    """
    Update the msg_editor with the full post entry when the corresponding node in the posts_tree
    is selected.
    """
    def node_select(self, event):
        index = int(self.users_tree.selection()[0])-1 #selections are not 0-based, so subtract one.
        entry = self._users[index].entry
        self.set_text_entry(entry)
    
    """
    Returns the text that is currently displayed in the msg_editor widget.
    """
    def get_text_entry(self) -> str:
        return self.msg_editor.get('1.0', 'end').rstrip()

    """
    Sets the text to be displayed in the msg_editor widget.
    NOTE: This method is useful for clearing the widget, just pass an empty string.
    """
    def set_text_entry(self, text:str):
        # TODO: Write code to that deletes all current text in the self.msg_editor widget
        # and inserts the value contained within the text parameter.
        self.msg_editor.delete(0.0, 'end')
        self.msg_editor.insert(0.0, text)
    
    """
    Populates the self._posts attribute with posts from the active DSU file.
    """
    def set_users(self, posts:list):
        # TODO: Write code to populate self._posts with the post data passed
        # in the posts parameter and repopulate the UI with the new post entries.
        # HINT: You will have to write the delete code yourself, but you can take 
        # advantage of the self.insert_posttree method for updating the posts_tree
        # widget.
        self._users = posts[:]
        count = 1
        for user in self._users:
            self._insert_user_tree(count, post)
            count += 1

    """
    Inserts a single user to the user_tree widget.
    """
    def insert_user(self, post:list):
        self._users.append(post)
        self._insert_user_tree(len(self._users), post)

    """
    Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
    as when a new DSU file is loaded, for example.
    """
    def reset_ui(self):
        self.set_text_entry("")
        self._users = []
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)

    """
    Inserts a post entry into the posts_tree widget.
    """
    def _insert_user_tree(self, id, post:list):
        entry = post.entry
        # Since we don't have a title, we will use the first 24 characters of a
        # post entry as the identifier in the user_tree widget.
        if len(entry) > 25:
            entry = entry[:24] + "..."
        
        self.users_tree.insert('', id, id, text=entry)
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        user_frame = tk.Frame(master=self, width=250, bg="gray")
        user_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.user_tree = ttk.Treeview(user_frame)
        self.user_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.user_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)
        
        view_frame = tk.Frame(master=self, bg="gray")
        view_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        entry_frame = tk.Frame(master=self, bg="gray")
        entry_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)

        self.msg_view = tk.Text(master=view_frame, height=20)
        self.msg_view.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)
        
        self.msg_editor = tk.Text(master=entry_frame, height=0)
        self.msg_editor.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True, padx=5, pady=5)

        #scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        #scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        #msg_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.msg_editor.yview)
        #self.msg_editor['yscrollcommand'] = msg_editor_scrollbar.set
        #msg_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the footer portion of the root frame.
"""
class Footer(tk.Frame):
    def __init__(self, root, send_callback=None, add_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._add_callback = add_callback
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance 
        self._draw()

    """
    Calls the callback function specified in the save_callback class attribute, if
    available, when the save_button has been clicked.
    """
    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def add_click(self):
        if self._add_callback is not None:
            self._add_callback()
     
    def refresh(self):
        pass
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        footer_frame = tk.Frame(master=self, bg="gray")
        footer_frame.pack(fill=tk.BOTH, side=tk.BOTTOM)
        
        send_button = tk.Button(master=footer_frame, text="Send", width=20)
        send_button.configure(command=self.send_click)
        send_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)
        
        refresh_button = tk.Button(master=footer_frame, text="Refresh", width=20)
        refresh_button.configure(command=self.send_click)
        refresh_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        add_button = tk.Button(master=footer_frame, text="Add User")
        add_button.configure(command=self.add_click)
        add_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the main portion of the root frame. Also manages all method calls for
the NaClProfile class.
"""
class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()
    
    """
    Closes the program when the 'Close' menu item is clicked.
    """
    def close(self):
        self.root.destroy()

    def send_message(self):
        pass

    def add_user(self):
        pass
    
    """
    Call only once, upon initialization to add widgets to root frame
    """
    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='Click')
        menu_file.add_command(label='Close', command=self.close)
        # NOTE: Additional menu items can be added by following the conventions here.
        # The only top level menu item is a 'cascading menu', that presents a small menu of
        # command items when clicked. But there are others. A single button or checkbox, for example,
        # could also be added to the menu bar. 

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        # TODO: Add a callback for detecting changes to the online checkbox widget in the Footer class. Follow
        # the conventions established by the existing save_callback parameter.
        # HINT: There may already be a class method that serves as a good callback function!
        self.footer = Footer(self.root, send_callback=self.send_message, add_callback=self.add_user)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

if __name__ == "__main__":
    main = tk.Tk()

    main.title("ICS 32 Mesenger Demo")

    main.geometry("720x480")

    main.option_add('*tearOff', False)

    MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()

