# Cashflow Game - Game Design

## Vision

Cashflow Game is a professional, gamified financial simulator for young adults and adults who want to train financial intelligence through play. The first product goal is a strong solo mode that teaches real-world concepts through monthly decisions, financial statements, market events, debt, assets, cash flow, and long-term consequences.

## Experience Pillars

- Realistic financial decisions with simplified early rules.
- A professional dashboard feel, closer to fintech than arcade.
- Every decision should teach a practical financial principle.
- The player should feel tension between liquidity, growth, debt, risk, and time.
- The game should generate shareable stories: age of financial freedom, best decision, worst decision, crises survived, and investor profile.

## Core Loop

One turn represents one month.

1. The player receives salary and passive income.
2. The player pays living expenses and debt payments.
3. A financial event or opportunity appears.
4. The player chooses an action.
5. The financial statement updates.
6. The game explains the consequence and lesson.
7. The month advances.

## Solo Mode MVP

The solo prototype must support a complete 15-20 minute session.

- Start a new game with a profession.
- Display a live financial dashboard.
- Advance monthly turns.
- Present one decision per month.
- Support opportunities, market events, expenses, debt decisions, education, and career events.
- Track assets, debts, cash flow, net worth, emergency runway, and financial freedom ratio.
- End when passive income covers expenses and the player has at least 6 months of emergency runway.
- End as a loss if the player remains insolvent for several months.
- Show a final educational report.

## Player Variables

- Cash.
- Monthly salary.
- Passive income.
- Monthly living expenses.
- Monthly debt payments.
- Assets.
- Debts.
- Net worth.
- Monthly cash flow.
- Age.
- Current month.
- Financial freedom ratio.
- Emergency runway.
- Financial education level.
- Stress level.
- Credit score.

## World Variables

- Market cycle.
- Inflation.
- Interest rate environment.
- Unemployment risk.

The MVP uses simplified world states: expansion, stable, recession, and recovery.

## Event Categories

- Investment opportunity.
- Market movement.
- Life expense.
- Doodad or impulse spending.
- Education.
- Career change.
- Debt and credit.
- Crisis.

## Assets

MVP asset types:

- Real estate.
- Paper assets.
- Small business.
- Education asset.

Each asset can affect cash, passive income, net worth, stress, and financial education.

## Debts

MVP debt types:

- Credit card.
- Student loan.
- Auto loan.
- Mortgage or investment loan.
- Personal loan.

Each debt has balance, monthly payment, and interest rate.

## Professions

Initial professions:

- Administrative employee.
- Programmer.
- Teacher.
- Young doctor.
- Salesperson.
- Creative freelancer.

Each profession teaches a different tradeoff between income, expenses, stability, debt, and growth.

## Win Condition

The player wins when:

```text
passive_income >= monthly_expenses + monthly_debt_payments
cash >= 6 * (monthly_expenses + monthly_debt_payments)
```

This prevents fragile wins where the player has passive income but no liquidity.

## Final Report

The end screen should show:

- Result.
- Age and simulated years.
- Net worth.
- Passive income.
- Freedom ratio.
- Emergency runway.
- Best decision.
- Worst decision.
- Investor profile.
- Short educational summary.

## Future Multiplayer

After solo mode is solid, multiplayer can add:

- Game rooms.
- Shared market events.
- Turn synchronization.
- Negotiation.
- Player loans.
- Partnerships.
- Auctions.
- Shared limited opportunities.
