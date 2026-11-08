# ADR-0002: La trayectoria es la secuencia de herramientas

Estado: Accepted
Fecha: 2026-11-07

## Context

Un texto final presentable puede esconder que se llamó a la herramienta equivocada.

## Decision

Una trayectoria pasa cuando la secuencia de nombres de herramienta es la esperada para esa tarea. El texto final no la repara. La tasa de trayectoria no sustituye al conteo de acciones no aprobadas.

## Alternatives

**Puntuar solo la frase.** Descartado: el producto dejaría de ver el camino.

**Un solo accuracy que mezcle frase y camino.** Descartado: un camino mal hecho podría quedar tapado por una frase correcta.

## Consequences

El informe imprime la trayectoria en su propia línea. Un caso que elige la herramienta equivocada no pasa la trayectoria aunque el borrador se lea bien. Esa línea no decide la salida del comando. La salida la decide la acción no aprobada. [ADR-0001](0001-the-action-waits.md).
