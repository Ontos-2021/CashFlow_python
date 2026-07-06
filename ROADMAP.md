# Cashflow Game - Roadmap

## Current Focus

Build a polished solo mode before multiplayer. The first playable experience should make players want one more run because they understand what they did wrong.

## Phase 0 - Cockpit Visual System

Status: implemented.

- Establish shared design tokens (palette, type scale, spacing, radii, elevation).
- Replace spreadsheet-style state list with focal three-column cockpit.
- Add phase ribbon (Survival - Growth - Freedom) and freedom hero bar.
- Distribute advanced metrics contextually next to what they explain.
- Redesign action buttons as command tiles with semantic edge color.
- Add post-decision feedback block (changes, interpretation, lesson chip).
- Add alert toasts and history ticker in the console.
- Reflight index and report screens on the same design system.
- Maintain 100vh no-scroll desktop target with mobile-responsive fallback.

## Phase 1 - Align Current MVP

Status: implemented in prototype form.

- Update design documentation to v2.
- Keep solo mode as the only active mode.
- Add partial outcomes beyond binary win/loss.
- Improve the final report with postmortem and shareable summary.
- Add derived metrics: debt-to-income, asset income ratio, lifestyle inflation, insolvency risk, and opportunity readiness.
- Convert decision feedback into immediate result, interpretation, and lesson.

## Phase 2 - Deepen Events

Status: implemented.

- 67 decision events across all categories (target was 60-100).
- Profession-specific events: 18 events (3 per profession) tagged with `requires_profession` and blended into the event pool.
- Each event includes safe, tempting, and risky options.
- Crisis, income, expense, debt, investment, and knowledge events covered.
- Dynamic amount scaling: events scale costs/rewards by player salary with rng variation.
- Education gating: premium actions unlock at education >= 3 and >= 5.
- Discretionary actions: sell assets and cut expenses from the UI without advancing time.

## Phase 3 - Improve Monthly Simulation

Status: implemented.

- Add market state effects to event consequences.
- Track delayed effects and future risks: implemented as the `schedule` system with countdown in the Condicion panel.
- Asset risk realized per month: vacancy, execution, high, very high; education reduces probability.
- World state gating: `requires_world` on events (job_loss, debt_free_temptation); small business drift; debt rate adjusts by credit availability.
- Quiet-month fast-forward: stable months show a "Mes tranquilo" card that advances 1-3 months while applying monthly cashflow, drift, shocks, and schedule checks.
- Make world state affect job risk, asset prices, credit availability, and inflation more strongly.

## Phase 4 - Viral Replayability

Status: partially implemented.

- Add richer investor profiles.
- Add biggest win, biggest mistake, most dangerous moment, best asset, and worst liability.
- Add compact shareable summary.
- Improve postmortem language for loss and partial outcomes.
- Refactor: `game_engine.py` monolítico (~2400 líneas) dividido en paquete `game_engine/` con 8 módulos de responsabilidad única (constants, events, metrics, actions, simulation, ui, report, __init__). Sin imports circulares. `final_report()` movido de `enrich_state` a la ruta `/report` para romper el ciclo ui<->report.

## Phase 5 - Future Multiplayer

Status: intentionally deferred.

- Rooms.
- Shared market events.
- Turn synchronization.
- Negotiation.
- Player loans.
- Partnerships.
- Auctions.
- Competitive and cooperative modes.
