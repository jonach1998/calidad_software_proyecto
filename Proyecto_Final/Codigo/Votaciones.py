from datetime import date
import requests
import pandas as pd
import numpy as np


class Votaciones:
    def __init__(self, distelect_path, padron_completo_path, url):
        self._distelect_path = distelect_path
        self._padron_completo_path = padron_completo_path
        self._distelect_dict = dict()
        self._personas_dict = dict()
        self._url = url

    def _get_candidatos(self):
        html = requests.get(self._url).content
        df_list = pd.read_html(html)
        df = df_list[2].convert_dtypes()
        column2 = df[df.columns[2]]
        column4 = df[df.columns[4]]
        df = pd.concat([column2, column4], axis=1, keys=["Partido", "Candidato"]).dropna()
        df = df[~(df.Candidato.str.contains(r"\d") | df.Candidato.str.contains(r"TSE"))]
        df["Candidato"] = df["Candidato"].str.replace("*", "", regex=True)
        df["Candidato"] = df["Candidato"].str.replace("†", "", regex=True)
        df["Candidato"] = df["Candidato"].str.replace("‡", "", regex=True)
        df["Candidato"] = df["Candidato"].str.replace("Δ", "", regex=True)
        df["Oficial"] = df.duplicated(subset=["Partido"], keep=False)
        df["Tipo de candidato"] = np.where(df["Oficial"], "**Posible Candidato", "Candidato Oficial")
        return df[["Partido", "Candidato", "Tipo de candidato"]].to_string()

    def _get_distelect(self):
        with open(self._distelect_path, "r", encoding="windows-1252") as lines:
            for line in lines:
                zipcode, *ubicacion = line.strip().split(",")
                self._distelect_dict.update({zipcode: ubicacion})

    def _get_padron(self):
        with open(self._padron_completo_path, "r", encoding="windows-1252") as padron_completo:
            for line in padron_completo:
                cedula, zipcode, _, fecha_vencimiento_cedula, _, nombre, apellido1, apellido2 = line.strip().split(",")
                self._personas_dict.update({cedula: {"zipcode": zipcode, "cedula_caducidad":
                    fecha_vencimiento_cedula, "nombre": nombre.strip(), "apellido1": apellido1.strip(), "apellido2":
                    apellido2.strip()}})

    @staticmethod
    def _calcular_edad(fecha_de_nacimiento):
        anno_actual, mes_actual, dia_actual = date.today().year, date.today().month, date.today().day
        dia_nacimiento, mes_nacimiento, anno_nacimiento = fecha_de_nacimiento.split("/")
        anno_nacimiento = int(anno_nacimiento)
        mes_nacimiento = int(mes_nacimiento)
        dia_nacimiento = int(dia_nacimiento)
        anno_actual = int(anno_actual)
        mes_actual = int(mes_actual)
        dia_actual = int(dia_actual)
        if mes_nacimiento > mes_actual:
            edad = anno_actual - anno_nacimiento - 1
        elif mes_nacimiento == mes_actual:
            if dia_nacimiento > dia_actual:
                edad = anno_actual - anno_nacimiento - 1
            else:
                edad = anno_actual - anno_nacimiento
        else:
            edad = anno_actual - anno_nacimiento
        return edad

    def run(self):
        self._get_distelect()
        self._get_padron()
        cedula = input("Favor ingrese su cedula sin guiones y con los 0 respectivos: ")
        fecha_de_nacimiento = input("Favor ingresar su fecha de nacimiento en el formato dd/mm/yyyy: ")
        edad = self._calcular_edad(fecha_de_nacimiento)
        nombre = self._personas_dict[cedula]["nombre"]
        apellido1 = self._personas_dict[cedula]["apellido1"]
        apellido2 = self._personas_dict[cedula]["apellido2"]
        zipcode = self._personas_dict[cedula]["zipcode"]
        provincia, canton, distrito = self._distelect_dict[zipcode]
        print("Hola", nombre)
        print("Su nombre completo es:", nombre, apellido1, apellido2)
        print("Su edad es:", edad)
        print("Su centro de votacion se ubica en:")
        print("\tProvincia:", provincia)
        print("\tCanton:", canton)
        print("\tDistrito:", distrito)
        print("La lista de candidatos es la siguiente:")
        print(self._get_candidatos())


if __name__ == "__main__":
    runner = Votaciones("Database/Distelec.txt", "Database/PADRON_COMPLETO.txt",
                        "https://es.wikipedia.org/wiki/Elecciones_generales_de_Costa_Rica_de_2022")
    runner.run()
