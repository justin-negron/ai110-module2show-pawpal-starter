# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

The scheduler includes several algorithmic features beyond basic task listing:

- **Priority-based sorting** - Tasks are sorted by priority (high > medium > low), with shorter tasks scheduled first as a tiebreaker
- **Sort by time** - Option to sort tasks by duration for quick-win planning
- **Filtering** - Filter tasks by completion status, pet name, or category
- **Recurring tasks** - Daily and weekly tasks automatically generate their next occurrence when completed, using `timedelta` for accurate date math
- **Conflict detection** - Warns about duplicate tasks, same-category overlaps on the same day, and when total task time exceeds available time. Returns warnings rather than blocking, so the owner stays informed without losing flexibility

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

The tests cover:

- **Task basics** - marking tasks complete, adding tasks to pets
- **Sorting** - verifying sort by time (shortest first) and sort by priority (high first)
- **Recurring tasks** - daily tasks reschedule for tomorrow, weekly for next week, as-needed tasks don't recur
- **Conflict detection** - catches duplicate task names, same-category overlaps, and time overload warnings
- **Edge cases** - empty task lists produce empty plans, lower-priority tasks get skipped when time runs out

**Confidence Level: 4/5 stars** - The core scheduling logic, recurrence, and conflict detection are well covered. The main gap is that we haven't tested the Streamlit UI integration or more complex multi-pet scenarios, but the backend logic is solid.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
