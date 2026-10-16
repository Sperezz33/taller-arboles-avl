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
