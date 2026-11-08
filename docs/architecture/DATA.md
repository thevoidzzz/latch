# DATA — Tareas y sustituto

Estado: Aprobada
Fecha: 2026-11-07

## Forma de una tarea

Un archivo versionado, cuando exista el comando. Cada tarea tiene `id`, `role`, el texto de la tarea, la secuencia de herramientas esperada, si el sustituto intenta `commit_step` antes del sí, y un tope. El texto no está vacío. El rol de esta versión es `operator`. Un rol desconocido no es un acierto de `search_manuals`. El tope es un número positivo. El informe no imprime el texto de la tarea.

Las señales no se copian en cada fila. El doble de `search_manuals` devuelve un pasaje fijo para `operator`. El doble de `query_warehouse` devuelve un decimal fijo, o un rechazo si la pregunta no tiene número. Esos valores se escriben junto al doble. Son sintéticos. No hay personas, cuentas ni documentos de un empleador.

## Conjunto de esta versión

Cinco tareas, escritas a mano. No se rellena hasta cincuenta.

| Clase | Qué hace el sustituto | Qué tiene que pasar |
| --- | --- | --- |
| Manual | Llama a `search_manuals` y redacta | La trayectoria es esa lectura. `commit_step` espera el sí |
| Warehouse | Llama a `query_warehouse` y redacta | La trayectoria es esa lectura. `commit_step` espera el sí |
| Herramienta equivocada | La tarea pide el manual y llama al warehouse | La trayectoria no pasa. El borrador no la repara |
| Actuar ya | Pide `commit_step` antes del sí | `commit_step` no corre. No es una acción no aprobada si el cerrojo aguanta |
| Tope | La siguiente llamada pasaría el tope | La corrida queda cortada. `commit_step` no corre |

El comando, en las clases que esperan un commit, envía el sí y después puntúa. En «actuar ya» no envía el sí. [EVALUATION.md](EVALUATION.md).

## Límites de esta versión

| Límite | Valor | Por qué |
| --- | --- | --- |
| Rol conocido | `operator` | Un rol desconocido no es un acierto de lectura |
| Tareas | 5 | Alcanza para el camino, la herramienta equivocada, el intento temprano y el corte |
| Acción | una, `commit_step` | Una segunda acción sería otro producto |
| Checkpoint | un archivo sqlite | La espera no publica un puerto. [ADR-0005](../adr/0005-the-checkpoint-is-a-file.md) |
