import tkinter as tk
from tkinter import ttk, filedialog
from ds_messenger import DirectMessenger

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the body portion of the root frame.
"""
class Body(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.recipient = None
        self._users = {}
      
        self._draw()
        self.msg_view.config(state='disabled')

    
    """
    Update the msg_editor with the full post entry when the corresponding node in the user_tree
    is selected.
    """
    def node_select(self, event):
        index = int(self.user_tree.selection()[0])-2 #selections are not 0-based, so subtract one.
        l = list(self._users)
        user = l[index]
        entry = ''
        self.recipient = user
        for users in self._users:
            if users == user:
                for i in range(len(self._users[user])):
                    entry = entry + '{} @ {}'.format(self._users[user][i]['message'], self._users[user][i]['timestamp']) + '\n'
        self.msg_view.config(state='normal')
        self.msg_view.delete(0.0, 'end')
        self.msg_view.insert(0.0, entry)
        self.msg_view.config(state='disabled')
    
    """
    Returns the text that is currently displayed in the msg_editor widget.
    """
    def get_text_entry(self) -> str:
        return self.msg_editor.get('1.0', 'end').rstrip()

    """
    Sets the text to be displayed in the msg_editor widget.
    """
    def set_text_entry(self, text:str):
        self.msg_editor.delete(0.0, 'end')
        self.msg_editor.insert(0.0, text)
    

    def set_users(self, dic:dict):
        self._users = dic
        o = 1
        for users in dic:
            o += 1
            entry = ''
            for i in range(len(dic[users])):
                entry = entry + '{} @ {}'.format(dic[users][i]['message'], dic[users][i]['timestamp']) + '\n'
            self._insert_user_tree(o, users)

    """
    Inserts a single user to the user_tree widget.
    """
    def insert_user(self, user):
        self._users[user] = []
        d = self._users.copy()
        self.reset_ui()
        self._users = d
        self.set_users(d)
        self._insert_user_tree(len(self._users)+2, '')

    """
    Resets all UI widgets to their default state.
    """
    def reset_ui(self):
        self.set_text_entry("")
        self._users = {}
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)

    """
    Inserts a user entry into the user_tree widget.
    """
    def _insert_user_tree(self, num, message):
        """entry = post.entry
        # Since we don't have a title, we will use the first 24 characters of a
        # post entry as the identifier in the user_tree widget.
        if len(entry) > 25:
            entry = entry[:24] + "..."""
        self.user_tree.insert('', num, num, text=message)
    
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

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the footer portion of the root frame.
"""
class Footer(tk.Frame):
    def __init__(self, root, send_callback=None, add_callback=None, refresh_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._add_callback = add_callback
        self._refresh_callback = refresh_callback
        
        self._draw()

    """
    Calls the callback function specified in the save_callback class attribute, if
    available, when the save_button has been clicked.
    """
    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    """
    Calls the callback function specified in the add_callback class attribute, if
    available, when the add_button has been clicked.
    """
    def add_click(self):
        if self._add_callback is not None:
            self._add_callback()

    """
    Calls the callback function specified in the refresh_callback class attribute, if
    available, when the refresh_button has been clicked.
    """ 
    def refresh(self):
        if self._refresh_callback is not None:
            self._refresh_callback()
    
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
        refresh_button.configure(command=self.refresh)
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
        self.user = None
        self.dsuserver = '168.235.86.101'
        self.port = 3021
        self.username = "defaultusername"
        self.password = '1223'
        self.token = 'user_token'

        self._draw()


    """
    Closes the program when the 'Close' menu item is clicked.
    """
    def close(self):
        self.root.destroy()

    
    """
    Sends the written message to the server when the 'Send' button is clicked.
    """
    def send_message(self):
        dm = DirectMessenger(self.dsuserver,self.username, self.password)
        resp = dm.send(self.body.get_text_entry(), self.body.recipient)
        if resp == 'ok':
            print('Message Sent Successful')
        else:
            print('Message Unable To Send')

    """
    Creates a new Toplevel window so that a user can add a new user.
    """
    def add_user(self):
        self.user_window = tk.Toplevel()
        self.user_window.geometry("300x100")
        
        title = tk.Label(master=self.user_window, text='LOGIN')
        title.pack(fill='x', padx=5, pady=5)

        self.msg_editor = tk.Text(master=self.user_window, height=0)
        self.msg_editor.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True, padx=5, pady=5)

        save_button = tk.Button(master=self.user_window, text="Add User", width=20)
        save_button.configure(command=self.get_user_info)
        save_button.pack(fill=tk.BOTH, side=tk.TOP, padx=5, pady=5)

    """
    Gets the username inputted from add_user and adds it onto the user_tree.
    """
    def get_user_info(self):
        self.body.insert_user(self.msg_editor.get('1.0', 'end').rstrip())
        self.body.recipient = self.msg_editor.get('1.0', 'end').rstrip()
        self.user_window.destroy()
    
    def refresh_msg(self):
        if self.username != None:
            dm = DirectMessenger(self.dsuserver,self.username,self.password)
            all_messages = dm.retrieve_all()
            before = self.body._users.copy()
            self.body.reset_ui()
            after = {}
            if len(all_messages) != 0:
                for i in range(len(all_messages)):
                    after[all_messages[i]['from']] = []
                for i in range(len(all_messages)):
                    if all_messages[i]['from'] in after:
                        after[all_messages[i]['from']].append({'message':all_messages[i]['message'], 'timestamp':all_messages[i]['timestamp']})
            for keys in after:
                if keys not in before:
                    before[keys] = after[keys]
                elif keys in before:
                    before[keys] = after[keys]
                    
            self._users = before
            self.body.set_users(self._users)
    
    """
    Call only once, upon initialization to add widgets to root frame
    """
    def _draw(self):
        
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        
        menu_bar.add_cascade(menu=menu_file, label='Click')
        

        menu_file.add_command(label='Close', command=self.close)

        self.body = Body(self.root)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        self.footer = Footer(self.root, send_callback=self.send_message, add_callback=self.add_user, refresh_callback=self.refresh_msg)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

if __name__ == "__main__":
    main = tk.Tk()

    main.title("ICS 32 Mesenger Demo")

    main.geometry("720x480")

    main.option_add('*tearOff', False)

    MainApp(main)

    main.update()
    
    main.minsize(main.winfo_width(), main.winfo_height())

    main.mainloop()
