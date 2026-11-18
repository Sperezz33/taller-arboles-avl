# ============================================================
#  GRAFOS en Python (version para estudiar a mano)
#
#  Todo va como METODOS de la clase Grafo (asi lo pide el profe).
#  Representacion: diccionario de diccionarios en self.ady
#     self.ady = {'A': {'B': 4, 'C': 2}, 'B': {'A': 4}, 'C': {'A': 2}}
#     self.ady[u][v] = peso de la arista u -> v   (sin pesos: 1)
#  No dirigido: la arista se guarda en los dos sentidos.
#
#  sorted(...) solo se usa para que los empates salgan en orden
#  alfabetico (como se hace a mano). Si el profe prohibe sorted(),
#  quitelo: el algoritmo sigue siendo correcto, solo cambia cual
#  empate se toma primero.
# ============================================================

INF = float('inf')


class Grafo:
    def __init__(self, dirigido=False):
        self.ady = {}
        self.dirigido = dirigido

    def agregar_vertice(self, v):
        if v not in self.ady:
            self.ady[v] = {}

    def agregar_arista(self, u, v, peso=1):
        self.agregar_vertice(u)
        self.agregar_vertice(v)
        self.ady[u][v] = peso
        if not self.dirigido:
            self.ady[v][u] = peso

    # ===================== RECORRIDOS =====================

    def bfs(self, inicio):
        # anchura: una COLA (el primero que entra es el primero que sale)
        visitados = [inicio]
        cola = [inicio]
        orden = []
        while len(cola) > 0:
            u = cola.pop(0)
            orden.append(u)
            for v in sorted(self.ady[u]):
                if v not in visitados:
                    visitados.append(v)
                    cola.append(v)
        return orden

    def dfs(self, inicio, visitados=None):
        # profundidad: recursivo (baja lo mas que pueda antes de devolverse)
        if visitados is None:
            visitados = []
        visitados.append(inicio)
        for v in sorted(self.ady[inicio]):
            if v not in visitados:
                self.dfs(v, visitados)
        return visitados

    def dfs_pila(self, inicio):
        # profundidad con PILA: da el mismo orden que el recursivo
        visitados = []
        pila = [inicio]
        while len(pila) > 0:
            u = pila.pop()
            if u not in visitados:
                visitados.append(u)
                for v in sorted(self.ady[u], reverse=True):
                    if v not in visitados:
                        pila.append(v)
        return visitados

    # ================= CAMINOS MAS CORTOS =================

    def dijkstra(self, inicio):
        # pesos NO negativos. Devuelve distancias y "de donde vengo" (prev)
        dist = {}
        prev = {}
        for v in self.ady:
            dist[v] = INF
            prev[v] = None
        dist[inicio] = 0
        pendientes = list(self.ady)
        while len(pendientes) > 0:
            u = pendientes[0]                   # el pendiente de menor distancia
            for v in pendientes:
                if dist[v] < dist[u] or (dist[v] == dist[u] and v < u):
                    u = v
            if dist[u] == INF:
                break                           # lo que queda no se alcanza
            pendientes.remove(u)
            for v in self.ady[u]:
                if v in pendientes and dist[u] + self.ady[u][v] < dist[v]:
                    dist[v] = dist[u] + self.ady[u][v]
                    prev[v] = u
        return dist, prev

    def dijkstra_heap(self, inicio):
        # la misma idea con cola de prioridad (mas rapida)
        import heapq
        dist = {v: INF for v in self.ady}
        prev = {v: None for v in self.ady}
        dist[inicio] = 0
        cola = [(0, inicio)]
        visitados = set()
        while len(cola) > 0:
            d, u = heapq.heappop(cola)
            if u in visitados:
                continue
            visitados.add(u)
            for v in sorted(self.ady[u]):
                if d + self.ady[u][v] < dist[v]:
                    dist[v] = d + self.ady[u][v]
                    prev[v] = u
                    heapq.heappush(cola, (dist[v], v))
        return dist, prev

    def camino(self, prev, destino):
        # reconstruye la ruta caminando hacia atras con prev
        ruta = []
        while destino is not None:
            ruta.append(destino)
            destino = prev[destino]
        ruta.reverse()
        return ruta

    def bellman_ford(self, inicio):
        # acepta pesos negativos y detecta ciclos negativos
        dist = {}
        prev = {}
        for v in self.ady:
            dist[v] = INF
            prev[v] = None
        dist[inicio] = 0
        aristas = []
        for u in sorted(self.ady):
            for v in sorted(self.ady[u]):
                aristas.append((u, v, self.ady[u][v]))
        for i in range(len(self.ady) - 1):       # V - 1 rondas
            for u, v, peso in aristas:
                if dist[u] + peso < dist[v]:
                    dist[v] = dist[u] + peso
                    prev[v] = u
        for u, v, peso in aristas:               # una ronda mas: si mejora, hay ciclo negativo
            if dist[u] + peso < dist[v]:
                return None, None
        return dist, prev

    def floyd_warshall(self):
        # todas las parejas. Matriz d[i][j]; se prueba pasar por k
        vs = sorted(self.ady)
        n = len(vs)
        d = []
        for i in range(n):
            fila = []
            for j in range(n):
                if i == j:
                    fila.append(0)
                elif vs[j] in self.ady[vs[i]]:
                    fila.append(self.ady[vs[i]][vs[j]])
                else:
                    fila.append(INF)
            d.append(fila)
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if d[i][k] + d[k][j] < d[i][j]:
                        d[i][j] = d[i][k] + d[k][j]
        return vs, d

    # ============== ARBOL DE EXPANSION MINIMA ==============

    def prim(self, inicio):
        # crece UN arbol: siempre la arista mas barata que sale del arbol
        en_arbol = [inicio]
        aristas = []
        total = 0
        while len(en_arbol) < len(self.ady):
            mejor = None
            for u in sorted(en_arbol):
                for v in sorted(self.ady[u]):
                    if v not in en_arbol:
                        if mejor is None or self.ady[u][v] < mejor[2]:
                            mejor = (u, v, self.ady[u][v])
            if mejor is None:
                break                                # grafo no conexo
            en_arbol.append(mejor[1])
            aristas.append(mejor)
            total += mejor[2]
        return aristas, total

    def kruskal(self):
        # ordena TODAS las aristas y las toma si no forman ciclo
        lista = []
        for u in self.ady:
            for v in self.ady[u]:
                if u < v:
                    lista.append((self.ady[u][v], u, v))
        lista.sort()                                 # sin sort(): sacar el minimo cada vez
        padre = {}
        for v in self.ady:
            padre[v] = v
        aristas = []
        total = 0
        for peso, u, v in lista:
            ru = buscar(padre, u)
            rv = buscar(padre, v)
            if ru != rv:                             # distinto grupo: no hay ciclo
                padre[ru] = rv
                aristas.append((u, v, peso))
                total += peso
        return aristas, total

    def boruvka(self):
        # cada componente escoge su arista mas barata hacia afuera, todas a la vez
        padre = {}
        for v in self.ady:
            padre[v] = v
        aristas = []
        total = 0
        componentes = len(self.ady)
        while componentes > 1:
            barata = {}
            for u in self.ady:
                for v in self.ady[u]:
                    ru = buscar(padre, u)
                    rv = buscar(padre, v)
                    if ru != rv:
                        a = (self.ady[u][v], min(u, v), max(u, v))
                        if ru not in barata or a < barata[ru]:
                            barata[ru] = a
            if len(barata) == 0:
                break                                # grafo no conexo
            for peso, u, v in sorted(set(barata.values())):
                ru = buscar(padre, u)
                rv = buscar(padre, v)
                if ru != rv:
                    padre[ru] = rv
                    aristas.append((u, v, peso))
                    total += peso
                    componentes -= 1
        return aristas, total

    # ===================== FLUJO MAXIMO =====================

    def ford_fulkerson(self, fuente, sumidero):
        # grafo dirigido con capacidades. Caminos de aumento buscados con BFS
        residual = {}
        for u in self.ady:
            residual[u] = {}
        for u in self.ady:
            for v in self.ady[u]:
                residual[u][v] = self.ady[u][v]
        for u in self.ady:
            for v in self.ady[u]:
                if u not in residual[v]:
                    residual[v][u] = 0               # arista de regreso
        flujo = 0
        caminos = []
        while True:
            prev = {fuente: None}
            cola = [fuente]
            while len(cola) > 0 and sumidero not in prev:
                u = cola.pop(0)
                for v in sorted(residual[u]):
                    if v not in prev and residual[u][v] > 0:
                        prev[v] = u
                        cola.append(v)
            if sumidero not in prev:
                break                                # ya no hay camino: termina
            cuello = INF
            v = sumidero
            while prev[v] is not None:
                cuello = min(cuello, residual[prev[v]][v])
                v = prev[v]
            v = sumidero
            while prev[v] is not None:
                residual[prev[v]][v] -= cuello
                residual[v][prev[v]] += cuello
                v = prev[v]
            flujo += cuello
            caminos.append((self.camino(prev, sumidero), cuello))
        return flujo, caminos

    # ================= MATRIZ DE ADYACENCIA =================

    def matriz_adyacencia(self):
        vs = sorted(self.ady)
        m = []
        for u in vs:
            fila = []
            for v in vs:
                if v in self.ady[u]:
                    fila.append(self.ady[u][v])
                else:
                    fila.append(0)
            m.append(fila)
        return vs, m

    # ===================== TALLER =====================

    def rodeados_de_primos(self):                       # 1
        res = []
        for v in sorted(self.ady):
            if len(self.ady[v]) == 0:
                continue
            todos = True
            for w in self.ady[v]:
                if not (es_primo(w) and w > 3):
                    todos = False
            if todos:
                res.append(v)
        return res

    def aviso_concierto(self, inicio):                  # 2 (BFS por niveles)
        minuto = {}
        for v in self.ady:
            minuto[v] = -1
        minuto[inicio] = 0
        cola = [inicio]
        while len(cola) > 0:
            u = cola.pop(0)
            for v in self.ady[u]:
                if minuto[v] == -1:
                    minuto[v] = minuto[u] + 1
                    cola.append(v)
        return minuto

    def recomendaciones(self, persona):                 # 3
        res = []
        for otro in self.ady:
            if otro == persona or otro in self.ady[persona]:
                continue
            comunes = 0
            for amigo in self.ady[persona]:
                if amigo in self.ady[otro]:
                    comunes += 1
            if comunes >= 2:
                res.append((-comunes, otro))
        res.sort()                                   # mayor cantidad primero, luego alfabetico
        salida = []
        for c, nombre in res:
            salida.append((nombre, -c))
        return salida

    def dos_turnos(self):                               # 4 (bipartito con BFS)
        turno = {}
        for s in sorted(self.ady):
            if s in turno:
                continue
            turno[s] = 1
            cola = [s]
            while len(cola) > 0:
                u = cola.pop(0)
                for v in self.ady[u]:
                    if v not in turno:
                        turno[v] = 3 - turno[u]      # 1 -> 2, 2 -> 1
                        cola.append(v)
                    elif turno[v] == turno[u]:
                        return "imposible"
        return turno

    def mayor_donacion(self, aporte):                   # 5 (componentes)
        vistos = []
        grupos = []
        for s in sorted(self.ady):
            if s in vistos:
                continue
            grupo = self.dfs(s)
            vistos += grupo
            total = 0
            for p in grupo:
                total += aporte[p]
            grupos.append((sorted(grupo), total))
        mejor = 0
        for g, t in grupos:
            if t > mejor:
                mejor = t
        res = []
        for g, t in grupos:
            if t == mejor:
                res.append((g, t))
        return res

    def ruta_accesible(self, origen, destino):          # 6 (Dijkstra filtrando)
        # self.ady[u][v] = (minutos, accesible)
        solo = Grafo(True)
        for u in self.ady:
            solo.agregar_vertice(u)
            for v in self.ady[u]:
                minutos, accesible = self.ady[u][v]
                if accesible:
                    solo.ady[u][v] = minutos
        dist, prev = solo.dijkstra(origen)
        if dist[destino] == INF:
            return "sin ruta accesible"
        return self.camino(prev, destino), dist[destino]

    def semestres(self):                                # 7 (orden topologico)
        entrada = {}
        for v in self.ady:
            entrada[v] = 0
        for u in self.ady:
            for v in self.ady[u]:
                entrada[v] += 1
        semestre = {}
        cola = []
        for v in self.ady:
            if entrada[v] == 0:
                semestre[v] = 1
                cola.append(v)
        procesadas = 0
        while len(cola) > 0:
            u = cola.pop(0)
            procesadas += 1
            for v in self.ady[u]:
                semestre[v] = max(semestre.get(v, 0), semestre[u] + 1)
                entrada[v] -= 1
                if entrada[v] == 0:
                    cola.append(v)
        if procesadas < len(self.ady):
            return "plan imposible"
        return semestre

    def puesto_cercano(self, puestos):                  # 8 (BFS desde cada puesto)
        distancias = {}
        for p in puestos:
            distancias[p] = self.aviso_concierto(p)    # mismo BFS por niveles
        res = {}
        for zona in self.ady:
            mejor = None
            for p in puestos:
                d = distancias[p][zona]
                if d != -1:
                    if mejor is None or d < mejor[1] or (d == mejor[1] and p < mejor[0]):
                        mejor = (p, d)
            if mejor is None:
                res[zona] = "sin cobertura"
            else:
                res[zona] = mejor
        return res

    def ida_y_vuelta(self, inicio):                     # 9
        ida = self.dfs(inicio)
        reverso = Grafo(True)
        for v in self.ady:
            reverso.agregar_vertice(v)
        for u in self.ady:
            for v in self.ady[u]:
                reverso.agregar_arista(v, u)          # se voltean las flechas
        vuelta = reverso.dfs(inicio)
        res = []
        for v in ida:
            if v in vuelta and v != inicio:
                res.append(v)
        return res

    def carreteras_criticas(self, capital):             # 10
        res = []
        for u in sorted(self.ady):
            for v in sorted(self.ady[u]):
                if u < v:
                    peso = self.ady[u][v]
                    del self.ady[u][v]               # cerrar la carretera
                    del self.ady[v][u]
                    aislados = len(self.ady) - len(self.bfs(capital))
                    self.ady[u][v] = peso            # volverla a abrir
                    self.ady[v][u] = peso
                    if aislados > 0:
                        res.append(((u, v), aislados))
        return res

    # ============ PARCIAL (otro grupo): RECOGER FLORES ============

    def recoger_flores(self, parcelas, pedidos, inicio):
        # parcelas[v] = [tipo, cantidad]   pedidos = [(tipo, cantidad), ...]
        actual = inicio
        resultados = []
        for tipo, cantidad in pedidos:                # en orden de llegada
            falta = cantidad
            for v in self.dfs(actual):                # recorrido por profundidad
                actual = v
                if parcelas[v][0] == tipo and parcelas[v][1] > 0:
                    tomar = min(falta, parcelas[v][1])
                    parcelas[v][1] -= tomar
                    falta -= tomar
                if falta == 0:
                    break
            if falta == 0:
                resultados.append((tipo, cantidad, "completo"))
            else:
                resultados.append((tipo, cantidad - falta, "incompleto"))
        dist, prev = self.dijkstra(actual)            # regreso: camino mas corto
        return resultados, self.camino(prev, inicio), dist[inicio]

    # ========= PRACTICA: problemas tipo "punto 2" (inventados) =========

    def entregar_pedidos(self, inicio, destinos):
        # Dijkstra desde donde esta el robot hasta cada destino, en orden
        actual = inicio
        ruta = [inicio]
        costo = 0
        no_entregados = []
        for d in destinos:
            dist, prev = self.dijkstra(actual)
            if dist[d] == INF:
                no_entregados.append(d)
                continue
            ruta += self.camino(prev, d)[1:]          # [1:] para no repetir 'actual'
            costo += dist[d]
            actual = d
        dist, prev = self.dijkstra(actual)            # volver al inicio
        ruta += self.camino(prev, inicio)[1:]
        costo += dist[inicio]
        return ruta, costo, no_entregados

    def buscar_libro(self, inicio, inventario, libro, copias):
        # BFS: primero las bibliotecas mas cercanas; se DETIENE al completar
        # inventario[v] = {'libro': cantidad, ...}
        saltos = {inicio: 0}
        cola = [inicio]
        res = []
        falta = copias
        while len(cola) > 0 and falta > 0:
            u = cola.pop(0)
            hay = inventario[u].get(libro, 0)
            if hay > 0:
                tomar = min(hay, falta)
                falta -= tomar
                res.append((u, tomar, saltos[u]))
            for v in sorted(self.ady[u]):
                if v not in saltos:
                    saltos[v] = saltos[u] + 1
                    cola.append(v)
        return res, falta

    def cablear(self, presupuesto):
        # Kruskal que se detiene cuando la plata no alcanza
        lista = []
        for u in self.ady:
            for v in self.ady[u]:
                if u < v:
                    lista.append((self.ady[u][v], u, v))
        lista.sort()
        padre = {}
        for v in self.ady:
            padre[v] = v
        grupos = len(self.ady)
        aristas = []
        gastado = 0
        for peso, u, v in lista:
            if gastado + peso > presupuesto:
                break                                # las que siguen son igual o mas caras
            ru = buscar(padre, u)
            rv = buscar(padre, v)
            if ru != rv:
                padre[ru] = rv
                aristas.append((u, v, peso))
                gastado += peso
                grupos -= 1
        return aristas, gastado, grupos


