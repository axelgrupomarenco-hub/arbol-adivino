import json
import os

from clases.arbol_decision import ArbolDecision


class GestorArchivos:
    """Carga y guarda arboles de decision en archivos JSON."""

    def __init__(self, ruta_por_defecto):
        self.ruta_actual = ruta_por_defecto

    def cargar_arbol(self, ruta):
        if not ruta or not os.path.exists(ruta):
            raise FileNotFoundError("El archivo seleccionado no existe.")

        if os.path.getsize(ruta) == 0:
            raise ValueError("El archivo esta vacio.")

        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except json.JSONDecodeError as error:
            raise ValueError("El archivo no tiene formato JSON valido.") from error

        # La clase ArbolDecision reconstruye los nodos a partir del diccionario.
        arbol = ArbolDecision.crear_desde_diccionario(datos)
        self.ruta_actual = ruta
        return arbol

    def guardar_arbol(self, arbol, ruta=None):
        ruta_guardado = ruta or self.ruta_actual
        carpeta = os.path.dirname(ruta_guardado)

        if carpeta:
            os.makedirs(carpeta, exist_ok=True)

        # ensure_ascii=False permite guardar tildes y signos en español correctamente.
        with open(ruta_guardado, "w", encoding="utf-8") as archivo:
            json.dump(arbol.convertir_a_diccionario(), archivo, indent=4, ensure_ascii=False)

        self.ruta_actual = ruta_guardado
        return ruta_guardado
