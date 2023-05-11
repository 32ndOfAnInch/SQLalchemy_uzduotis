import PySimpleGUI as sg
import backend as bke
from typing import Any
from sqlalchemy import create_engine, Integer, String, Float, DateTime, Date
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column
from datetime import datetime

engine = create_engine('sqlite:///darbuotojai.db')
Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    pass

layoutl = [[sg.Button("Atvaizduoti darbuotojus", key="-atvaizduoti-", button_color="#23277b", pad=10, size=(25, 1), font=20)],
          [sg.Button("Atleisti darbuotoja", key="-atleisti-", button_color="#7a223f", pad=10, size=(25, 1), font=20)],
          [sg.Button("Uzdaryti lentele", key="-close-", button_color="#23277b", pad=10, size=(25, 1), font=20)],
          [sg.Text("", pad=(10, 130))],
          [sg.Text("", pad=(10, 130))],
          [sg.Button("Iseiti is programos", key="-EXIT-", button_color="#23277b", pad=(10, 10), size=(25, 1), font=20)]]


darbuotojai_list = []
headings = ['ID', 'Vardas', 'Pavarde', 'Gimimo data', 'Pareigos', 'Atlyginimas', 'Dirba nuo']

layoutr = [[sg.Table(values=darbuotojai_list, headings=headings,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification='left',
                    num_rows=11,
                    key='-TABLE-',
                    row_height=40,
                    enable_events=True,
                    alternating_row_color="#460c1f",
                    background_color="#271d20",
                    font=20,
                    selected_row_colors="white on black"
                    )],
            [sg.Text('ID', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-ID-', pad=(0, 10), font=20, disabled=True),
             sg.Button("Irasyti nauja darbuotoja", key="-irasyti-", button_color="#23277b", pad=10, size=(25, 1), font=20)],
            [sg.Text('Vardas', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-VARDAS-', pad=(0, 10), font=20), 
             sg.Button("Redaguoti duomenis", key="-redaguoti-", button_color="#23277b", pad=10, size=(25, 1), font=20)],
            [sg.Text('Pavarde', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-PAVARDE-', pad=(0, 10), font=20)],
            [sg.Text('Gimimo data', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-GIMIMAS-', pad=(0, 10), font=20)],
            [sg.Text('Pareigos', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-PAREIGOS-', pad=(0, 10), font=20)],
            [sg.Text('Atlyginimas', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-ATLYGINIMAS-', pad=(0, 10), font=20),
             sg.Button("Isvalyti laukus", key="-CLEAR-", button_color="#23277b", pad=(10, 10), size=(25, 1), font=20)]
    ]

# atnaujinti lentele
def refresh_table():
    darbuotojai_list = bke.spausdinti(session)
    window['-TABLE-'].update(values=darbuotojai_list)

# isvalyti laukelius
def clear_inputs():
    window['-ID-'].update(value="")
    window['-VARDAS-'].update(value="")
    window['-PAVARDE-'].update(value="")
    window['-GIMIMAS-'].update(value="")
    window['-PAREIGOS-'].update(value="")
    window['-ATLYGINIMAS-'].update(value="")

layout = [[sg.Col(layoutl, p=0), sg.Col(layoutr, p=0, visible=False, key="-COL2-")]]
window = sg.Window("Darboutojai", layout, size=(1000, 780))

while True:
    event, values = window.read()
    if event == "-atvaizduoti-":
        window["-COL2-"].update(visible=True)
        darbuotojai_list = bke.spausdinti(session)
        #new_list = [string.replace(",", "") for string in darbuotojai_list]
        window['-TABLE-'].update(values=darbuotojai_list)
 
    if event == "-close-":
        window["-COL2-"].update(visible=False)

    if event == "-TABLE-":
        try:
            row_value = values['-TABLE-'][0]
            reiksmes = bke.pasirinkti(session, row_value)
            #print(reiksmes)
            window['-ID-'].update(value=reiksmes[0])
            window['-VARDAS-'].update(value=reiksmes[1])
            window['-PAVARDE-'].update(value=reiksmes[2])
            window['-GIMIMAS-'].update(value=reiksmes[3])
            window['-PAREIGOS-'].update(value=reiksmes[4])
            window['-ATLYGINIMAS-'].update(value=reiksmes[5])
            #print(row_value)
        except:
            pass
    if event == "-atleisti-":
        #print("kazkas turi vykti")
        # dialogas atleidimui
        atleisti_ask_id = window['-ID-'].get()
        if atleisti_ask_id:
            ask_delete = sg.popup_yes_no(f"Ar tikrai norite atleisti darbuotoja ID: {atleisti_ask_id}? ")
            if ask_delete == "Yes":
                bke.istrinti(session, atleisti_ask_id)
                # refreshiti lenta
                refresh_table()
                # isvalyti laukelius
                clear_inputs()
                # parodyti pranesima
                sg.popup_notify("Darbuotojas sekmingai ismestas is darbo")
        else:
            pass

    if event == "-irasyti-":
        try:
            ask_write = sg.popup_yes_no("Ar tikrai norite irasyti nauja darbuotoja? ")
            if ask_write == "Yes":
                vardas = window['-VARDAS-'].get()
                pavarde = window['-PAVARDE-'].get()
                gim_data = window['-GIMIMAS-'].get()
                pareigos = window['-PAREIGOS-'].get()
                atlyginimas = window['-ATLYGINIMAS-'].get()
                bke.irasymas(vardas, pavarde, gim_data, pareigos, atlyginimas)
                # refreshiti lenta
                refresh_table()
                # isvalyti laukelius
                clear_inputs()
                # parodyti pranesima
                sg.popup_notify("Irasytas naujas darbuotojas")
            else:
                pass      
        except Exception as e:
            print(e)

    if event == "-redaguoti-":
        try:
            ask_edit = sg.popup_yes_no(f"Ar tikrai norite redaguoti darbuotojo duomenis? ID = {window['-ID-'].get()}")
            if ask_edit == "Yes":
                # input reiksmiu paemimas
                id = window['-ID-'].get()
                vardas = window['-VARDAS-'].get()
                pavarde = window['-PAVARDE-'].get()
                gim_data = window['-GIMIMAS-'].get()
                pareigos = window['-PAREIGOS-'].get()
                atlyginimas = window['-ATLYGINIMAS-'].get()
                bke.keitimas(id, vardas, pavarde, gim_data, pareigos, atlyginimas)
                # refreshiti lenta
                refresh_table()
                # parodyti pranesima
                sg.popup_notify("Darbuotojo duomenys sekmingai pakeisti")
            else:
                pass
        except Exception as e:
            print(e)

    if event == "-CLEAR-":
        # isvalyti laukelius
        clear_inputs()

    if event == sg.WINDOW_CLOSED or event == "-EXIT-":
        break

window.close()