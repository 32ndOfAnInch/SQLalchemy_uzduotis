from typing import Any
from sqlalchemy import create_engine, Integer, String, Float, DateTime, Date
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column
from datetime import datetime

engine = create_engine('sqlite:///darbuotojai.db')
Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    pass


class Darbuotojas(Base):
    __tablename__ = "darbuotojai"
    id = mapped_column(Integer, primary_key=True)
    vardas = mapped_column(String(50), nullable=False)
    pavarde = mapped_column(String(50), nullable=False)
    gimimo_data = mapped_column(String(50), nullable=False)
    pareigos = mapped_column(String(50), nullable=False)
    atlyginimas = mapped_column(Float(2), nullable=False)
    nuo_kada_dirba = mapped_column(DateTime, default=datetime.today)

    def __init__(self, **kw: Any):
        # super().__init__(**kw)
        for key, value in kw.items():
            setattr(self, key, value)
    
    def __repr__(self) -> str:
        return f"({self.id}, {self.vardas}, {self.pavarde}, {self.gimimo_data}, {self.pareigos}, {self.atlyginimas}, {self.nuo_kada_dirba})"

Base.metadata.create_all(engine)

def spausdinti(session):
    darbuotojai = session.query(Darbuotojas).all()
    print("-------------------")
    for darbuotojas in darbuotojai:
        print(darbuotojas)
    print("-------------------")
    return darbuotojai


while True:
    pasirinkimas = input("""Pasirinkite veiksmą: 
1 - atvaizduoti darbuotojus
2 - irasyti nauja darbuotoja
3 - redaguoti darbuotojo duomenis
4 - atleisti darbuotoja
0 - išeiti
>:""")

    try:
        pasirinkimas = int(pasirinkimas)
    except:
        pass

    if pasirinkimas == 1:
        spausdinti(session)

    elif pasirinkimas == 2:
        vardas = input("Įveskite darbuotojo varda: ")
        pavarde = input("Įveskite darbuotojo pavarde: ")
        gimimo_data = input("Įveskite darbuotojo gimimo data YYYY-MM-DD: ")
        pareigos = input("Įveskite darbuotojo pareigas: ")
        atlyginimas = float(input("Įveskite darbuotojo atlyginima: "))
        projektas = Darbuotojas(vardas=vardas, pavarde=pavarde, gimimo_data=gimimo_data, pareigos=pareigos, atlyginimas=atlyginimas)
        session.add(projektas)
        session.commit()

    elif pasirinkimas == 3:
        projektai = spausdinti(session)
        try:
            keiciamas_id = int(input("Pasirinkite norimo pakeisti darbuotojo ID: "))
            keiciamas_projektas = session.get(Darbuotojas, keiciamas_id)
        except Exception as e:
            print(f"Klaida: {e}")
        else:
            pakeitimas = int(input("Ką norite pakeisti: 1 - varda, 2 - pavarde, 3 - gimimo data, 4 - pareigas, 5 - atlyginima: "))
            if pakeitimas == 1:
                keiciamas_projektas.vardas = input("Įveskite darbuotojo varda: ")
            if pakeitimas == 2:
                keiciamas_projektas.pavarde = input("Įveskite darbuotojo pavarde: ")
            if pakeitimas == 3:
                keiciamas_projektas.gimimo_data = input("Įveskite gimimo data: ")
            if pakeitimas == 4:
                keiciamas_projektas.pareigos = input("Įveskite darbuotojo pareigas: ")
            if pakeitimas == 5:
                keiciamas_projektas.atlyginimas = float(input("Įveskite darbuotojo atlyginima: "))
            session.commit()

    elif pasirinkimas == 4:
        projektai = spausdinti(session)
        trinamas_id = int(input("Pasirinkite norimo atleisti darbuotojo ID: "))
        try:
            trinamas_projektas = session.get(Darbuotojas, trinamas_id)
            session.delete(trinamas_projektas)
            session.commit()
        except Exception as e:
            print(f"Klaida: {e}")

    elif pasirinkimas == 0:
        print("Ačiū už tvarkingą uždarymą")
        break

    else:
        print("Klaida: Neteisingas pasirinkimas")