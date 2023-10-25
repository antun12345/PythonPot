# We will create CLASS Pot as a template for PotLabelFrame
import tkinter as tk
from sqlite_functions import *
from diagrams import *
from gui import *
from sensors import *


class Pot(tk.LabelFrame):
    def __init__(self, parent, pot_photo, pot_name, pot_status, plant_name, pot_id, fire_icon, checked_icon, question_mark_icon):
        super().__init__(master=parent)
        self.potPhoto = pot_photo
        self.potName = pot_name
        self.potStatus = pot_status
        self.plantName = plant_name
        self.id = pot_id
        plants_database_connection = create_connection("Data/Plants Database")
        rows = select_all_data(plants_database_connection, "biljke")

        plant_data = False
        for row in rows:
            if row[1] == self.plantName:
                try:
                    self.optimalPH = float(row[2])
                    self.optimalSalinity = float(row[3])
                    self.tempMin = float(row[4])
                    self.tempMax = float(row[5])
                    self.optimalLightness = int(row[7])
                    plant_data = True
                except ValueError:
                    plant_data = False

        if plant_name == "":
            self.humidity = ""
            self.pH = ""
            self.salinity = ""
            self.lightness = ""
            self.temperature = ""
            self.potStatus = "Prazna posuda"
            self.statusIcon = question_mark_icon
        else:
            self.pH = ph_sensor()
            self.salinity = salinity_sensor()
            self.temperature = temperature()
            self.humidity = humidity_sensor()
            self.lightness = lightness_sensor()

            if self.humidity == 0:
                self.humidity = "Potrebno zalijevanje"
                self.potStatus = "Potrebno zalijevanje"
                self.statusIcon = fire_icon
            else:
                self.humidity = "Optimalna"
                self.potStatus = "Optimalna vlaga"
                self.statusIcon = checked_icon

        try:
            if not plant_data:
                self.statusIcon = question_mark_icon
                self.potStatus = "Nisu dostupni svi podaci"
                self.humidity = "Nema podataka"
        except NameError:
            pass

        # Main data in each Pot labelFrame
        tk.Button(self, image=self.potPhoto, command=self.pot_info_window).grid(
            column=0, row=0, rowspan=3)
        tk.Label(self, text=self.potName, font=(
            "Cambria", 15)).grid(column=2, row=0)
        tk.Label(self, text=self.plantName, font=(
            "Cambria", 12)).grid(column=2, row=1, sticky="n")
        tk.Label(self, text=self.potStatus, font=(
            "Cambria", 10)).grid(column=1, row=2, padx=3)
        tk.Label(self, image=self.statusIcon).grid(column=3, row=2)

    def color_change(self, sensor, optimal_value):
        try:
            if sensor < optimal_value - (optimal_value * 0.2):
                return "blue"
            elif sensor > optimal_value + (optimal_value * 0.2):
                return "red"
            else:
                return "green"
        except TypeError as err:
            print(f"TypeError: {err}")
        except:
            pass

    def pot_info_window(self):
        global pot_window
        pot_window = tk.Toplevel(self)
        pot_window.title("Prikaz biljke")
        pot_window.geometry("700x550")
        pot_window.resizable(width=False, height=False)

        pot_window_frame = tk.Frame(pot_window)
        pot_window_frame.grid(column=0, row=0, padx=10, pady=10, ipady=5)

        # create Labelframes
        left_frame = tk.LabelFrame(
            pot_window_frame, text="Podaci sa senzora", padx=10, pady=2)
        left_frame.grid(column=0, row=0, padx=10, ipady=2)
        middle_frame = tk.LabelFrame(pot_window_frame, padx=10, pady=2)
        middle_frame.grid(column=1, row=0, padx=10, ipady=2)
        right_frame = tk.LabelFrame(pot_window_frame, padx=10, pady=2)
        right_frame.grid(column=2, row=0, padx=10, pady=3)
        bottom_frame = tk.LabelFrame(pot_window_frame, padx=10, pady=2)
        bottom_frame.grid(column=0, row=1, padx=10, ipady=2)
        data_frame = tk.LabelFrame(pot_window_frame, padx=10, pady=2)
        data_frame.grid(column=1, row=1, padx=10, ipady=2, columnspan=2)

        # Data inside labelFrame
        tk.Label(right_frame, image=self.potPhoto).grid(column=0, row=0)

        tk.Label(left_frame, text="pH senzor: ", font=(
            "Cambria", 11)).grid(column=0, row=1, padx=3, pady=2)
        tk.Label(left_frame, text=self.pH, font=("Cambria", 9)).grid(
            column=0, row=2, padx=3, pady=2)

        tk.Label(left_frame, text="Slanost:", font=("Cambria", 11)).grid(
            column=0, row=3, padx=3, pady=2)
        tk.Label(left_frame, text=self.salinity, font=(
            "Cambria", 9)).grid(column=0, row=4, padx=3, pady=2)

        tk.Label(left_frame, text="Temperatura", font=(
            "Cambria", 11)).grid(column=0, row=5, padx=3, pady=2)
        tk.Label(left_frame, text=self.temperature, font=(
            "Cambria", 9)).grid(column=0, row=6, padx=3, pady=2)

        tk.Label(left_frame, text="Vlaga:", font=("Cambria", 11)).grid(
            column=0, row=7, padx=3, pady=2)
        tk.Label(left_frame, text=self.humidity, font=(
            "Cambria", 9)).grid(column=0, row=8, padx=3, pady=2)

        tk.Label(left_frame, text="Količina svjetla:", font=(
            "Cambria", 11)).grid(column=0, row=9, padx=3, pady=2)
        tk.Label(left_frame, text=self.lightness, font=(
            "Cambria", 9)).grid(column=0, row=10, padx=3, pady=2)

        tk.Button(data_frame, text="Line", font=("Cambria", 11),
                  command=create_line_chart, width=10).grid(column=0, row=0, pady=25, padx=5)
        tk.Button(data_frame, text="Pie", font=("Cambria", 11),
                  command=create_pie_chart, width=10).grid(column=1, row=0, pady=25, padx=5)
        tk.Button(data_frame, text="Hist", font=("Cambria", 11),
                  command=create_histogram, width=10).grid(column=2, row=0, pady=25, padx=5)

        if self.plantName != "":
            try:
                tk.Label(left_frame, fg=(self.color_change(self.pH, self.optimalPH)), text="pH senzor: ", font=(
                    "Cambria", 11)).grid(column=0, row=1, padx=3, pady=2)
                tk.Label(left_frame, fg=(self.color_change(self.salinity, self.optimalSalinity)),
                         text="Slanost:", font=("Cambria", 11)).grid(column=0, row=3, padx=3, pady=2)
                tk.Label(left_frame, fg=(self.color_change(self.lightness, self.optimalLightness)),
                         text="Količina svjetla:", font=("Cambria", 11)).grid(column=0, row=9, padx=3, pady=2)
                tk.Label(left_frame, fg=(self.color_change(self.temperature, ((self.tempMin + self.tempMax)/2))),
                         text="Temperatura", font=("Cambria", 11)).grid(column=0, row=5, padx=3, pady=2)
            except AttributeError:
                pass
        updateButton = tk.Button(middle_frame, text="Ažuriraj", font=(
            "Cambria", 11), command=lambda: update(self.id))
        updateButton.grid(column=0, row=0, pady=25, padx=5)
        deleteButton = tk.Button(middle_frame, text="Izbriši posude", font=(
            "Cambria", 11), command=lambda: delete_pot(self.id))
        deleteButton.grid(column=0, row=1, pady=25, padx=5)
        cancelButton = tk.Button(middle_frame, text="Odustani", font=(
            "Cambria", 11), command=self.cancel)
        cancelButton.grid(column=0, row=2, pady=25, padx=5)

        def update(id):
            id = id
            pot_id = id
            plants_database_connection = create_connection(
                r"Data/Plants Database")
            rows = select_all_data(plants_database_connection, "biljke")
            list_button = tk.Listbox(bottom_frame)
            i = 1
            for row in rows:
                list_button.insert(i, row[1])
                i += 1
            list_button.config(height=list_button.size(),
                               font=("sans 10 bold", 10))
            list_button.grid(column=0, row=0, rowspan=list_button.size(
            ), columnspan=2, ipadx=10, ipady=10, pady=10, padx=10)

            def change_plant(event):
                selection = list_button.curselection()
                new_plant_id = int(selection[0]) + 1
                for row in rows:
                    if row[0] == new_plant_id:
                        new_plant = row[1]
                pots_database_connection = create_connection(
                    r"Data/Pots Database")
                update_base(pots_database_connection, "posude",
                            "biljka", pot_id, new_plant)
                pot_window.destroy()

            list_button.bind('<Double-Button-1>', change_plant)

        def delete_pot(id):
            id = id
            row = id
            pots_database_connection = create_connection(r"Data/Pots Database")
            delete_data(pots_database_connection, "posude", "id", row)
            self.cancel()
            pot_window.destroy()

    def cancel(self):
        global pot_window
        pot_window.destroy()


