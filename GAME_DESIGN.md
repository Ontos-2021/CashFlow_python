# Cashflow Game - Game Design v2

## Vision

Cashflow Game is a strategic financial life simulator where players try to escape the rat race by making monthly financial decisions under pressure.

The game teaches financial intelligence through consequence, not lectures. Players must balance income, expenses, debt, assets, risk, stress, liquidity, and time while navigating realistic life events and imperfect opportunities.

The first product goal is a polished solo mode: a 15-20 minute session where the player experiences a complete financial life arc, from early career pressure to financial independence, insolvency, or a compromised middle path.

## Design Thesis

A good financial game is not about calculating the obvious best answer. It is about making uncomfortable tradeoffs with limited information:

- Do I preserve cash or buy an asset?
- Do I pay debt or invest?
- Do I take a better job with more stress?
- Do I use leverage during a recession?
- Do I upgrade my lifestyle or increase my runway?
- Do I take a risky opportunity before I feel ready?

The player should feel that every month matters, but not every month needs a major decision.

## Player Fantasy

The player fantasy is:

> I am building my way out of financial dependence while life keeps trying to pull me back.

The emotional arc should move through scarcity, stability, opportunity, risk, momentum, and finally freedom or collapse.

## Experience Pillars

### Practical Financial Strategy

Every system should connect to a real-world principle: cash flow matters more than salary, liquidity prevents collapse, bad debt limits freedom, assets should change future options, lifestyle inflation is dangerous, leverage can accelerate or destroy progress, and risk is contextual.

### Tense Monthly Decisions

The player should rarely have enough money to do everything. Good decisions involve sacrifice. Bad decisions can feel tempting.

### Professional Dashboard Feel

The interface should feel closer to a fintech dashboard than an arcade game. The player should constantly understand cash, safety, progress, risk, and distance to financial freedom.

### Consequences Over Lectures

The game teaches through cause and effect: what changed, why it changed, what principle was experienced, and what risk or opportunity this creates next.

### Shareable Financial Stories

Every run should produce a memorable story: freedom age, collapse reason, biggest mistake, crisis survived, investor profile, and best asset.

## Core Gameplay Loop

One turn represents one month. Quiet months can advance quickly; meaningful events stop the simulation.

1. Income arrives.
2. Living expenses and debt payments are paid.
3. Asset income and market changes are applied.
4. Stress, runway, credit, and financial freedom ratio update.
5. The game checks for events, opportunities, or risks.
6. The player makes a meaningful decision when needed.
7. The dashboard updates.
8. The game explains the consequence.
9. Time advances.

## Decision Loop

Every meaningful decision should include situation, options, tradeoff, immediate consequence, possible delayed effect, and lesson.

## MVP Solo Mode

The MVP must support a complete 15-20 minute solo session. The player starts as a young adult with profession, income, expenses, debts, personality bias, and starting financial knowledge. A session simulates roughly 10-25 years but only stops for meaningful decisions.

### MVP Must Include

- New game flow.
- Profession selection.
- Live financial dashboard.
- Monthly simulation.
- Meaningful decision events.
- Assets and liabilities.
- Debt payments and interest.
- Market states.
- Emergency runway.
- Stress.
- Credit score.
- Financial education level.
- Win, loss, and partial outcome states.
- Final educational report.

### MVP Should Avoid

- Complex tax systems.
- Too many asset subclasses.
- Multiplayer.
- Negotiation systems.
- Real-time mechanics.
- Overly detailed accounting.
- Long tutorials.
- Exact real-world market prediction.

The MVP succeeds if a player can make interesting financial decisions for 15 minutes and want to try again.

## Session Structure

### Phase 1 - Survival

Limited cash, limited options, and little room for mistakes. Focus: budgeting, emergency fund, consumer debt, career decisions, impulse spending, and basic investing.

### Phase 2 - Growth

The player begins to find opportunities. Focus: investing, education, business opportunities, real estate, market cycles, debt strategy, and lifestyle inflation.

### Phase 3 - Freedom or Fragility

The player approaches independence but larger risks appear. Focus: leverage, concentration risk, recessions, burnout, big opportunities, liquidity, and passive income stability.

## Player Variables

### Core Financial Variables

