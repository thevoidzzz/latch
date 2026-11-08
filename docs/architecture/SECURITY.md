# SECURITY — Qué está cerrado

Estado: Aprobada
Fecha: 2026-11-07

Latch no describe cómo saltarse el cerrojo. Este documento fija qué garantiza el comando y qué hueco queda abierto a propósito.

## Cerrado en esta versión

- El check no llama a un modelo, no usa una clave y no abre la red. [ADR-0004](../adr/0004-the-check-uses-the-stand-in.md).
- `commit_step` no corre sin un sí en ese hilo. Un intento bloqueado no cuenta como acción no aprobada. [ADR-0001](../adr/0001-the-action-waits.md).
- Si la siguiente llamada pasaría el tope, la corrida se corta y la acción no corre. [ADR-0003](../adr/0003-the-ceiling-cuts.md).
- El informe de una corrida verde no imprime el texto de la tarea. Un fallo nombra el id.
- La traza lleva el id, las latencias y los tokens. No lleva una clave.
- El checkpoint no se publica como puerto. [ADR-0005](../adr/0005-the-checkpoint-is-a-file.md).
- Las tareas no tienen datos de personas.

## Hueco que se admite

Quien llama a la aprobación es, para esta versión, quien aprueba. Latch no autentica a una persona ni demuestra quién llamó. El rol de la corrida es el rol que se entregó al abrirla.

El archivo sqlite guarda el borrador. Quien puede leer el archivo puede leer la espera.

Una corrida verde nombra al sustituto. No es un resultado sobre otro despliegue.

## Lo que el archivo de tareas contiene

El texto de las tareas y los valores fijos del doble están en el repositorio cuando el comando exista. Hace falta para que el test falle. El README publica las tasas, no ese texto. Este repositorio no promete que el conjunto sea secreto.

No hay una clave que retirar. El sustituto no tiene un secreto.
