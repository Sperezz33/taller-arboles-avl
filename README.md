# Talleres de Estructuras de Datos

- **Parcial 1 — Árboles AVL:** https://sperezz33.github.io/taller-arboles-avl/
- **Parcial 2 — Grafos:** https://sperezz33.github.io/taller-arboles-avl/grafos.html

# Taller de Árboles AVL

Página para estudiar **BST y árboles AVL** para el parcial de Estructuras de Datos. Corrige sus respuestas y le explica cada paso.

**Abrir la página:** https://sperezz33.github.io/taller-arboles-avl/

## Qué trae

| Sección | Para qué sirve |
|---|---|
| **Guía** | La receta AVL, la regla del medio, eliminación con predecesor, medidas del árbol (raíz = nivel 0) |
| **Rotaciones rápidas** | Árboles al azar: ponga el nodo en su hueco y rote **arrastrando un nodo encima de su padre**. La página revisa |
| **Taller libre** | Inserte números uno por uno, balancee usted mismo y vea los recorridos |
| **Series** | Pasar de palabras a fórmula ("los primos más 1" → aₙ = pₙ + 1) |
| **Parcial simulado** | Serie → lista → AVL → eliminar 3 nodos → recorridos y medidas |
| **Python** | Sintaxis mínima, ejercicios de completar y **escribir desde cero** (con revisión de errores típicos) |
| **Tuplas** | Nodos con prioridad: comparar tuplas y armar la clave |
| **2-3 y Rojo-Negro** | Reglas básicas y visualizador paso a paso |

## Convenciones

- Profundidad de la raíz = 0; altura de una hoja = 0, árbol vacío = −1
- FB = altura(izquierda) − altura(derecha)
- Eliminar con dos hijos → **predecesor** (el mayor del subárbol izquierdo)

## Código Python

`arboles.py` tiene BST, recorridos, AVL completo (con eliminación) y el ejemplo de nodos con prioridad. Se ejecuta con:

```bash
python arboles.py
```

# Taller de Grafos

**Abrir la página:** https://sperezz33.github.io/taller-arboles-avl/grafos.html

| Sección | Para qué sirve |
|---|---|
| **Guía** | Cuál algoritmo usar, recetas a mano, complejidades y cómo responder el punto 2 |
| **Simulador** | Grafos al azar: BFS, DFS, Dijkstra, Bellman-Ford, Floyd-Warshall, Prim, Kruskal, Borůvka, Ford-Fulkerson y matriz de adyacencia, paso a paso con corrección |
| **¿Qué algoritmo uso?** | 28 enunciados (taller, parcial de las flores y clásicos) con explicación y parámetros |
| **Python** | Sintaxis para grafos y 19 ejercicios desde cero con revisión y esqueleto |

`grafos.py` tiene todos los algoritmos como métodos de la clase `Grafo`, los 10 ejercicios del taller, el problema de las flores y 3 problemas de práctica tipo punto 2:

```bash
python grafos.py
```
