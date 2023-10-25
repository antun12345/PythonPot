import tkinter as tk
from PIL import Image, ImageTk
from sqlite_functions import *
from classes import *


opened_profile_windows = 0


def set_password():
    if show_password.get() == "show":
        user_password_entry.config(show="")
    else:
        user_password_entry.config(show="*")


def del_password_1():
    user_password_entry.delete(0, "end")
    user_password_entry.config(fg="black")


def del_user_name(e):
    user_name_entry.delete(0, "end")
    user_name_entry.config(fg="black")


def del_password(e):
    user_password_entry.delete(0, "end")
    user_password_entry.config(fg="black")


def login():
    global users, user_name_entry
    users_database_connection = create_connection(r"Data/Users Database")
    rows = select_all_data(users_database_connection, "korisnici")
    users = {}
    for row in rows:
        users[row[0]] = [row[1], row[2], int(row[3])]

    user_name = user_name_entry.get()
    if user_name not in users:
        user_name = False

    try:
        password = int(user_password_entry.get())

    except:
        password = False

    try:
        if password in users[user_name]:
            password = True
        else:
            password = False
    except:
        password = False

    if user_name == False:
        user_name_entry.delete(0, "end")
        user_name_entry.insert(0, "Pogrešno korisničko ime")
        user_name_entry.config(fg="red")
        del_password_1()
        user_name_entry.bind("<Button-1>",  del_user_name)

    elif password == False:
        user_password_entry.delete(0, "end")
        user_password_entry.insert(0, "Pogrešna lozinka")
        user_password_entry.config(fg="red")
        show_password.set('show')
        user_password_entry.bind("<Button-1>",  del_password)

        set_password()

    else:
        pots_frame()


def login_window(root, width, height):
    global main_frame, user_name_entry, user_password_entry
    global login_label_frame
    global background_picture, binding_id
    global login_root, login_width, login_height, show_password
    # we need this to set default vaulue of radiobutton
    show_password = tk.StringVar()
    show_password.set('show')
    login_root = root
    login_width = width
    login_height = height

    photo_file_name = Image.open(r"Photos\ResizedPhoto.png")
    background_picture = ImageTk.PhotoImage(photo_file_name)

    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.grid(row=0, column=0)
    login_label_frame = tk.LabelFrame(
        main_frame, width=width-30, height=height-30, labelanchor="n")
    login_label_frame.pack()
    photo_label = tk.Label(login_label_frame, image=background_picture)
    photo_label.place(x=0, y=0)
    user_name_label = tk.Label(
        login_label_frame, text="Korisničko ime", font=("Times", 10))
    user_name_label.place(x=width - 450, y=140)
    user_name_entry = tk.Entry(login_label_frame, width=30)
    user_name_entry.place(x=width - 300, y=140)
    user_name_entry.insert(0, "Unesite koriničko ime")
    user_name_entry.bind("<FocusIn>", del_user_name)
    user_password_label = tk.Label(
        login_label_frame, text="Lozinka", font=("Times", 10))
    user_password_label.place(x=width - 450, y=180)
    user_password_entry = tk.Entry(login_label_frame, width=30)
    user_password_entry.place(x=width - 300, y=180)
    user_password_entry.insert(0, "Unesite lozinku")
    user_password_entry.bind("<FocusIn>", del_password)
    binding_id = user_password_entry.bind("<FocusIn>", del_password)
    radiobutton_show_password = tk.Radiobutton(login_label_frame,
                                               text="Prikaži lozinku",
                                               variable=show_password,
                                               value="show",
                                               command=set_password).place(x=width-300, y=220)
    radiobutton_hide_password = tk.Radiobutton(login_label_frame,
                                               text="Sakrij lozinku",
                                               variable=show_password,
                                               value="hide",
                                               command=set_password).place(x=width - 450, y=220)
    login_button = tk.Button(login_label_frame,
                             text="Prijava",
                             font=("Times", 10),
                             state="active",
                             width=43,
                             command=login)
    login_button.place(x=width - 450, y=260)


def log_out():
    for widgets in main_frame.winfo_children():
        widgets.destroy()
    login_window(login_root, login_width, login_height)


def sync():
    if sync_button_variable == "pot":
        pots_frame()
    else:
        plants_frame()