class Plant(tk.LabelFrame):
    def __init__(self, parent, plant_photo, plant_name, optimal_ph, optimal_salinity, temp_min, temp_max, humidity, lightness):
        super().__init__(master=parent)
        self.plantPhoto = plant_photo
        self.plantName = plant_name
        self.optimalPH = optimal_ph
        self.optimalSalinity = optimal_salinity
        self.tempMin = temp_min
        self.tempMax = temp_max
        self.humidity = humidity
        self.lightness = lightness

        tk.Button(self, image=self.plantPhoto, command=self.plant_info_window).grid(
            column=0, row=0, rowspan=3)
        tk.Label(self, text=self.plantName, font=("Cambria", 15),
                 anchor="center").grid(column=2, row=0)
        tk.Label(self, text=f"Optimalni pH:\n{optimal_ph}\nSlanost:\n{optimal_salinity}\nTemperatura:\n{temp_min}-{temp_max}℃\nZalijevanje:\n{humidity}\nOsvjetljenje:\n{lightness}lx", font=(
            "Cambria", 10)).grid(column=3, row=1)

    def plant_info_window(self):
        global plant_window

        plant_window = tk.Toplevel(self)
        plant_window.title("Prikaz biljke")
        plant_window.geometry("670x500")

        plant_window_frame = tk.Frame(plant_window)
        plant_window_frame.grid(column=0, row=0, padx=10, pady=10, ipady=5)

        left_frame = tk.LabelFrame(
            plant_window_frame, text="Plant Info", padx=10, pady=2)
        left_frame.grid(column=0, row=0, padx=10, ipady=2)
        right_frame = tk.LabelFrame(plant_window_frame, padx=10, pady=2)
        right_frame.grid(column=1, row=0, padx=10, pady=3)
        middleFrame = tk.LabelFrame(
            plant_window_frame, padx=10, pady=2)
        middleFrame.grid(column=1, row=0, padx=10, ipady=2)

        button_label_frame = tk.LabelFrame(plant_window_frame)
        button_label_frame.grid(column=0, row=2, pady=2)

        tk.Label(left_frame, text="Naziv biljke:", font=(
            "Cambria", 10)).grid(column=0, row=0, padx=3, pady=2)
        plant_name_entry = tk.Entry(left_frame)
        plant_name_entry.insert(0, self.plantName)
        plant_name_entry.config(state="readonly")
        plant_name_entry.grid(column=1, row=0, padx=3, pady=2)

        tk.Label(left_frame, text="Optimalna pH vrijednost:", font=(
            "Cambria", 10)).grid(column=0, row=1, padx=3, pady=2)
        optimal_ph_entry = tk.Entry(left_frame)
        optimal_ph_entry.insert(0, self.optimalPH)
        optimal_ph_entry.grid(column=1, row=1, padx=3, pady=2)

        tk.Label(left_frame, text="Optimalna slanost tla:", font=(
            "Cambria", 10)).grid(column=0, row=2, padx=3, pady=2)
        optimal_salinity_entry = tk.Entry(left_frame)
        optimal_salinity_entry.insert(0, self.optimalSalinity)
        optimal_salinity_entry.grid(column=1, row=2, padx=3, pady=2)

        tk.Label(left_frame, text="Minimalna temperatura (°C):", font=(
            "Cambria", 10)).grid(column=0, row=3, padx=3, pady=2)
        temp_min_entry = tk.Entry(left_frame)
        temp_min_entry.insert(0, self.tempMin)
        temp_min_entry.grid(column=1, row=3, padx=3, pady=2)

        tk.Label(left_frame, text="Maksimalna temperatura (°C):", font=(
            "Cambria", 10)).grid(column=0, row=4, padx=3, pady=2)
        temp_max_entry = tk.Entry(left_frame)
        temp_max_entry.insert(0, self.tempMax)
        temp_max_entry.grid(column=1, row=4, padx=3, pady=2)

        tk.Label(left_frame, text="Potrebna vlažnost zraka (%):", font=(
            "Cambria", 10)).grid(column=0, row=5, padx=3, pady=2)
        humidity_entry = tk.Entry(left_frame)
        humidity_entry.insert(0, self.humidity)
        humidity_entry.grid(column=1, row=5, padx=3, pady=2)

        tk.Label(left_frame, text="Potrebna količina svjetla (lx):",
                 font=("Cambria", 10)).grid(column=0, row=6, padx=3, pady=2)
        lightness_entry = tk.Entry(left_frame)
        lightness_entry.insert(0, self.lightness)
        lightness_entry.grid(column=1, row=6, padx=3, pady=2)

        tk.Label(right_frame, image=self.plantPhoto).grid(column=0, row=0)

        tk.Button(button_label_frame, text="Ažuriraj", font=("Cambria", 11), command=lambda: update_plant_info(
            self.plantName)).grid(column=0, row=0, sticky="e", padx=25)
        tk.Button(button_label_frame, text="Odustani", font=("Cambria", 11),
                  command=self.cancel).grid(column=1, row=0, sticky="we", padx=25)
        tk.Button(button_label_frame, text="Obriši biljku", font=("Cambria", 11),
                  command=lambda: delete_plant(self.plantName)).grid(column=2, row=0, sticky="e", padx=25)

        def update_plant_info(name):
            name = str(name).strip()
            plants_database_connection = create_connection(
                r"Data/Plants Database")
            rows = select_all_data(plants_database_connection, "biljke")
            optimal_ph = float(optimal_ph_entry.get())
            optimal_salinity = float(optimal_salinity_entry.get())
            temp_min = float(temp_min_entry.get())
            temp_max = float(temp_max_entry.get())
            humidity = humidity_entry.get()
            lightness = int(lightness_entry.get())
            plant_info = (optimal_ph, optimal_salinity, temp_min,
                          temp_max, humidity, lightness, name)

            query = ''' UPDATE biljke 
                SET  optimalni_ph = ?, optimalna_slanost = ?, temp_min = ?, temp_max = ?, zalijevanje = ?, zahtjev_za_svjetlom = ?
                WHERE ime = ?'''
            update_plant_base(plants_database_connection, plant_info, query)
            plant_window.destroy()

        def delete_plant(name):
            name = str(name).strip()
            ime = name
            plant_database_connection = create_connection(
                r"Data/Plants Database")
            delete_data(plant_database_connection, "biljke", "ime", ime)
            plant_window.destroy()

    def cancel(self):
        global plant_window
        plant_window.destroy()