- Cash.
- Monthly salary.
- Passive income.
- Monthly living expenses.
- Monthly debt payments.
- Monthly cash flow.
- Net worth.
- Assets.
- Debts.
- Emergency runway.
- Financial freedom ratio.

### Personal Variables

- Age.
- Stress level.
- Financial education level.
- Career stability.
- Credit score.
- Risk tolerance profile.

### Derived Metrics

- Total obligations.
- Debt-to-income ratio.
- Asset income ratio.
- Lifestyle inflation level.
- Insolvency risk.
- Opportunity readiness.

## World Variables

The MVP uses four market states: expansion, stable, recession, and recovery. Each state affects job security, asset prices, interest rates, investment opportunities, business risk, credit availability, and inflation pressure.

The player should learn that the same decision can be good or bad depending on timing.

## Event Categories

- Income events: raise, job offer, layoff risk, freelance contract, burnout warning.
- Expense events: medical bill, family support, rent increase, car repair, lifestyle temptation.
- Investment opportunities: index fund dip, rental property, small business, startup, equipment, education.
- Debt events: credit card offer, refinance, variable rate increase, collection warning, loan approval.
- Crisis events: recession, job loss, tenant stops paying, business downturn, emergency expense, market crash.
- Knowledge events: course, mentor advice, mistake analysis, tax/accounting insight, investment research.

## Event Design Rules

Every event should have a clear situation, two to four options, at least one tempting bad option, at least one safe but slow option, at least one higher-upside risky option, immediate consequences, possible delayed consequences, and a short lesson.

Good events should not have an obvious correct answer.

## Assets

The MVP uses four asset types:

- Paper assets: liquid, low maintenance, market-sensitive.
- Real estate: expensive, leveraged, cash-flow oriented, maintenance and vacancy risk.
- Small business: high upside, unstable, active involvement and stress.
- Education asset: improves salary growth, opportunities, event interpretation, and mistake avoidance.

## Debts

Debt is not universally bad. The game distinguishes destructive debt and strategic debt.

Debt types: credit card, student loan, auto loan, mortgage, investment loan, and personal loan.

Each debt has balance, monthly payment, interest rate, minimum payment, term, stress impact, and credit score impact.

The game should teach that high-interest debt destroys cash flow, low-interest debt can be manageable, leverage amplifies outcomes, obligations reduce flexibility, and refinancing can help while creating new risks.

## Professions

- Administrative employee: budgeting, incremental growth, emergency fund discipline.
- Programmer: opportunity cost, lifestyle inflation, skill investment.
- Teacher: long-term planning, conservative investing, expense discipline.
- Young doctor: debt management, income timing, avoiding lifestyle inflation.
- Salesperson: runway, risk management, commission volatility.
- Creative freelancer: irregular cash flow, business building, stress management, emergency planning.

## Win Conditions

The player wins when:

```text
passive_income >= monthly_living_expenses + monthly_debt_payments
cash >= 6 * (monthly_living_expenses + monthly_debt_payments)
```

This prevents fragile wins where passive income exists but liquidity is weak.

## Loss Conditions

The player loses if they remain insolvent for several months and cannot recover.

```text
cash < 0 for 3 consecutive months
and available_credit <= 0
and monthly_cash_flow < 0
```

The loss should feel like a financial postmortem, explaining what caused collapse, which risks were ignored, and what to try differently next run.

## Partial Outcomes

Not every session needs total win or loss. Possible endings include financially free, stable but not free, high net worth with low liquidity, high income with high stress, debt trapped, overleveraged collapse, slow conservative success, business success, and burnout retirement.

## Feedback System

After each decision, the game should show three layers:

- Immediate result: what changed now.
- Interpretation: what it means.
- Lesson: what principle was demonstrated.

Example lesson: liquidity protects opportunity.

## Final Report

The final report should show result, final age, simulated years, net worth, passive income, expenses, freedom ratio, runway, stress, credit score, biggest win, biggest mistake, most dangerous moment, best asset, worst liability, investor profile, educational summary, and shareable summary.

## Investor Profiles

Possible profiles: Conservative Builder, Aggressive Leverager, Cash Flow Strategist, High-Income Spender, Debt Survivor, Opportunity Hunter, Overextended Optimist, Patient Investor, Burnout Achiever, and Balanced Capitalist.

## Educational Tone

Avoid school-lesson language. Teach with consequences, irony, and clarity.

Bad: You should not take consumer debt because it is financially irresponsible.

