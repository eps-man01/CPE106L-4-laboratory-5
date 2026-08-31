# CPE106L-4: Laboratory Activity 5 - Relational Database Implementation and SQL Modeling

## Project Overview

This laboratory activity demonstrates the design and implementation of a Relational Database Model using SQL and Python's built-in `sqlite3` engine.
The application models a fictional railway operations management system (Yuan's Railway Ticketing & Scheduling System) where passenger profiles, train fleet routes, and booking manifests are managed through structured relational entities and multi-table queries.

## Relational Database Design

### 1. Entity Relationships & Schema Structure

* **`passengers`**: Stores commuter identity, unique contact numbers, and passenger classification (`Regular`, `Student`, `Senior`).
* **`trains`**: Manages train fleet details including operational routes (origin to destination), seating capacity, and standard fare rates.
* **`bookings`**: Junction table establishing a Many-to-Many relationship between passengers and train routes, capturing seat assignments and confirmed reservation statuses with cascading foreign keys.

### 2. SQL Query Capabilities & CLI Features

* **Multi-Table Joins (`INNER JOIN`)**: Aggregates booking manifests combining passenger details, assigned routes, seat allocations, and fare calculations.
* **Conditional Filtering (`WHERE`)**: Filters passenger manifests by discount eligibility and high-fare train routes.
* **Aggregation & Grouping (`GROUP BY`, `SUM`, `COUNT`)**: Computes operational metrics, including passenger counts and total revenue generated per train line.
* **Interactive CLI**: Provides a terminal interface allowing real-time route inspection, manifest review, ticket booking, and revenue reporting with menu navigation.

## Project Structure

```text
velasco_danielyuan_labactivity6/
├── screenshots/         # Terminal execution evidence and query results
│   └── test_case_lab6_screenshots.pdf
├── src/
│   └── main.py          # SQLite schema initialization, data seeding, queries, and interactive CLI
├── schema.sql           # Standalone SQL schema script
└── README.md            # Activity documentation and execution instructions
```

## How to Run

1. Navigate to the project directory in your Ubuntu WSL terminal:
```bash
cd velasco_danielyuan_labactivity5
```

2. Run the database application using Python 3:
```bash
python3 src/main.py
```

## AI Disclosure

AI assistant (Gemini) has been used to assist in schema structure design, query formulation, and debugging during the development of this program.