def buscar(padre, x):
    # union-find: sube hasta la raiz del grupo
    while padre[x] != x:
        x = padre[x]
    return x


def es_primo(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def crear(aristas, dirigido=False, vertices=()):
    # aristas: [(u, v)] o [(u, v, peso)]
    g = Grafo(dirigido)
    for v in vertices:
        g.agregar_vertice(v)
    for a in aristas:
        if len(a) == 2:
            g.agregar_arista(a[0], a[1])
        else:
            g.agregar_arista(a[0], a[1], a[2])
    return g


# ======================== DEMO ========================

if __name__ == "__main__":
    g = crear([('A', 'B', 4), ('A', 'C', 2), ('B', 'C', 1), ('B', 'D', 5),
               ('C', 'D', 8), ('C', 'E', 10), ('D', 'E', 2)])
    print("BFS desde A:      ", g.bfs('A'))
    print("DFS desde A:      ", g.dfs('A'))
    dist, prev = g.dijkstra('A')
    print("Dijkstra A:       ", dist, " camino a E:", g.camino(prev, 'E'))
    print("Prim desde A:     ", g.prim('A'))
    print("Kruskal:          ", g.kruskal())
    print("Boruvka:          ", g.boruvka())
    vs, d = g.floyd_warshall()
    print("Floyd-Warshall:   ", vs)
    for fila in d:
        print("                  ", fila)
    red = crear([('s', 'a', 10), ('s', 'b', 5), ('a', 'b', 15), ('a', 't', 10),
                 ('b', 't', 10)], dirigido=True)
    print("Ford-Fulkerson:   ", red.ford_fulkerson('s', 't'))
