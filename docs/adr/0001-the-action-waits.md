# ADR-0001: La acción espera y la lectura no

Estado: Accepted
Fecha: 2026-11-07

## Context

El borrador tiene que poder citar un manual o un número antes de que una persona decida. Si toda herramienta esperara, la persona aprobaría un texto vacío. Si la acción corriera junto con la lectura, el paso ya estaría hecho.

## Decision

`search_manuals` y `query_warehouse` pueden correr antes de la aprobación. `commit_step` corre solo después de un sí en el mismo hilo. Un hilo nuevo no hereda ese sí. Un intento de ejecutar sin sí no llama a `commit_step`.

## Alternatives

**Parar antes de cualquier herramienta.** Descartado: la aprobación no tendría qué mirar.

**Ejecutar y compensar.** Descartado: la acción ya habría ocurrido.

## Consequences

Una lectura no es una acción no aprobada. El contador mira `commit_step`, no la petición del modelo de saltarse el cerrojo.
