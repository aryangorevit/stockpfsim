# Vityrathi project statement

## Problem statement

How do different trading decisions, portfolio allocations, and simulated
market conditions affect portfolio performance, risk, and overall returns?
Vityrathi answers this question with a small, transparent market model that
students can inspect, run repeatedly, and extend.

## Scope

The project includes fictional stocks, virtual cash, validated buy and sell
orders, transaction history, price simulation, portfolio metrics, scenario
comparison, terminal reports, JSON save/load, and CSV export. It is explicitly
an educational simulation. Live market feeds, brokerages, real-money
transactions, investment advice, machine learning, web frameworks, and
databases are outside the core scope.

## Target users

- Students learning Python and object-oriented programming
- Programming learners studying simulation and validation
- People learning basic portfolio and risk concepts
- Instructors demonstrating modular application design

## High-level features

1. Fictional market and stock management
2. Portfolio and position accounting
3. Buy/sell transaction processing
4. Repeatable stochastic market simulation
5. Return, drawdown, volatility, and scenario analysis
6. Interactive terminal menu and command-line demo mode
7. JSON persistence and CSV export
8. Automated behavioral tests

## Non-functional requirements

The interface should be readable and usable from a terminal. Normal input
mistakes should produce an explanation instead of terminating the program.
The modular design should remain maintainable, and simulations should avoid
unnecessary dependencies or network access.
