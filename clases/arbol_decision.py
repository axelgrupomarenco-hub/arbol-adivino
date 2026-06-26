from clases.nodo import NodoDecision


class ArbolDecision:
    """Controla el recorrido y aprendizaje del arbol."""

    def __init__(self, raiz=None):
        self.raiz = raiz if raiz else self.crear_arbol_por_defecto()
        self.nodo_actual = self.raiz

    def crear_arbol_por_defecto(self):
        return NodoDecision(
            "¿Es una comida dulce?",
            es_pregunta=True,
            si=NodoDecision("pastel"),
            no=NodoDecision("pizza"),
        )

    def reiniciar(self):
        self.nodo_actual = self.raiz

    def obtener_texto_actual(self):
        return self.nodo_actual.texto

    def actual_es_pregunta(self):
        return self.nodo_actual.es_pregunta

    def responder(self, respuesta_si):
        if self.nodo_actual.es_hoja():
            return

        # En un arbol binario se avanza por una de dos ramas: si o no.
        self.nodo_actual = self.nodo_actual.si if respuesta_si else self.nodo_actual.no

    def aprender(self, respuesta_correcta, nueva_pregunta, respuesta_si_para_nueva):
        respuesta_anterior = self.nodo_actual.texto

        nodo_respuesta_anterior = NodoDecision(respuesta_anterior, es_pregunta=False)
        nodo_respuesta_nueva = NodoDecision(respuesta_correcta, es_pregunta=False)

        self.nodo_actual.texto = nueva_pregunta
        self.nodo_actual.es_pregunta = True

        # El nodo que antes era una respuesta se transforma en pregunta.
        # Luego se conectan la respuesta nueva y la respuesta anterior.
        if respuesta_si_para_nueva:
            self.nodo_actual.si = nodo_respuesta_nueva
            self.nodo_actual.no = nodo_respuesta_anterior
        else:
            self.nodo_actual.si = nodo_respuesta_anterior
            self.nodo_actual.no = nodo_respuesta_nueva

    def convertir_a_diccionario(self):
        return self.raiz.convertir_a_diccionario()

    @staticmethod
    def crear_desde_diccionario(datos):
        raiz = NodoDecision.crear_desde_diccionario(datos)
        return ArbolDecision(raiz)