def top_label_frame_pots():
    global main_frame, top_label_frame, title, page_title
    global sync_button, my_profile_button, log_out_button
    top_label_frame = tk.LabelFrame(main_frame, borderwidth=2)
    top_label_frame.grid(column=0, row=0)
    title = tk.Label(top_label_frame, text="PyFlora", font=(
        "Cambria", 14), anchor="w").grid(row=0, column=0, padx=5, pady=10)
    page_title = tk.Label(top_label_frame, text="Posude", font=(
        "Cambria", 14), anchor="center").grid(row=0, column=1, padx=5, pady=10)
    sync_button = tk.Button(top_label_frame, text="SYNC", font=(
        "Cambria", 10), anchor="e", command=sync)
    sync_button.grid(row=0, column=2, padx=5,  pady=10)
    my_profile_button = tk.Button(top_label_frame, text="MOJ PROFIL", font=(
        "Cambria", 10), command=users_account)
    my_profile_button.grid(row=0, column=3, padx=5,  pady=10)
    show_pots_label = tk.Button(top_label_frame, text="PRIKAZ BILJAKA", font=(
        "Cambria", 10), command=plants_frame)
    show_pots_label.grid(row=0, column=4, padx=5,  pady=10)
    log_out_button = tk.Button(top_label_frame, text="ODJAVA",
                               font=("Cambria", 10), command=log_out)
    log_out_button.grid(row=0, column=5, padx=5,  pady=10)


def top_label_frame_plants():
    global main_frame, top_label_frame, title, page_title, sync_button, my_profile_button, log_out_button
    top_label_frame = tk.LabelFrame(main_frame, borderwidth=2)
    top_label_frame.grid(column=0, row=0)
    title = tk.Label(top_label_frame, text="PyFlora",
                     font=("Cambria", 14),
                     anchor="w").grid(row=0, column=0, padx=5, pady=10)
    page_title = tk.Label(top_label_frame,
                          text="Posude",
                          font=("Cambria", 14),
                          anchor="center").grid(row=0, column=1, padx=5, pady=10)
    sync_button = tk.Button(top_label_frame,
                            text="SYNC",
                            font=("Cambria", 10),
                            anchor="e",
                            command=sync)
    sync_button.grid(row=0, column=2, padx=5,  pady=10)
    my_profile_button = tk.Button(top_label_frame,
                                  text="MOJ PROFIL",
                                  font=("Cambria", 10),
                                  command=users_account)
    my_profile_button.grid(row=0, column=3, padx=5,  pady=10)
    show_pots_label = tk.Button(top_label_frame, text="PRIKAZ POSUDA", font=(
        "Cambria", 10), command=pots_frame)
    show_pots_label.grid(row=0, column=4, padx=5,  pady=10)
    log_out_button = tk.Button(top_label_frame, text="ODJAVA",
                               font=("Cambria", 10), command=log_out)
    log_out_button.grid(row=0, column=5, padx=5,  pady=10)


def save_pot():
    '''Functions which add new pot to the base by pressing button "SPREMI"'''

    new_pot_name = pot_name_entry.get()
    pots_database_connection = create_connection(r"Data/Pots Database")
    querry = '''INSERT INTO posude (naziv_posude,
                                    ispravnost_posude, 
                                    biljka)
                    VALUES (?,?,?)'''
    insert_data(pots_database_connection, (new_pot_name, True, ""), querry)
    new_pot_window.destroy()
    for widgets in main_frame.winfo_children():
        widgets.destroy()
    pots_frame()


def add_new_pot():
    '''When "Dodaj biljku button is pressed, newPot window is opened"'''

    global pot_name_entry, new_pot_window
    new_pot_window = tk.Tk()
    new_pot_window.title("Dodavanje posude")
    new_pot_window.geometry("500x300")
    frame = tk.Frame(new_pot_window)
    frame.grid(column=0, row=0,
               ipadx=20, ipady=20)
    new_pot_frame = tk.LabelFrame(frame, padx=10, pady=10)
    new_pot_frame.grid(column=0, row=0)
    pot_name = tk.Label(new_pot_frame, text="Unesite naziv posude",
                        font=("Times", 10), padx=20, pady=20)
    pot_name.grid(column=0, row=1, ipadx=10, ipady=10)
    pot_name_entry = tk.Entry(new_pot_frame, width=30)
    pot_name_entry.grid(column=1, row=1, ipadx=10, ipady=10)
    save_button = tk.Button(new_pot_frame,
                            text="Spremi",
                            font=("Times", 10),
                            state="active",
                            width=43,
                            command=save_pot)
    save_button.grid(column=0, row=2, columnspan=2)


