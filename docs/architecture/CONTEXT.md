# CONTEXT — Latch

Estado: Aprobada
Fecha: 2026-11-07

Latch redacta el paso siguiente y no lo ejecuta hasta que una persona aprueba esa misma corrida. Una lectura puede ocurrir antes. `commit_step` no. El vocabulario está en [GLOSSARY.md](../../GLOSSARY.md).

## Actores

| Actor | Qué hace |
| --- | --- |
| Quien aprueba | Envía el sí o el no sobre un hilo y lee el borrador |
| Quien publica | Corre el comando antes de aceptar un cambio y lee las tasas |
| Evaluación | Corre el conjunto fijo y lee el informe. No es quien aprueba una corrida real |

## Dentro de esta versión

Dos lecturas, `search_manuals` y `query_warehouse`. Una acción, `commit_step`. Un sustituto determinista. Un checkpoint en archivo. Una traza local. Un comando que imprime las tasas. Una entrada HTTP para abrir la corrida y para aprobarla. El diseño se escribe en español. [ADR-0006](../adr/0006-public-text-is-english.md).

## Fuera

Pantalla, una cuenta de nube, un modelo hospedado en el check, un sink en el check, una base publicada y un servicio vivo de lecturas en el check. Un cliente hacia otro despliegue queda para después: esa corrida se fecha y no es el check. [ADR-0004](../adr/0004-the-check-uses-the-stand-in.md).

## Sistemas externos

Ninguno en el check. El modelo y las lecturas son puertos. Esta versión los implementa el sustituto y los dobles, sin red y sin clave.
