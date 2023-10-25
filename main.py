from sqlite_functions import *
import tkinter as tk
from screeninfo import get_monitors
from gui import login_window

# variable for plantWindow/potWindow change
syncButtonVariable = "pot"
# we need to know monitor size to mak e applicable to all monitors
monitor = get_monitors()[0]
width = monitor.width
height = monitor.width
root = tk.Tk()
root.title("PyPosuda")
root.geometry("%dx%d" % (height, width))


# we need this to set default vaulue of radiobutton
show_password = tk.StringVar()
show_password.set('show')

# Dictionary contatinig userName and password
users = {"ADMIN": ["Antun", "Ivić", 1111]}

# we need to check users in Users Dabase
usersDatabaseConnection = create_connection(r"data/Users Database")
rows = select_all_data(usersDatabaseConnection, "korisnici")
if len(rows) == 0:
    for key, value in users.items():
        user = (key, value[0], value[1], value[2])
        querry = '''INSERT INTO korisnici (korisnicko_ime, 
                                            ime, 
                                            prezime, 
                                            lozinka)
        VALUES (?,?,?,?)'''
        insert_data(usersDatabaseConnection, user, querry)


login_window(root, width, height)
root.mainloop()
