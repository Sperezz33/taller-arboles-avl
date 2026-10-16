# ============================================================
#  ARBOLES BST y AVL en Python (version para estudiar a mano)
#
#  Convenciones (las de su profe):
#    - profundidad de la raiz = 0
#    - altura de una hoja = 0, arbol vacio = -1
#    - eliminar nodo con dos hijos -> PREDECESOR
#      (el mayor del subarbol izquierdo)
#    - FB (factor de balance) = altura(izq) - altura(der)
# ============================================================


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None
        self.altura = 0          # solo lo usa el AVL


# ======================== BST ========================

def insertar_bst(nodo, valor):
    if nodo is None:
        return Nodo(valor)
    if valor < nodo.valor:
        nodo.izq = insertar_bst(nodo.izq, valor)
    elif valor > nodo.valor:
        nodo.der = insertar_bst(nodo.der, valor)
    return nodo


def buscar(nodo, valor):
    if nodo is None:
        return False
    if valor == nodo.valor:
        return True
    if valor < nodo.valor:
        return buscar(nodo.izq, valor)
    return buscar(nodo.der, valor)


def maximo(nodo):
    # el predecesor de X es maximo(X.izq)
    while nodo.der is not None:
        nodo = nodo.der
    return nodo


def eliminar_bst(nodo, valor):
    if nodo is None:
        return None
    if valor < nodo.valor:
        nodo.izq = eliminar_bst(nodo.izq, valor)
    elif valor > nodo.valor:
        nodo.der = eliminar_bst(nodo.der, valor)
    else:
        # caso 1 y 2: hoja o un solo hijo
        if nodo.izq is None:
            return nodo.der
        if nodo.der is None:
            return nodo.izq
        # caso 3: dos hijos -> predecesor
        pred = maximo(nodo.izq)
        nodo.valor = pred.valor
        nodo.izq = eliminar_bst(nodo.izq, pred.valor)
    return nodo


# ===================== RECORRIDOS =====================

def inorden(nodo, res):
    if nodo is not None:
        inorden(nodo.izq, res)
        res.append(nodo.valor)
        inorden(nodo.der, res)


def preorden(nodo, res):
    if nodo is not None:
        res.append(nodo.valor)
        preorden(nodo.izq, res)
        preorden(nodo.der, res)


def postorden(nodo, res):
    if nodo is not None:
        postorden(nodo.izq, res)
        postorden(nodo.der, res)
        res.append(nodo.valor)


def anchura(raiz):
    # recorrido por niveles (BFS) usando una lista como cola
    res = []
    if raiz is None:
        return res
    cola = [raiz]
    while len(cola) > 0:
        actual = cola.pop(0)
        res.append(actual.valor)
        if actual.izq is not None:
            cola.append(actual.izq)
        if actual.der is not None:
            cola.append(actual.der)
    return res


def altura(nodo):
    if nodo is None:
        return -1
    return 1 + max(altura(nodo.izq), altura(nodo.der))


def profundidad(nodo, valor):
    d = 0
    while nodo is not None:
        if valor == nodo.valor:
            return d
        if valor < nodo.valor:
            nodo = nodo.izq
        else:
            nodo = nodo.der
        d += 1
    return -1                    # no esta


def contar_hojas(nodo):
    if nodo is None:
        return 0
    if nodo.izq is None and nodo.der is None:
        return 1
    return contar_hojas(nodo.izq) + contar_hojas(nodo.der)


# ======================== AVL ========================

def h(nodo):
    if nodo is None:
        return -1
    return nodo.altura


def actualizar(nodo):
    nodo.altura = 1 + max(h(nodo.izq), h(nodo.der))


def fb(nodo):
    return h(nodo.izq) - h(nodo.der)


def rotar_derecha(y):
    x = y.izq
    t2 = x.der
    x.der = y
    y.izq = t2
    actualizar(y)                # primero el que quedo abajo
    actualizar(x)
    return x                     # x es la nueva raiz del subarbol


def rotar_izquierda(x):
    y = x.der
    t2 = y.izq
    y.izq = x
    x.der = t2
    actualizar(x)
    actualizar(y)
    return y


def balancear(nodo):
    actualizar(nodo)
    b = fb(nodo)
    if b > 1:                            # pesa a la izquierda
        if fb(nodo.izq) < 0:             # zig-zag: caso LR
            nodo.izq = rotar_izquierda(nodo.izq)
        return rotar_derecha(nodo)       # caso LL
    if b < -1:                           # pesa a la derecha
        if fb(nodo.der) > 0:             # zig-zag: caso RL
            nodo.der = rotar_derecha(nodo.der)
        return rotar_izquierda(nodo)     # caso RR
    return nodo


