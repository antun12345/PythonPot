import tkinter as tk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sqlite_functions import *

fakeMeteoConnection = create_connection("Data/fakeMeteo.db")
query = "SELECT * FROM Vrijednosti"
fakeMeteoDF = pd.read_sql_query(query, fakeMeteoConnection)
df_sorted = fakeMeteoDF.sort_values(by='datum', ascending=True)

df_sorted['datum'] = pd.to_datetime(df_sorted['datum'], format='%Y-%m-%d')
df_sorted['mjesec'] = df_sorted['datum'].dt.month
df_sorted['temperatura'] = df_sorted['temperatura'].astype(int)
df_sorted['pH'] = df_sorted['pH'].astype(float)
df_sorted['vlažnost'] = df_sorted['vlažnost'].astype(float)
monthly_mean_temp = df_sorted.groupby('mjesec')['temperatura'].mean()
monthly_mean_ph = df_sorted.groupby('mjesec')['pH'].mean()
monthly_humidity = df_sorted.groupby('mjesec')['vlažnost'].mean()


def create_line_chart():

    visualisation = tk.Tk()
    visualisation.title("Prikaz mjerenja")

    # Diagram 1: Monthly Average Temperature
    figure1 = Figure(figsize=(4, 4), dpi=100)
    ax1 = figure1.add_subplot(111)
    ax1.plot(monthly_mean_temp.index, monthly_mean_temp.values,
             "-g", label="Temperatura")
    ax1.set_title("Prosječna mjesečna temperatura")
    ax1.set_xlabel("Mjesec")
    ax1.set_ylabel(" Temperatura")
    ax1.legend()

    canvas1 = FigureCanvasTkAgg(figure1, master=visualisation)
    canvas1.draw()
    canvas1.get_tk_widget().grid(row=0, column=0)

    # Diagram 2: Monthly Average pH
    figure2 = Figure(figsize=(4, 4), dpi=100)
    ax2 = figure2.add_subplot(111)
    ax2.plot(monthly_mean_ph.index, monthly_mean_ph.values, "-b", label="pH")
    ax2.set_title("Prosječna razina pH")
    ax2.set_xlabel("Mjesec")
    ax2.set_ylabel(" pH")
    ax2.legend()

    canvas2 = FigureCanvasTkAgg(figure2, master=visualisation)
    canvas2.draw()
    canvas2.get_tk_widget().grid(row=0, column=1)

    # Diagram 3: Monthly Average Humidity
    figure3 = Figure(figsize=(4, 4), dpi=100)
    ax3 = figure3.add_subplot(111)
    ax3.plot(monthly_humidity.index,
             monthly_humidity.values, "-y", label="Vlažnost")
    ax3.set_title("Prosječna razina vlažnosti")
    ax3.set_xlabel("Mjesec")
    ax3.set_ylabel("Vlažnost")
    ax3.legend()

    canvas3 = FigureCanvasTkAgg(figure3, master=visualisation)
    canvas3.draw()
    canvas3.get_tk_widget().grid(row=0, column=2)
    visualisation.mainloop()


def create_histogram():
    visualisation = tk.Tk()
    visualisation.title("Prikaz mjerenja")

    # Diagram 1: Monthly Average Temperature Histogram
    figure1 = Figure(figsize=(4, 4), dpi=80)
    ax1 = figure1.add_subplot(111)
    ax1.hist(monthly_mean_temp.values, bins=10, color='g', alpha=0.7)
    ax1.set_title("Prosječna mjesečna temperatura")
    ax1.set_xlabel("Temperatura")
    ax1.set_ylabel("Frequency")

    canvas1 = FigureCanvasTkAgg(figure1, master=visualisation)
    canvas1.draw()
    canvas1.get_tk_widget().grid(row=0, column=0)

    # Diagram 2: Monthly Average pH Histogram
    figure2 = Figure(figsize=(4, 4), dpi=80)
    ax2 = figure2.add_subplot(111)
    ax2.hist(monthly_mean_ph.values, bins=10, color='b', alpha=0.7)
    ax2.set_title("Prosječna razina pH")
    ax2.set_xlabel(" pH")
    ax2.set_ylabel("Frequency")

    canvas2 = FigureCanvasTkAgg(figure2, master=visualisation)
    canvas2.draw()
    canvas2.get_tk_widget().grid(row=0, column=1)

    # Diagram 3: Monthly Average Humidity Histogram
    figure3 = Figure(figsize=(4, 4), dpi=80)
    ax3 = figure3.add_subplot(111)
    ax3.hist(monthly_humidity.values, bins=10, color='y', alpha=0.7)
    ax3.set_title("Prosječna vlažnost")
    ax3.set_xlabel("Vlažnost")
    ax3.set_ylabel("Frequency")

    canvas3 = FigureCanvasTkAgg(figure3, master=visualisation)
    canvas3.draw()
    canvas3.get_tk_widget().grid(row=0, column=2)

    visualisation.mainloop()


def create_pie_chart():

    visualisation = tk.Tk()
    visualisation.minsize(800, 400)
    visualisation.title("Prikaz mjerenja")

    # Diagram 1: Monthly Average Temperature Pie Chart
    figure1 = Figure(figsize=(4, 4), dpi=80)
    ax1 = figure1.add_subplot(111)
    ax1.pie(monthly_mean_temp.values,
            labels=monthly_mean_temp.index, autopct='%1.1f%%')
    ax1.set_title("Prosječna mjesečna temperatura")
    canvas1 = FigureCanvasTkAgg(figure1, master=visualisation)
    canvas1.draw()
    canvas1.get_tk_widget().grid(row=0, column=0)

    # Diagram 2: Monthly Average pH Pie Chart
    figure2 = Figure(figsize=(4, 4), dpi=80)
    ax2 = figure2.add_subplot(111)
    ax2.pie(monthly_mean_ph.values,
            labels=monthly_mean_ph.index, autopct='%1.1f%%')
    ax2.set_title("Prosječna pH razina")

    canvas2 = FigureCanvasTkAgg(figure2, master=visualisation)
    canvas2.draw()
    canvas2.get_tk_widget().grid(row=0, column=1)

    # Diagram 3: Monthly Average Humidity Pie Chart
    figure3 = Figure(figsize=(4, 4), dpi=80)
    ax3 = figure3.add_subplot(111)
    ax3.pie(monthly_humidity.values,
            labels=monthly_humidity.index, autopct='%1.1f%%')
    ax3.set_title("Prosječna razina vlažnosti")

    canvas3 = FigureCanvasTkAgg(figure3, master=visualisation)
    canvas3.draw()
    canvas3.get_tk_widget().grid(row=0, column=2)

    visualisation.mainloop()
