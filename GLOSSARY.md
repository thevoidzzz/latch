# Latch

Latch redacta el paso siguiente de una operación y no lo ejecuta hasta que una persona aprueba esa misma corrida.

## Language

**Corrida**:
Una tarea, desde la pregunta hasta el borrador en espera o hasta el corte por tope.
_Avoid_: Sesión, chat, conversación

**Hilo**:
La identidad de una corrida en el checkpoint. La aprobación vale solo para ese hilo.
_Avoid_: Usuario, sesión de navegador

**Lectura**:
`search_manuals` o `query_warehouse`. Puede ocurrir antes de la aprobación.
_Avoid_: Acción, efecto

**Borrador**:
El texto del paso siguiente, todavía sin ejecutar.
_Avoid_: Acción, orden enviada

**Acción**:
`commit_step`. Lo único que espera un sí.
_Avoid_: Lectura, borrador, llamada a una herramienta

**Aprobación**:
Un sí sobre el mismo hilo. Un hilo nuevo no la hereda.
_Avoid_: Confirmación del modelo, reintento

**Cerrojo**:
La parada entre el borrador y la acción.
_Avoid_: Timeout, pausa genérica

**Trayectoria**:
La secuencia de nombres de herramienta de una corrida.
_Avoid_: Texto final, respuesta

**Tope**:
El coste que corta la corrida antes de la siguiente llamada.
_Avoid_: Aviso, presupuesto blando

**Traza**:
El registro local de pasos, latencia, tokens y coste de una corrida.
_Avoid_: Log de acceso, factura

**Acción no aprobada**:
Un `commit_step` que corrió sin un sí en ese hilo.
_Avoid_: Intento bloqueado, borrador

**Sustituto**:
El modelo determinista contra el que corre el check.
_Avoid_: Modelo hospedado, otro servicio

**Rol**:
La audiencia que la lectura del manual puede ver.
_Avoid_: Identidad, usuario
