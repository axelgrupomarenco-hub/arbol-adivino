class NodoDecision:
    """Representa un nodo del arbol binario de decision."""

    def __init__(self, texto, es_pregunta=False, si=None, no=None):
        self.texto = texto
        self.es_pregunta = es_pregunta
        self.si = si
        self.no = no

    def es_hoja(self):
        return not self.es_pregunta

    def convertir_a_diccionario(self):
        # Se usa un diccionario porque JSON no puede guardar objetos directamente.
        datos = {
            "texto": self.texto,
            "es_pregunta": self.es_pregunta,
        }

        if self.es_pregunta:
            datos["si"] = self.si.convertir_a_diccionario()
            datos["no"] = self.no.convertir_a_diccionario()

        return datos

    @staticmethod
    def crear_desde_diccionario(datos):
        # Estas validaciones evitan cargar archivos dañados o con estructura incorrecta.
        if not isinstance(datos, dict):
            raise ValueError("El nodo debe ser un diccionario.")

        texto = datos.get("texto")
        es_pregunta = datos.get("es_pregunta")

        if not isinstance(texto, str) or not texto.strip():
            raise ValueError("El nodo no tiene texto valido.")

        if not isinstance(es_pregunta, bool):
            raise ValueError("El nodo no indica si es pregunta o respuesta.")

        if not es_pregunta:
            return NodoDecision(texto.strip(), es_pregunta=False)

        if "si" not in datos or "no" not in datos:
            raise ValueError("Un nodo de pregunta debe tener ramas si y no.")

        nodo_si = NodoDecision.crear_desde_diccionario(datos["si"])
        nodo_no = NodoDecision.crear_desde_diccionario(datos["no"])
        return NodoDecision(texto.strip(), es_pregunta=True, si=nodo_si, no=nodo_no)
