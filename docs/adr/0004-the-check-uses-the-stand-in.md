# ADR-0004: El check usa el sustituto

Estado: Accepted
Fecha: 2026-11-07

## Context

El check tiene que poder fallar sin red y sin clave. Si llamara a un modelo de pago o a un servicio vivo, fallaría por una factura o por un nombre que no es el de este producto.

## Decision

El modelo es un puerto. El check enchufa el sustituto de este repositorio. Es determinista, no abre la red y no lee una clave. La traza se queda en el proceso. Un sink se construye solo cuando hay un host configurado, y el check deja ese host vacío.

Una corrida contra un modelo hospedado o contra un servicio vivo se fecha, nombra a ese otro extremo y no sustituye al sustituto en el check. Esta versión no incluye ese cliente.

## Alternatives

**Llamar a un modelo hospedado en cada pull request.** Descartado: el check fallaría por una clave o por una factura.

**Exigir el sink en el check.** Descartado: el check dependería de un host y de una clave.

## Consequences

El job no instala un SDK de modelo y no lee una clave. Ningún archivo versionado contiene una credencial. Una traza verde del sustituto no es evidencia de otro despliegue. El README dice qué extremo produjo un número solo después de que el comando lo imprima.
