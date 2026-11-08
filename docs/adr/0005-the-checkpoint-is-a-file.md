# ADR-0005: El checkpoint es un archivo

Estado: Accepted
Fecha: 2026-11-07

## Context

La espera tiene que seguir ahí cuando llega la aprobación. Un checkpoint solo en memoria muere con el proceso. Publicar una base abre otro servicio y otro puerto.

## Decision

El checkpoint es un archivo sqlite junto al proceso. No se publica como puerto. La aprobación reanuda el hilo de ese archivo. Esta versión no abre un puerto de base.

## Alternatives

**Solo memoria.** Descartado: la aprobación no podría llegar en otra llamada.

**Una base publicada.** Descartado: la espera no necesita un segundo servicio en esta versión.

## Consequences

Dos procesos con el mismo archivo ven el mismo hilo. Borrar el archivo pierde la espera. El check usa un archivo temporal.
