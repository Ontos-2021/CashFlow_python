# Cashflow Game

Cashflow Game is a strategic financial life simulator where players try to escape the rat race by making monthly financial decisions under pressure. It is realistic in its financial model, professional in its interface, and gamified through consequences, progression, investor profiles, and shareable run stories.

The current implementation is a Flask solo-mode prototype focused on 15-20 minute sessions. Players balance income, expenses, debt, assets, risk, stress, liquidity, and time while navigating realistic life events and imperfect opportunities.

See `GAME_DESIGN.md` for the v2 product direction, `ROADMAP.md` for the implementation plan, and the `Visual Design System` section in `GAME_DESIGN.md` for the UI specification.

## Descripcion General

Simulador de vida financiera en modo solo. El jugador elige una profesion y recorre un arco de 10 a 25 anos en sesiones de 15 a 20 minutos. Cada turno es un mes: llega el ingreso, se pagan gastos y deudas, los activos generan rentas, el mercado se mueve y aparecen decisiones tensas. La meta es construir ingreso pasivo y reserva suficientes para alcanzar la libertad financiera sostenible.

No es una calculadora: es un tablero profesional gamificado donde cada decision tiene tradeoff, riesgo, consecuencia inmediata, interpretacion y principio. La derrota enseña a traves del postmortem, no de la culpa.

## Pantallas

- `/` Seleccion de profesion y descripcion del juego.
- `/game` Cockpit fullscreen: header con arco emocional, tira de KPIs, area de trabajo en tres columnas (Condicion / Escenario / Riqueza) y consola con alertas e historial.
- `/report` Reporte final con perfil de inversor, barra de libertad, metricas clave, decisiones clave y postmortem compartible.

## Modelo Financiero

- 6 profesiones con perfil financiero distinto.
- 4 estados del mundo: Expansion, Estable, Recesion, Recuperacion, con inflacion, drift de activos, riesgo laboral y credito.
- 4 tipos de activos: papel, inmobiliario, pequena empresa, education.
- 6 tipos de deudas con interes, pago, plazo, impacto en estres y credito.
- Metricas derivadas: deuda/ingreso, ingreso/activo, inflacion de estilo de vida, riesgo de insolvencia, preparacion para oportunidades, estado financiero.
- Condiciones de victoria y derrota, ademas de finales parciales (burnout, overleveraged collapse, high net worth low liquidity, etc.).

## Sistema Visual

Un sistema de design compartido en `cashflow_game/app/static/style.css` rige las tres pantallas:

- Paleta semantica: verde (positivo), rojo (insolvencia), oro (cautela), azul (neutro).
- Tipografia y espaciado con tokens unicos.
- Componentes reutilizables: `kpi-card`, `progress-bar`, `phase-ribbon`, `chip`, `command-tile`, `toast`, `ticker`, `surface`.
- Regla focal: el panel Escenario es la unica superficie elevada; demas paneles son contexto.

## Stack

- Python 3.
- Flask con sesiones (no requiere base de datos para el modo solo).
- Jinja2 para templates.
- CSS puro, sin frameworks ni JavaScript.

## Estructura

```
cashflow_game/
  app/
    __init__.py        # Fabrica de la app Flask.
    config.py          # Configuracion.
    routes.py          # Rutas: / /new-game /game /action /report /reset.
    game_engine/       # Motor dividido en 8 modulos de responsabilidad unica.
      __init__.py      # Re-exports: mantiene compatibilidad con imports existentes.
      constants.py     # 6 profesiones, 4 estados del mundo, liquidacion por tipo.
      events.py        # 67 eventos base + 18 de profesion + 15 menores (datos puros).
      metrics.py       # Calculos derivados, fase de sesion, edad mostrada, snapshots.
      actions.py       # Efectos de acciones, venta, corte de gastos, pagar deuda, normalize.
      simulation.py    # Loop de juego: new_game, apply_action, quiet months, finales.
      ui.py            # enrich_state, badges, alertas, feedback, perfil de inversor.
      report.py        # Postmortem: patrones, consejos, key_moments, benchmarks, final_report.
    templates/         # base, index, game, report.
    static/style.css   # Design system.
  run.py               # Punto de entrada.
tests/test_game_engine.py  # Pruebas del motor.
GAME_DESIGN.md         # Spec v2 (incluye el Sistema Visual).
ROADMAP.md             # Plan de implementacion.
```

## Como correrlo

```bash
pip install -r requirements.txt
python cashflow_game/run.py
```

Abrir `http://127.0.0.1:5000/` en el navegador.

## Pruebas

```bash
python -m pytest tests/ -q
```

## Contribucion

1. Haz un fork del repositorio.
2. Crea una rama para tu feature: `git checkout -b feature-nueva-funcionalidad`.
3. Realiza un commit con tus cambios.
4. Haz push a la rama.
5. Abre un Pull Request.

## Licencia

Este proyecto esta licenciado bajo la Licencia MIT - consulta el archivo LICENSE.md para mas detalles.

## Creditos

- Jose Mercado: idea original, diseño del juego y desarrollo.
- Inspiracion: el juego de mesa Cashflow de Robert Kiyosaki.
- Comunidad Open Source: herramientas y recursos utilizados.