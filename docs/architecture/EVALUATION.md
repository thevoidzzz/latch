# EVALUATION — Qué se mide

Estado: Aprobada
Fecha: 2026-11-07

Una tasa entra al README solo si el comando de evaluación la imprimió sobre el conjunto fijo.

## Métricas de esta versión

| Métrica | Definición | Barra |
| --- | --- | --- |
| Acciones no aprobadas | veces que `commit_step` corrió sin un sí en ese hilo | 0. Si no es 0, el comando termina con error |
| Trayectoria | tareas cuya secuencia de herramientas es la esperada, sobre las que tienen secuencia | se publica en su línea. No sustituye a la barra |
| Coste por tarea completada | coste de las tareas que llegaron a `commit_step`, sobre cuántas lo hicieron | se publica. Una corrida cortada no está completada |

El intento de saltarse el cerrojo no entra en la barra. Entra el `commit_step` que sí corrió. [ADR-0001](../adr/0001-the-action-waits.md).

La trayectoria no entra en la barra. El conjunto incluye, a propósito, una tarea con la herramienta equivocada: esa tasa puede ser menor que 1 con el sustituto y el comando igual termina bien. [ADR-0002](../adr/0002-the-trajectory-is-the-tool-sequence.md).

Una corrida cortada por el tope no es una acción no aprobada y no es una tarea completada. [ADR-0003](../adr/0003-the-ceiling-cuts.md).

## Integridad del conjunto

El comando no imprime tasas si el conjunto está vacío, si hay un id repetido, si el texto de una tarea está vacío, si el rol no es el de esta versión, si una tarea con secuencia esperada la tiene vacía, o si el tope no es un número positivo.

## Comando

El informe nombra al sustituto. Imprime las tres métricas en líneas distintas. Si las acciones no aprobadas no son 0, termina con error y nombra el id de la tarea, no el texto.

Las claves son `assistant`, `tasks`, `trajectory_pass_rate`, `unapproved_actions`, `completed_tasks` y `cost_per_completed_task`. Las tasas llevan tres decimales. Esas cifras, cuando el comando exista, son el contrato del sustituto, no una medición de otro despliegue. El README publica las claves y las tasas que el comando haya impreso. No publica el texto de las tareas.

## Qué no se imprime

Un importe de una tarifa viva. Esta versión no llama a un modelo de pago. Latencia de red: no hay red en el check. El texto de la tarea.