def add_new_plant():
    '''New window for new plant data'''

    global new_plant_window, plant_name_entry, optimal_ph_entry, optimal_salinity_entry, temp_max_entry, temp_min_entry, humidity_entry, lightness_entry
    new_plant_window = tk.Toplevel()
    new_plant_window.title("DOdavanje nove biljke")
    new_plant_window.geometry("800x400")

    # create a label frame to hold the plant information
    plant_window_frame = tk.Frame(new_plant_window)
    plant_window_frame.grid(column=0, row=0, padx=10, pady=10, ipady=5)
    # create left and right label frames
    left_frame = tk.LabelFrame(plant_window_frame, padx=10, pady=2)
    left_frame.grid(column=0, row=0, padx=10, ipady=2)
    button_label_frame = tk.LabelFrame(plant_window_frame)
    button_label_frame.grid(column=0, row=2, pady=2)
    # plant name label and entry
    plant_name_label = tk.Label(
        left_frame, text="Naziv biljke:", font=("Cambria", 10))
    plant_name_label.grid(column=0, row=0, padx=3, pady=2)
    plant_name_entry = tk.Entry(left_frame)
    plant_name_entry.grid(column=1, row=0, padx=3, pady=2)
    # optimal pH label and entry
    optimal_ph_label = tk.Label(
        left_frame, text="Optimalna pH vrijednost:", font=("Cambria", 10))
    optimal_ph_label.grid(column=0, row=1, padx=3, pady=2)
    optimal_ph_entry = tk.Entry(left_frame)
    optimal_ph_entry.grid(column=1, row=1, padx=3, pady=2)
    # optimal salinity label and entry
    optimal_salinity_label = tk.Label(
        left_frame, text="Optimalna slanost tla:", font=("Cambria", 10))
    optimal_salinity_label.grid(column=0, row=2, padx=3, pady=2)
    optimal_salinity_entry = tk.Entry(left_frame)
    optimal_salinity_entry.grid(column=1, row=2, padx=3, pady=2)
    # temperature min and max labels and entries
    temp_min_label = tk.Label(
        left_frame, text="Minimalna temperatura (°C):", font=("Cambria", 10))
    temp_min_label.grid(column=0, row=3, padx=3, pady=2)
    temp_min_entry = tk.Entry(left_frame)
    temp_min_entry.grid(column=1, row=3, padx=3, pady=2)
    temp_max_label = tk.Label(
        left_frame, text="Maksimalna temperatura (°C):", font=("Cambria", 10))
    temp_max_label.grid(column=0, row=4, padx=3, pady=2)
    temp_max_entry = tk.Entry(left_frame)
    temp_max_entry.grid(column=1, row=4, padx=3, pady=2)
    # humidity label and entry
    humidity_label = tk.Label(
        left_frame, text="Potrebna vlažnost zraka (%):", font=("Cambria", 10))
    humidity_label.grid(column=0, row=5, padx=3, pady=2)
    humidity_entry = tk.Entry(left_frame)
    humidity_entry.grid(column=1, row=5, padx=3, pady=2)
    # lightness label and entry
    lightness_label = tk.Label(
        left_frame, text="Potrebna količina svjetla (lx):", font=("Cambria", 10))
    lightness_label.grid(column=0, row=6, padx=3, pady=2)
    lightness_entry = tk.Entry(left_frame)
    lightness_entry.grid(column=1, row=6, padx=3, pady=2)

    save_button = tk.Button(button_label_frame,
                            text="Spremi",
                            font=("Times", 10),
                            state="active",
                            width=43,
                            command=save_plant)
    save_button.grid(column=0, row=0)
    cancel_button = tk.Button(button_label_frame,
                              text="Odustani",
                              font=("Times", 10),
                              state="active",
                              width=43,
                              command=lambda: new_plant_window.destroy())
    cancel_button.grid(column=1, row=0)


