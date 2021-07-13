import unittest
import mock
from Proyecto_Final.Codigo.Votaciones import Votaciones
import io
from Mock_URL import url
import requests


class TestVotaciones(unittest.TestCase):
    def setUp(self) -> None:
        self._target = Votaciones("dummy", "dummy", "dummy")
        self._distelec = """101001,SAN JOSE,CENTRAL,HOSPITAL                                                          
        108001,SAN JOSE,CENTRAL,HATILLO"""
        self._padron = """100339724,109007, ,20231119,00000,JOSE,DELGADO,CORRALES         
        100842598,108001, ,20261024,00000,CARMEN                        ,CORRALES                  ,MORALES           
        101019387,101026, ,20230416,00000,CLAUDIA MANUELA               ,ESPINOZA                  ,FONSECA"""
        self._distelec_return = mock.mock_open(read_data=self._distelec).return_value
        self._padron_return = mock.mock_open(read_data=self._padron).return_value
        self._url_return = url

    # Caso 1
    @mock.patch("Proyecto_Final.Codigo.Votaciones.requests")
    @mock.patch("Proyecto_Final.Codigo.Votaciones.input")
    @mock.patch("Proyecto_Final.Codigo.Votaciones.open")
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_todo_sale_bien(self, mock_stdout, mock_open, mock_input, mock_requests):
        mock_open.side_effect = [self._distelec_return, self._padron_return]
        mock_input.side_effect = ["100842598", "13/12/1998"]
        mock_requests.get.return_value.content = url
        self._target.run()
        target_output = mock_stdout.getvalue()
        expected_output = """Hola CARMEN
Su nombre completo es: CARMEN CORRALES MORALES
Su edad es: 22
Su centro de votacion se ubica en:
	Provincia: SAN JOSE
	Canton: CENTRAL
	Distrito: HATILLO
La lista de candidatos es la siguiente:
                        Partido                            Candidato    Tipo de candidato
0           Liberación Nacional            José María Figueres Olsen    Candidato Oficial
1               Nueva República              Fabricio Alvarado Muñoz    Candidato Oficial
2   Progreso Social Democrático                Rodrigo Chaves Robles    Candidato Oficial
3       Unidad Social Cristiana              Lineth Saborío Chaverri    Candidato Oficial
4                Unidos Podemos                Natalia Díaz Quintana    Candidato Oficial
6   Accesibilidad Sin Exclusión             Óscar Andrés López Arias    Candidato Oficial
7              Acción Ciudadana             Marcia González Aguiluz   **Posible Candidato
8              Acción Ciudadana            Carolina Hidalgo Herrera   **Posible Candidato
9              Acción Ciudadana               Welmer Ramos González   **Posible Candidato
10             Acción Ciudadana               Hernán Solano Venegas   **Posible Candidato
11        Movimiento Libertario              Carlos Valenciano Kamer    Candidato Oficial
12             Nueva Generación                     Sergio Mena Díaz    Candidato Oficial
13                Unión Liberal             Federico Malavassi Calvo    Candidato Oficial
14                  Por definir          Juan Diego Castro Fernández  **Posible Candidato
15                  Por definir                       Viviam Quesada  **Posible Candidato
17     Coalición para el Cambio               Eliécer Feinzaig Mintz    Candidato Oficial
18                Frente Amplio  José María Villalta Florez-Estrada     Candidato Oficial
19        Restauración Nacional                 Eduardo Cruickshank   **Posible Candidato
20        Restauración Nacional                        Melvin Nuñez   **Posible Candidato
"""
        self.assertEqual(expected_output, target_output)

    # Caso 2
    @mock.patch("Proyecto_Final.Codigo.Votaciones.input")
    @mock.patch("Proyecto_Final.Codigo.Votaciones.open")
    def test_distelect_formato_incorrecto(self, mock_open, mock_input):
        distelec = """101001-SAN JOSE-CENTRAL-HOSPITAL
108001-SAN JOSE-CENTRAL-HATILLO"""
        distelec_return = mock.mock_open(read_data=distelec).return_value
        mock_open.side_effect = [distelec_return, self._padron_return]
        mock_input.side_effect = ["100842598", "13/12/1998"]
        with self.assertRaises(KeyError):
            self._target.run()

    # Caso 3
    @mock.patch("Proyecto_Final.Codigo.Votaciones.input")
    @mock.patch("Proyecto_Final.Codigo.Votaciones.open")
    def test_padron_formato_incorrecto(self, mock_open, mock_input):
        padron = """100339724-109007- -20231119-00000-JOSE-DELGADO-CORRALES         
100842598-108001- -20261024-00000-CARMEN                        -CORRALES                  -MORALES           
101019387-101026- -20230416-00000-CLAUDIA MANUELA               -ESPINOZA                  -FONSECA"""
        padron_return = mock.mock_open(read_data=padron).return_value
        mock_open.side_effect = [self._distelec_return, padron_return]
        mock_input.side_effect = ["100842598", "13/12/1998"]
        with self.assertRaises(ValueError):
            self._target.run()

    # Caso 4
    @mock.patch("Proyecto_Final.Codigo.Votaciones.input")
    @mock.patch("Proyecto_Final.Codigo.Votaciones.open")
    def test_cedula_caracteres_especiales_y_letras(self, mock_open, mock_input):
        mock_open.side_effect = [self._distelec_return, self._padron_return]
        mock_input.side_effect = ["holi151.<?", "13/12/1998"]
        with self.assertRaises(KeyError):
            self._target.run()

    # Caso 5
    @mock.patch("Proyecto_Final.Codigo.Votaciones.input")
    @mock.patch("Proyecto_Final.Codigo.Votaciones.open")
    def test_cedula_no_encontrada(self, mock_open, mock_input):
        mock_open.side_effect = [self._distelec_return, self._padron_return]
        mock_input.side_effect = ["117110446", "13/06/1998"]
        with self.assertRaises(KeyError):
            self._target.run()

    # Caso 6
    @mock.patch("Proyecto_Final.Codigo.Votaciones.input")
    @mock.patch("Proyecto_Final.Codigo.Votaciones.open")
    def test_fecha_nacimiento_vacio(self, mock_open, mock_input):
        mock_open.side_effect = [self._distelec_return, self._padron_return]
        mock_input.side_effect = ["100842598", ""]
        with self.assertRaises(ValueError):
            self._target.run()

    # Caso 7
    def test_distelect_no_existe(self):
        with self.assertRaises(FileNotFoundError):
            self._target.run()

    # Caso 8
    def test_padron_no_existe(self):
        target = Votaciones("Database/Distelec.txt", "dummy", "dummy")
        with self.assertRaises(FileNotFoundError):
            target.run()

    # Caso 9
    @mock.patch("Proyecto_Final.Codigo.Votaciones.requests")
    @mock.patch("Proyecto_Final.Codigo.Votaciones.input")
    @mock.patch("Proyecto_Final.Codigo.Votaciones.open")
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_formato_fecha_nacimiento_incorrecto(self, mock_stdout, mock_open, mock_input, mock_requests):
        mock_open.side_effect = [self._distelec_return, self._padron_return]
        mock_input.side_effect = ["100842598", "13/12/98"]
        mock_requests.get.return_value.content = url
        self._target.run()
        target_output = mock_stdout.getvalue()
        expected_output = """Hola CARMEN
Su nombre completo es: CARMEN CORRALES MORALES
Su edad es: 1922
Su centro de votacion se ubica en:
\tProvincia: SAN JOSE
\tCanton: CENTRAL
\tDistrito: HATILLO
La lista de candidatos es la siguiente:
                        Partido                            Candidato    Tipo de candidato
0           Liberación Nacional            José María Figueres Olsen    Candidato Oficial
1               Nueva República              Fabricio Alvarado Muñoz    Candidato Oficial
2   Progreso Social Democrático                Rodrigo Chaves Robles    Candidato Oficial
3       Unidad Social Cristiana              Lineth Saborío Chaverri    Candidato Oficial
4                Unidos Podemos                Natalia Díaz Quintana    Candidato Oficial
6   Accesibilidad Sin Exclusión             Óscar Andrés López Arias    Candidato Oficial
7              Acción Ciudadana             Marcia González Aguiluz   **Posible Candidato
8              Acción Ciudadana            Carolina Hidalgo Herrera   **Posible Candidato
9              Acción Ciudadana               Welmer Ramos González   **Posible Candidato
10             Acción Ciudadana               Hernán Solano Venegas   **Posible Candidato
11        Movimiento Libertario              Carlos Valenciano Kamer    Candidato Oficial
12             Nueva Generación                     Sergio Mena Díaz    Candidato Oficial
13                Unión Liberal             Federico Malavassi Calvo    Candidato Oficial
14                  Por definir          Juan Diego Castro Fernández  **Posible Candidato
15                  Por definir                       Viviam Quesada  **Posible Candidato
17     Coalición para el Cambio               Eliécer Feinzaig Mintz    Candidato Oficial
18                Frente Amplio  José María Villalta Florez-Estrada     Candidato Oficial
19        Restauración Nacional                 Eduardo Cruickshank   **Posible Candidato
20        Restauración Nacional                        Melvin Nuñez   **Posible Candidato
"""
        self.assertEqual(expected_output, target_output)

    # Caso 10
    @mock.patch("Proyecto_Final.Codigo.Votaciones.input")
    @mock.patch("Proyecto_Final.Codigo.Votaciones.open")
    def test_fecha_nacimiento_caracteres_especiales_no_esperados(self, mock_open, mock_input):
        mock_open.side_effect = [self._distelec_return, self._padron_return]
        mock_input.side_effect = ["100842598", "13-12-1998"]
        with self.assertRaises(ValueError):
            self._target.run()

    # Caso 12
    @mock.patch("Proyecto_Final.Codigo.Votaciones.input")
    @mock.patch("Proyecto_Final.Codigo.Votaciones.open")
    def test_pagina_no_existe(self, mock_open, mock_input):
        mock_open.side_effect = [self._distelec_return, self._padron_return]
        mock_input.side_effect = ["100842598", "13/06/1998"]
        with self.assertRaises(requests.exceptions.MissingSchema):
            self._target.run()