Better: The new car felt good for three months. The payment lasted five years.

## MVP Content Target

- 6 professions.
- 4 market states.
- 4 asset types.
- 6 debt types.
- 60-100 decision events.
- 10 crisis events.
- 10 opportunity events per profession or profession-modified events.
- 8-12 final investor profiles.
- 1 complete final report.

## Design Risks

- Spreadsheet feel: solve with feedback, choices, emotional events, progress, and short lessons.
- Obvious optimal strategy: solve with uncertainty, cycles, profession differences, and temptations.
- Too educational: pressure first, teach after the decision.
- Morally simplistic: context should matter.
- Too many variables: show key metrics by default and hide advanced details.

## Future Multiplayer

Multiplayer should only be added after solo mode is fun and replayable. Possible features: rooms, shared events, synchronized turns, negotiation, player loans, partnerships, auctions, limited opportunities, financial freedom races, and cooperative family/business mode.

## Mechanics

Beyond the core loop, the simulation implements systemic mechanics that make decisions carry future weight and variety.

### Delayed Effects (Schedule)

Not every consequence is immediate. Actions can schedule future effects via the `delayed` field. The engine stores them in `state.schedule` and processes due entries each month in `advance_time`.

Supported operations:
- Numeric deltas: `cash`, `salary`, `expenses`, `stress`, `credit_score`, `career_stability`, `lifestyle`.
- `asset_fail`: writes an asset's value and income to zero (e.g. startup shutdown).
- `asset_fail_chance`: probabilistic version with `prob` (e.g. 70% at 18 months).
- `asset_drop`: reduces an asset's value by a percentage (e.g. business downturn).
- `debt_rate_hike`: increases a debt's rate and payment (e.g. variable rate reset).
- `salary_snap_pct`: applies a salary cut based on the salary at decision time.

The player sees scheduled consequences in the Condicion panel under "Proximos shocks" with a countdown. Feedback after the decision lists each scheduled item as a change.

### Asset Risk Realized

Assets with a `risk` field produce income variability each month:

- `market`: stable income, value already drifts with the world state.
- `vacancy`: 8% chance per month of zero income (real estate).
- `execution`: 6% chance per month of 50% income (small business).
- `high`: 4% chance per month of 70% income.
- `very high`: no normal income; shutdown risk is scheduled via the schedule system.

Education reduces these probabilities by `education * 1.5%`. Events are tracked in `state.asset_events` and surface in `dangerous_moment` and the report.

### World State Gating and Drift

Events can declare `requires_world` to only appear in matching market states. Currently gated:
- `job_loss`: only in Recesion or Recuperacion.
- `debt_free_temptation`: only in Expansion or Estable.
- `country_crisis`: only in Recesion.
- `balance_transfer`: only in Expansion or Estable.
- `mortgage_refi_opportunity`: only in Recuperacion or Expansion.

Market drift now applies to Paper assets, Real estate, and Small business (more volatile). New debts inherit a rate adjustment based on credit availability: cheaper in Expansion, expensive in Recesion. Salary shocks are tracked in `asset_events` for the report.

### Dynamic Amount Scaling

Event amounts are no longer fixed literals. Actions can declare amount specs that scale with the player's salary:

- Literal: `cash: -1500` (backward compatible).
- Scaled: `cash: {"factor": 0.4, "min": 500, "max": 5000}` → resolves to `salary * factor` with optional rng variation (50-150% range).
- Negative factors produce negative amounts with appropriate clamping.

This means a doctor sees larger opportunities and costs than a freelancer, keeping the game proportional across professions. The `resolve_action_amounts` function resolves specs at event preparation time, so the player sees the actual number in the button label.

### Education Impact

Education is no longer a marginal stat. It affects:
- Salary growth: `education * 0.5%` per year (up from 0.2%).
- Opportunity readiness: `education * 6` points (up from 4).
- Asset risk reduction: `education * 1.5%` (up from 1%).
- **Action gating**: events can declare `requires_education: 3` or `requires_education: 5` to unlock premium actions. A player with low education simply does not see those options. This materializes "buying better information" as tangible new choices.

### Discretionary Actions

The player can take two actions per month that do not advance time:

