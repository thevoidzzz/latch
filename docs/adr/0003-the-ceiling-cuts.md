# ADR-0003: El tope corta

Estado: Accepted
Fecha: 2026-11-07

## Context

Una corrida puede seguir llamando al modelo después de haber gastado el coste que se le dio.

## Decision

Si la siguiente llamada pasaría el tope, la corrida se detiene, queda cortada y `commit_step` no corre. El coste acumulado se informa igual. Un aviso que deja seguir no es esta versión.

## Alternatives

**Registrar el exceso y seguir.** Descartado: el tope no cortaría nada.

**Negarse a empezar.** Descartado: una corrida corta tiene que poder terminar.

## Consequences

El corte no es una acción no aprobada. Es otra salida. El check usa costes del sustituto, no una tarifa viva.
