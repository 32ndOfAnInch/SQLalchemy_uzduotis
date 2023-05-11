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

layoutl = [[sg.Button("Atvaizduoti darbuotojus", key="-atvaizduoti-", button_color="#ff11ee", pad=10, size=(25, 1))],
          [sg.Button("Irasyti nauja darbuotoja", key="-irasyti-", button_color="#ff11ee", pad=10, size=(25, 1))],
          [sg.Button("Redaguoti darbuotojo duomenis", key="-redaguoti-", button_color="#ff11ee", pad=10, size=(25, 1))],
          [sg.Button("Atleisti darbuotoja", key="-atleisti-", button_color="red", pad=10, size=(25, 1))],
          [sg.Button("Uzdaryti lentele", key="-close-", button_color="#ff1155", pad=10, size=(25, 1))],
          [sg.Text("", pad=(10, 90))],
          [sg.Text("", pad=(10, 80))],
          [sg.Button("Isvalyti laukus", key="-CLEAR-", button_color="#ff1155", pad=(10, 10), size=(25, 1))],
          [sg.Button("Iseiti is programos", key="-EXIT-", button_color="#ff1155", pad=(10, 10), size=(25, 1))]]


darbuotojai_list = []
headings = ['ID', 'Vardas', 'Pavarde', 'Gimimo data', 'Pareigos', 'Atlyginimas', 'Dirba nuo']

layoutr = [[sg.Table(values=darbuotojai_list, headings=headings,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification='left',
                    num_rows=15,
                    key='-TABLE-',
                    row_height=32,
                    enable_events=True
                    )],
            [sg.Text('ID', size=10), sg.Input(default_text="", enable_events=True, key='-ID-', disabled=True)],
            [sg.Text('Vardas', size=10), sg.Input(default_text="", enable_events=True, key='-VARDAS-')],
            [sg.Text('Pavarde', size=10), sg.Input(default_text="", enable_events=True, key='-PAVARDE-')],
            [sg.Text('Gimimo data', size=10), sg.Input(default_text="", enable_events=True, key='-GIMIMAS-')],
            [sg.Text('Pareigos', size=10), sg.Input(default_text="", enable_events=True, key='-PAREIGOS-')],
            [sg.Text('Atlyginimas', size=10), sg.Input(default_text="", enable_events=True, key='-ATLYGINIMAS-')]
    ]


layout = [[sg.Col(layoutl, p=0), sg.Col(layoutr, p=0, visible=False, key="-COL2-")]]
window = sg.Window("Darboutojai", layout, size=(960, 720))

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
                sg.popup_notify("Darbuotojas sekmingai ismestas is darbo")
                # refreshiti lenta
                darbuotojai_list = bke.spausdinti(session)
                window['-TABLE-'].update(values=darbuotojai_list)
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
                sg.popup_notify("Irasytas naujas darbuotojas")
                # refreshiti lenta
                darbuotojai_list = bke.spausdinti(session)
                window['-TABLE-'].update(values=darbuotojai_list)
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
                sg.popup_notify("Darbuotojo duomenys sekmingai pakeisti")
                # refreshiti lenta
                darbuotojai_list = bke.spausdinti(session)
                window['-TABLE-'].update(values=darbuotojai_list)
            else:
                pass
        except Exception as e:
            print(e)

    if event == "-CLEAR-":
        window['-ID-'].update(value="")
        window['-VARDAS-'].update(value="")
        window['-PAVARDE-'].update(value="")
        window['-GIMIMAS-'].update(value="")
        window['-PAREIGOS-'].update(value="")
        window['-ATLYGINIMAS-'].update(value="")

    if event == sg.WINDOW_CLOSED or event == "-EXIT-":
        break

window.close()