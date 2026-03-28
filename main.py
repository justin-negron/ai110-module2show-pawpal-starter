from pawpal_system import Owner, Pet, Task, Scheduler

# Create pets
buddy = Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=4)
whiskers = Pet(name="Whiskers", species="Cat", breed="Siamese", age=2)

# Create owner with 60 minutes available
owner = Owner(name="Justin", available_minutes=60)
owner.add_pet(buddy)
owner.add_pet(whiskers)

# Add normal tasks
buddy.add_task(Task(name="Morning Walk", category="walk", duration=30, priority="high"))
buddy.add_task(Task(name="Give Heartworm Meds", category="meds", duration=5, priority="high", frequency="weekly"))
whiskers.add_task(Task(name="Clean Litter Box", category="grooming", duration=10, priority="high"))
whiskers.add_task(Task(name="Play Session", category="enrichment", duration=20, priority="medium"))

# Add CONFLICTING tasks — two walks on the same day, duplicate task name
buddy.add_task(Task(name="Evening Walk", category="walk", duration=25, priority="medium"))  # same category as Morning Walk
buddy.add_task(Task(name="Morning Walk", category="walk", duration=30, priority="high"))    # duplicate name + same date

print("=== All Tasks ===")
for pet in owner.pets:
    print(f"\n{pet.name}:")
    for t in pet.tasks:
        print(f"  {t.get_summary()}")

# Run conflict detection
all_tasks = owner.get_all_tasks()
scheduler = Scheduler(tasks=all_tasks, available_minutes=owner.available_minutes)

print("\n=== Conflict Detection ===")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  ⚠ {warning}")
else:
    print("  No conflicts detected.")

# Generate plan anyway (warnings don't block scheduling)
print()
plan = scheduler.generate_plan()
print(plan.display())