def save_plant():
    '''Function for adding new plant to  database'''

    plant_database_connection = create_connection(r"Data/Plants Database")
    querry = '''INSERT INTO biljke (ime, 
                                    optimalni_ph, 
                                    optimalna_slanost, 
                                    temp_min, 
                                    temp_max, 
                                    zalijevanje, 
                                    zahtjev_za_svjetlom)
                VALUES (?,?,?,?,?,?,?)'''

    plant_info = (plant_name_entry.get(), optimal_ph_entry.get(), optimal_salinity_entry.get(
    ), temp_min_entry.get(), temp_max_entry.get(), humidity_entry.get(), lightness_entry.get())
    insert_data(plant_database_connection, plant_info, querry)
    new_plant_window.destroy()
    plants_frame()


def pots_frame():
    '''PotsLabelFrame is created when button PRIJAVA is pressed  '''

    global login_label_frame, plant_photo, plant_photo_list, empty_pot, sync_button_variable
    sync_button_variable = "pot"
    for widgets in main_frame.winfo_children():
        widgets.destroy()
    plant_photo_list = []
    top_label_frame_pots()
    fire_icon = ImageTk.PhotoImage(Image.open(r"Photos\fire.jpeg"))
    empty_pot = ImageTk.PhotoImage(Image.open(r"Photos\posuda.png"))
    checked_icon = ImageTk.PhotoImage(Image.open(r"Photos\check.png"))
    question_mark_icon = ImageTk.PhotoImage(
        Image.open(r"Photos\questionMark.png"))

    pots_database_connection = create_connection(r"Data/Pots Database")
    rows = select_all_data(pots_database_connection, "posude")
    row_grid = 1
    column_grid = 0

    for row in rows:
        try:
            if (row[3]) != "":
                plant_photo = ImageTk.PhotoImage(
                    Image.open(f"Photos/{str(row[3])}.png"))
                id = int(row[0])
            elif (row[3]) == "":
                plant_photo = empty_pot
                id = int(row[0])
        except Exception as e:
            print(e)
            plant_photo = ImageTk.PhotoImage(Image.open(R"Photos\noImage.png"))

            id = int(row[0])
        try:
            plant_name = row[3]
        except:
            plant_name = ""

        Pot(main_frame, plant_photo, row[1], "Status", plant_name, id, fire_icon, checked_icon, question_mark_icon).grid(
            row=row_grid, column=column_grid, ipadx=20, padx=40, pady=50)
        plant_photo_list.append(plant_photo)

        # Row/Grid adjustment
        column_grid += 1
        if column_grid % 3 == 0:
            row_grid += 1
            column_grid = 0
    add_pot_button = tk.Button(main_frame, text="+\nDodaj novu posudu", font=("Cambria", 20),
                               command=add_new_pot, width=25, height=6, relief="raised").grid(column=column_grid, row=row_grid)


def plants_frame():
    '''Functionn which present plantslabelFrames based on data in Plants Database '''
    for widgets in main_frame.winfo_children():
        widgets.destroy()
    global login_label_frame, plant_photo,  plant_photo_list, empty_pot, sync_button_variable
    sync_button_variable = "plant"
    top_label_frame_plants()
    plants = []
    plant_photo_list = []

    plants_database = r"Data/Plants Database"
    plants_database_connection = create_connection(plants_database)

    rows = select_all_data(plants_database_connection, "biljke")
    row_grid = 1
    column_grid = 0
    for row in rows:
        try:
            plant_photo = ImageTk.PhotoImage(
                Image.open(f"Photos/{str(row[1])}.png"))
        except Exception as e:
            print(e)
            plant_photo = ImageTk.PhotoImage(Image.open(R"Photos\noImage.png"))

        plant_name = row[1]
        optimal_ph = row[2]
        optimal_salinity = row[3]
        temp_min = row[4]
        temp_max = row[5]
        humidity = row[6]
        lightness = row[7]

        if len(plant_name) < 12:
            counter = 0
            for simbol in plant_name:
                counter += 1
            counter = 12 - counter
            string = ""
            while counter != 0:
                string = string + " "
                counter -= 1

            Plant(main_frame, plant_photo, (f"{plant_name}{string}"), optimal_ph, optimal_salinity, temp_min, temp_max, humidity, lightness).grid(
                row=row_grid, column=column_grid, ipadx=5, padx=5, pady=10, sticky="we")
            plant_photo_list.append(plant_photo)
        else:
            Plant(main_frame, plant_photo, plant_name, optimal_ph, optimal_salinity, temp_min, temp_max, humidity,
                  lightness).grid(row=row_grid, column=column_grid, ipadx=5, padx=5, pady=10, sticky="we")
            plant_photo_list.append(plant_photo)

        # Row/Grid adjustment
        column_grid += 1
        if column_grid % 3 == 0:
            row_grid += 1
            column_grid = 0
    add_plant_button = tk.Button(main_frame, text="+\nDodaj novu biljku", font=("Cambria", 20),
                                 command=add_new_plant, width=25, height=6, relief="raised").grid(column=column_grid, row=row_grid)


