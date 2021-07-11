import unittest
import mock
from Proyecto_Final.Codigo.Votaciones import Votaciones


class TestVotaciones(unittest.TestCase):
    def setUp(self) -> None:
        self._target = Votaciones("dummy", "dummy", "dummy")
        self._distelec = """101001,SAN JOSE,CENTRAL,HOSPITAL                                                                                               
        101007,SAN JOSE,CENTRAL,HATILLO"""
        self._padron = """100339724,109007, ,20231119,00000,JOSE,DELGADO,CORRALES                  
        100842598,108001, ,20261024,00000,CARMEN                        ,CORRALES                  ,MORALES                                     
        101019387,101026, ,20230416,00000,CLAUDIA MANUELA               ,ESPINOZA                  ,FONSECA"""
        self._distelec_return = mock.mock_open(read_data=self._distelec).return_value
        self._padron_return = mock.mock_open(read_data=self._padron).return_value

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