def insertar_avl(nodo, valor):
    if nodo is None:
        return Nodo(valor)
    if valor < nodo.valor:
        nodo.izq = insertar_avl(nodo.izq, valor)
    elif valor > nodo.valor:
        nodo.der = insertar_avl(nodo.der, valor)
    else:
        return nodo                      # repetido: no se inserta
    return balancear(nodo)


def eliminar_avl(nodo, valor):
    if nodo is None:
        return None
    if valor < nodo.valor:
        nodo.izq = eliminar_avl(nodo.izq, valor)
    elif valor > nodo.valor:
        nodo.der = eliminar_avl(nodo.der, valor)
    else:
        if nodo.izq is None:
            return nodo.der
        if nodo.der is None:
            return nodo.izq
        pred = maximo(nodo.izq)
        nodo.valor = pred.valor
        nodo.izq = eliminar_avl(nodo.izq, pred.valor)
    return balancear(nodo)


class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        self.raiz = insertar_avl(self.raiz, valor)

    def eliminar(self, valor):
        self.raiz = eliminar_avl(self.raiz, valor)


# ============ NODOS CON TUPLAS Y PRIORIDAD ============
# Python compara tuplas campo por campo, de izquierda a derecha:
#   (3, 1, 20) < (3, 2, 5)   -> True  (empatan en 3, decide el 1 < 2)
# Entonces: ponga primero el campo MAS importante.
# Si un campo es "mayor primero", pongale signo menos.

class Evento:
    def __init__(self, prioridad, magnitud, id):
        self.prioridad = prioridad
        self.magnitud = magnitud
        self.id = id

    def clave(self):
        # 1. magnitud (mayor primero)  2. prioridad (menor primero)  3. id
        return (-self.magnitud, self.prioridad, self.id)

    def __lt__(self, otro):
        # con esto "a < b" funciona directo entre eventos
        return self.clave() < otro.clave()

    def __repr__(self):
        return f"#{self.id}(p={self.prioridad}, m={self.magnitud})"


def insertar_evento(nodo, ev):
    if nodo is None:
        return Nodo(ev)
    if ev.clave() < nodo.valor.clave():
        nodo.izq = insertar_evento(nodo.izq, ev)
    else:                                # el id es unico: nunca empatan
        nodo.der = insertar_evento(nodo.der, ev)
    return nodo


# ======================== DIBUJO ========================

def imprimir(nodo, nivel=0):
    # dibuja el arbol de lado: la raiz a la izquierda, la derecha arriba
    if nodo is not None:
        imprimir(nodo.der, nivel + 1)
        print("      " * nivel + str(nodo.valor))
        imprimir(nodo.izq, nivel + 1)


# ======================== DEMO ========================

def primos(n):
    res = []
    x = 2
    while len(res) < n:
        es_primo = True
        for d in range(2, x):
            if x % d == 0:
                es_primo = False
        if es_primo:
            res.append(x)
        x += 1
    return res


if __name__ == "__main__":
    serie = [p + 1 for p in primos(15)]      # "los primos mas 1"
    print("Serie:", serie)

    arbol = ArbolAVL()
    for x in serie:
        arbol.insertar(x)
    imprimir(arbol.raiz)

    for x in [20, 4, 32]:
        arbol.eliminar(x)
    print("\nDespues de eliminar 20, 4 y 32:")
    imprimir(arbol.raiz)

    r = []
    inorden(arbol.raiz, r)
    print("Inorden:  ", r)
    r = []
    preorden(arbol.raiz, r)
    print("Preorden: ", r)
    r = []
    postorden(arbol.raiz, r)
    print("Postorden:", r)
    print("Anchura:  ", anchura(arbol.raiz))
    print("Altura:   ", altura(arbol.raiz))
    print("Profundidad de 44:", profundidad(arbol.raiz, 44))
    print("Hojas:    ", contar_hojas(arbol.raiz))

    print("\nEventos (magnitud mayor primero, luego prioridad, luego id):")
    eventos = [Evento(1, 3, 25), Evento(2, 5, 11), Evento(1, 5, 40), Evento(3, 3, 7)]
    raiz = None
    for e in eventos:
        raiz = insertar_evento(raiz, e)
    r = []
    inorden(raiz, r)
    print(r)