def users_account():
    '''Function for user account manager'''
    global user_name_entry, name_entry, surname_entry, password_entry, profil_window, opened_profile_windows

    if opened_profile_windows == 0:
        opened_profile_windows = 1
        profil_window = tk.Tk()
        profil_window.title("Postavke profila")
        profil_window.geometry("400x250")
        profil_window.resizable(height=False, width=False)
        profil_window_frame = tk.Frame(profil_window)
        profil_window_frame.grid(column=0, row=0, padx=10, pady=10, ipady=5)
        window_label_frame = tk.LabelFrame(
            profil_window_frame, text="Korisnički podaci", padx=10, pady=2)
        window_label_frame.grid(column=0, row=0, padx=10, ipady=2)

        for key, value in users.items():
            user_name_label = tk.Label(
                window_label_frame, text="Korisničko ime:", font=("Cambria", 10))
            user_name_label.grid(column=0, row=0, padx=3, pady=2)
            user_name_entry = tk.Entry(window_label_frame)
            user_name_entry.insert(0, key)
            user_name_entry.grid(column=1, row=0, padx=3, pady=2)

            name_label = tk.Label(window_label_frame, text="Ime:",
                                  font=("Cambria", 10))
            name_label.grid(column=0, row=1, padx=3, pady=2)
            name_entry = tk.Entry(window_label_frame)
            name_entry.insert(0, value[0])
            name_entry.grid(column=1, row=1, padx=3, pady=2)

            surname_label = tk.Label(
                window_label_frame, text="Prezime:", font=("Cambria", 10))
            surname_label.grid(column=0, row=2, padx=3, pady=2)
            surname_entry = tk.Entry(window_label_frame)
            surname_entry.insert(0, value[1])
            surname_entry.grid(column=1, row=2, padx=3, pady=2)

            password_label = tk.Label(
                window_label_frame, text="Lozinka:", font=("Cambria", 10))
            password_label.grid(column=0, row=3, padx=3, pady=2)
            password_entry = tk.Entry(window_label_frame)
            password_entry.insert(0, value[2])
            password_entry.grid(column=1, row=3, padx=3, pady=2)

            update_button = tk.Button(profil_window_frame, text="Ažuriraj", font=(
                "Cambria", 11), command=update_users_data, width=30)
            update_button.grid(column=0, row=1, columnspan=2,
                               sticky="e", padx=25, pady=10)

            def on_closing():
                global opened_profile_windows
                opened_profile_windows = 0
                profil_window.destroy()
            profil_window.protocol("WM_DELETE_WINDOW", on_closing)
            profil_window.mainloop()

    else:
        pass


def update_users_data():
    global users, opened_profile_windows
    opened_profile_windows = 0
    user_name = (user_name_entry.get())
    name = name_entry.get()
    surname = (surname_entry.get())
    password = int(password_entry.get())
    user = (user_name, name, surname, password)

    querry = ''' UPDATE korisnici
                SET korisnicko_ime = ?, 
                ime = ?, 
                prezime = ?, 
                lozinka = ?'''
    users_database_connection = create_connection(r"Data/Users Database")
    update_plant_base(users_database_connection,  user, querry)

    profil_window.destroy()
