import xml.etree.ElementTree as ET

class ElementoXML:
    """Clase base para representar elementos XML."""
    
    # Herencia: ElementoHoja y ElementoPadre heredan de ElementoXML
    def __init__(self, nombre, atributos):
        self.nombre = nombre
        self.atributos = atributos

    def __str__(self):
        return f"<{self.nombre} {self.atributos_str()}>"

    def atributos_str(self):
        if self.atributos:
            return " ".join(f'{k}="{v}"' for k, v in self.atributos.items())
        else:
            return ""

    def procesar(self, visitador):
        visitador.visitar(self)  # Polimorfismo de inclusion: Invocación del método visitar dependiendo del tipo de objeto.

class ElementoHoja(ElementoXML):
    """Clase para representar elementos XML hoja (sin subelementos)."""
    
    # Herencia: ElementoHoja hereda de ElementoXML
    def __init__(self, nombre, atributos, contenido):
        super().__init__(nombre, atributos)
        self.contenido = contenido

    def __str__(self):
        return f"{super().__str__()}>{self.contenido}</{self.nombre}>"

    def procesar(self, visitador):
        visitador.visitar_hoja(self)  # Polimorfismo de inclusion: Invocación del método visitar_hoja dependiendo del tipo de objeto.

class ElementoPadre(ElementoXML):
    """Clase para representar elementos XML padre (con subelementos)."""
    
    # Herencia: ElementoPadre hereda de ElementoXML
    def __init__(self, nombre, atributos, elementos_hijos):
        super().__init__(nombre, atributos)
        self.elementos_hijos = elementos_hijos

    def __str__(self):
        return f"{super().__str__()}\n{''.join(str(elemento) for elemento in self.elementos_hijos)}\n</{self.nombre}>"

    def procesar(self, visitador):
        visitador.visitar_padre(self, self.elementos_hijos)  # Polimorfismo de inclusion: Invocación del método visitar_padre dependiendo del tipo de objeto.


class Visitador:
    """Interfaz para definir cómo procesar los elementos XML."""

    def visitar(self, elemento):
        raise NotImplementedError

    def visitar_hoja(self, elemento_hoja):
        raise NotImplementedError

    def visitar_padre(self, elemento_padre, elementos_hijos):
        raise NotImplementedError

class VisitadorImpresion(Visitador):
    """Visitador que imprime la información de los elementos XML."""

    def visitar(self, elemento):
        print(f"Elemento: {elemento.nombre}")
        print(f"Atributos: {elemento.atributos}")

    def visitar_hoja(self, elemento_hoja):
        print(f"Elemento: {elemento_hoja.nombre}")
        print(f"Atributos: {elemento_hoja.atributos}")
        if elemento_hoja.contenido is not None:
            print(f"Contenido: {elemento_hoja.contenido}")

    def visitar_padre(self, elemento_padre, elementos_hijos):
        print(f"Elemento: {elemento_padre.nombre}")
        print(f"Atributos: {elemento_padre.atributos}")
        print("Subelementos:")
        for elemento_hijo in elementos_hijos:
            elemento_hijo.procesar(self)  # Polimorfismo de inclusion: Invocación del método procesar dependiendo del tipo de objeto.

def construir_arbol_xml(ruta_archivo):
    arbol = ET.parse(ruta_archivo)
    raiz = arbol.getroot()

    def procesar_nodo(nodo):
        nombre = nodo.tag
        atributos = nodo.attrib

        if nodo.text:
            contenido = nodo.text.strip()
        else:
            contenido = None

        if nodo.findall("*"):
            elementos_hijos = [procesar_nodo(hijo) for hijo in nodo]
            return ElementoPadre(nombre, atributos, elementos_hijos)
        else:
            return ElementoHoja(nombre, atributos, contenido)

    return procesar_nodo(raiz)

def main():
    ruta_archivo_xml = "C:/Users/glsx0/Downloads/Documento.xml" #Recuerde cambiar esta ruta.
    arbol_xml = construir_arbol_xml(ruta_archivo_xml)
    visitador = VisitadorImpresion()

    arbol_xml.procesar(visitador)

if __name__ == "__main__":
    main()
