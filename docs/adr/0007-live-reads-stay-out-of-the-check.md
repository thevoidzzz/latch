# ADR-0007: Las lecturas vivas no entran al check

Estado: Accepted
Fecha: 2026-11-09

## Context

Una corrida puede querer leer un manual y un warehouse que viven en otros procesos. El check tiene que seguir fallando sin red y sin clave. Un fallo de esos procesos no puede cambiar la trayectoria ni el contador de acciones.

## Decision

`python -m latch` no lee `LATCH_MANUALS_URL` ni `LATCH_WAREHOUSE_URL`. El proceso de la API sí. Cada URL recibe `POST /v1/answers`. Del manual se usa el primer `excerpt`. Del warehouse se usa `value` cuando es un texto. Un rechazo es un hit vacío. Un proceso que no contesta, o un valor que no es texto, es un error: HTTP 503, no un hit vacío. No se envía una clave. El MCP sigue con los dobles. El checkpoint sigue siendo un archivo.

## Alternatives

**Hacer que el check use las URL cuando existan.** Descartado: la tasa dejaría de ser repetible.

**Tratar un proceso caído como “no hay pasaje”.** Descartado: un fallo de red parecería una respuesta vacía.

## Consequences

La corrida viva no se pega en el README hasta que un comando la imprima. El check sigue en los dobles. Una base publicada y un sink con host siguen fuera de esta versión.