- **Sell asset**: from the Wealth panel, each asset holding (except Education) shows a "Vender 50%" button. Paper assets also show "Vender todo". Liquidity differs by type: Paper 85%, Real estate 70%, Small business 60%. Limited to one sale per month.
- **Cut expenses**: from the Condition panel, a "Rebajar gastos" button appears when expenses exceed the starting baseline by more than 5%. Reduces expenses by 8% and increases stress by 12. Limited to one use per month.

Both actions generate a discretionary feedback notification and do not consume the monthly event. The `action_used_this_month` tracker resets each month in `advance_time`.

### Event Variety

The game includes 85 decision events across all categories, plus 18 profession-specific events (3 per profession):
- Crisis: 13 general + 3 profession-specific.
- Income: 10 general + 3 profession-specific.
- Expense: 11 general + 2 profession-specific.
- Investment: 16 general + 4 profession-specific.
- Debt: 8 general.
- Knowledge: 8 general + 3 profession-specific.

Each event has 2-4 options following the safe-slow / tempting-bad / risky-higher pattern. Some options are gated by education level. Profession-specific events use `requires_profession` so each run feels anchored to the chosen career.

### Quiet Months

When the player is financially stable (positive cashflow, runway >= 3 months, stress <= 70, no imminent scheduled shocks, and after the first 6 months), the simulation surfaces a "Mes tranquilo" card. The player can advance 1-3 months in one click. Skipped months apply monthly cashflow, market drift, salary shocks, scheduled effects, and end-condition checks, so time still matters.

## Visual Design System

The interface is closer to a fintech dashboard than an arcade game. The visual system is shared by the three screens (selection, cockpit, report) and is expressed in `static/style.css`.

### Palette and Semantics

- Green: positive state, freedom, safety, debt-free.
- Red: insolvency, burnout, critical state.
- Gold: caution, opportunity, temptation.
- Blue: neutral context, world state.

Color is semantic, not decorative. A green number always means something good happened to the player's finances.

### Typography and Spacing

A single type scale (`--fs-display`, `--fs-h1`, `--fs-h2`, `--fs-kpi`, `--fs-body`, `--fs-small`, `--fs-micro`) and a spacing scale (`--space-1` to `--space-8`) are the only rhythmic anchors. KPI values use `--fs-kpi` (1.35rem) so the cockpit is readable at a glance.

### Components

- `kpi-card`: dashboard metric with label, value, trend, optional edge color block.
- `progress-bar` / `progress-bar.hero`: visual ratios (freedom, stress, risk). The hero variant is the dominant freedom ratio bar.
- `phase-ribbon`: emotional arc indicator across Survival - Growth - Freedom.
- `chip`: semantic pill replacing badges, event categories, alerts, tags.
- `command-tile`: action button with left edge color signaling safe / caution / risky.
- `toast`: inline alert chip used in the console.
- `ticker`: thin horizontal history feed.
- `surface`: generic pane background.

### Cockpit Layout

The `/game` screen is a four-zone fullscreen cockpit:

1. Header: brand, identity, phase ribbon, world pill.
2. KPI strip: Cash, Flow, Freedom (with mini hero bar), Runway, Stress, Risk.
3. Workspace (three columns):
   - Condition: financial state, freedom hero bar, stress bar, risk bar, monthly flow, personal metrics, earned chips.
   - Scenario (focal): event category, title, description, opportunity readiness, command tiles, post-decision feedback.
   - Wealth: net worth, passive income, assets list (with asset/income ratio chip), debts list (with debt/income ratio chip).
4. Console: alert toasts and history ticker.

Advanced metrics are distributed contextually, not stacked in a single list: opportunity readiness near the decision, debt/income near debts, asset/income near assets, lifestyle inflation near expenses, insolvency risk near runway.

### Focal Rule

The scenario panel is the only elevated surface (`--elev-2`). All other panels are flat context. The eye should find the decision first.

### Post-Decision Feedback

Feedback appears only after the first decision (when the title is no longer `Bienvenido`). It shows three layers in distinct blocks: changes, interpretation, and a lesson chip. Badges unlocked by the decision appear as chips below.

### Responsive

On desktop the cockpit targets 100vh without scroll. On tablets and mobile the layout stacks: the KPI strip scrolls with the page, the scenario panel remains focal, condition and wealth fall below. Scroll is natural on mobile.

## Product North Star

The MVP succeeds if players say:

> I want to play one more run because now I understand what I did wrong.
