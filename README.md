# Cashflow Game

Cashflow Game is a strategic financial life simulator where players try to escape the rat race by making monthly financial decisions under pressure. It is realistic in its financial model, professional in its interface, and gamified through consequences, progression, investor profiles, and shareable run stories.

The current implementation is a Flask solo-mode prototype focused on 15-20 minute sessions. Players balance income, expenses, debt, assets, risk, stress, liquidity, and time while navigating realistic life events and imperfect opportunities.

See `GAME_DESIGN.md` for the current v2 product direction and `ROADMAP.md` for the implementation plan.

## Descripción General

El **Cashflow Game** es una simulación educativa basada en el popular juego de mesa creado por Robert Kiyosaki. El objetivo del juego es enseñar conceptos de finanzas personales, inversiones y gestión del dinero de una manera divertida e interactiva. Los jugadores deben manejar sus finanzas, adquirir activos y reducir pasivos para salir de la "Carrera de la Rata" y alcanzar la "Pista Rápida", donde pueden buscar la independencia financiera.

## Objetivo del Juego

El objetivo principal es salir de la "Carrera de la Rata" alcanzando un ingreso pasivo que supere los gastos mensuales y luego llegar a la "Pista Rápida" para cumplir tus sueños financieros.

## Mecánicas del Juego

### Factores Temporales

- **Edades Iniciales**: Cada jugador comienza a una edad específica (por ejemplo, 25 años).
- **Progreso del Tiempo**: Con cada turno, el tiempo avanza un período determinado (por ejemplo, una semana o un mes).
- **Efecto del Tiempo**:
  - **Eventos de Vida**: A ciertas edades, los jugadores pueden enfrentar eventos importantes como matrimonio, hijos, jubilación, etc.
  - **Envejecimiento**: Con el tiempo, pueden surgir factores de salud que afecten los gastos y las decisiones financieras.

### Factores Económicos

- **Inflación**: Definir una tasa de inflación que afecte los costos de vida y precios de activos.
- **Ajustes Periódicos**: Cada cierto número de turnos (por ejemplo, cada año en el juego), ajustar los costos y salarios según la inflación.

### Tipos de Activos

1. **Acciones**: Representan inversiones en empresas y pueden generar dividendos.
2. **Propiedades Inmobiliarias**: Generan ingresos por alquiler.
3. **Negocios**: Pueden generar ingresos activos o pasivos.
4. **Bonos**: Generan ingresos por intereses.
5. **Ahorros**: Generan intereses en cuentas bancarias.

### Adquisición de Activos

- **Cartas de Oportunidad**: Cuando un jugador saca una carta de oportunidad, puede optar por invertir en el activo descrito en la carta.
  - La carta detalla el costo de adquisición y el retorno esperado (dividendos, alquiler, intereses, etc.).
  - Si el jugador decide invertir, se resta el costo del efectivo del jugador y se añade el activo a su hoja de juego.

### Generación de Ingresos

- **Dividendos de Acciones**: Cada cierto número de turnos (por ejemplo, cada mes en el juego), las acciones pueden generar dividendos.
  - Los dividendos se suman al efectivo del jugador.
  - El valor de las acciones puede fluctuar con eventos de mercado.

### Eventos Relacionados con Activos

1. **Mercado de Valores**:
   - Cartas de Mercado pueden afectar el valor de las acciones, subiendo o bajando su precio.
   - El jugador puede decidir vender las acciones para obtener ganancias o evitar pérdidas.
2. **Mantenimiento de Propiedades**:
   - Las propiedades pueden requerir mantenimiento, lo que se refleja en cartas de Doodads o Emergencias.
   - El jugador debe pagar los costos de mantenimiento para seguir recibiendo ingresos por alquiler.
3. **Crisis Económicas**:
   - Eventos aleatorios pueden simular crisis económicas que afecten negativamente el valor de los activos.
   - El jugador debe adaptarse a estas situaciones, ajustando su estrategia de inversión.

### Interacción Social

- **Negociación y Comercio**: Permitir a los jugadores negociar y comerciar activos y pasivos entre sí.
- **Competencia y Cooperación**: Incluir desafíos cooperativos o competitivos para mantener el interés.

### Progresión y Metas

- **Logros y Recompensas**: Implementar un sistema de logros y recompensas para hitos alcanzados (por ejemplo, primer millón, diversificación de inversiones).
- **Metas Personales**: Permitir a los jugadores establecer metas personales que les proporcionen bonificaciones cuando se alcanzan.

### Diversificación de Inversiones

- **Variedad de Activos**: Ofrecer múltiples tipos de inversiones con diferentes riesgos y retornos.
- **Eventos Aleatorios**: Incluir eventos aleatorios que puedan beneficiar o perjudicar a los jugadores (por ejemplo, lotería, crisis económicas).

### Factores de Realismo

- **Impuestos y Deducciones**: Incluir el cálculo de impuestos y posibles deducciones fiscales.
- **Crisis y Recuperaciones**: Simular crisis económicas y períodos de recuperación para agregar un nivel de desafío adicional.

## Lógica del Juego

### Inicialización del Juego

```plaintext
function inicializar_juego():
    crear_jugadores()
    distribuir_ocupaciones()
    barajar_cartas()
    posicionar_jugadores()
```

## Turno del jugador

```function jugar_turno(jugador):
    lanzar_dados(jugador)
    mover_ficha(jugador)
    realizar_accion(jugador)
    avanzar_tiempo(jugador)
```

## Manejo de cartas

```
function sacar_carta_oportunidad(jugador):
    carta = cartas_oportunidad.pop()
    mostrar_carta_al_jugador(jugador, carta)
    decision = obtener_decision_jugador(jugador)
    if decision == 'invertir':
        ejecutar_efecto_carta(jugador, carta)
```

## Ajustes por inflación

```
function ajustar_por_inflacion():
    for jugador in jugadores:
        jugador.salario *= (1 + tasa_inflacion)
        jugador.gastos *= (1 + tasa_inflacion)
        ajustar_valor_activos(jugador)

```

## Eventos de Mercado

```
function manejar_evento_mercado(jugador):
    carta = cartas_mercado.pop()
    ajustar_valor_activos(jugador, carta)
    decision = obtener_decision_vender(jugador, carta)
    if decision == 'vender':
        vender_activo(jugador, carta)
```

## Contribución
¡Nos encantaría contar con tu colaboración! Si deseas contribuir a este proyecto, por favor sigue estos pasos:

## Haz un fork del repositorio.
Crea una rama para tu feature 

```git checkout -b feature-nueva-funcionalidad```.

Realiza un commit con tus cambios 

```(git commit -am 'Añadir nueva funcionalidad').```

Haz push a la rama 

```(git push origin feature-nueva-funcionalidad).```

Abre un Pull Request.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo LICENSE.md para más detalles.

## Agradecimientos
Agradecemos a todos los contribuidores y a la comunidad por su apoyo en el desarrollo de este proyecto.

## Créditos

Este proyecto fue desarrollado por:

* **José Mercado**: Idea original, diseño del juego y desarrollo.
* **[José Mercado]**: Desarrollador principal.
* **Robert Kiyosaki**: Inspiración y creación del juego original Cashflow.
* **Comunidad Open Source**: Herramientas y recursos utilizados en el desarrollo de este proyecto.
