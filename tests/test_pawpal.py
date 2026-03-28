from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# --- Existing tests ---

def test_mark_complete_changes_status():
    task = Task(name="Morning Walk", category="walk", duration=30, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=4)
    assert len(pet.tasks) == 0
    pet.add_task(Task(name="Walk", category="walk", duration=30, priority="high"))
    assert len(pet.tasks) == 1
    pet.add_task(Task(name="Feed", category="feeding", duration=10, priority="high"))
    assert len(pet.tasks) == 2


# --- Sorting correctness ---

def test_sort_by_time_returns_shortest_first():
    tasks = [
        Task(name="Long Walk", category="walk", duration=45, priority="high"),
        Task(name="Quick Feed", category="feeding", duration=5, priority="low"),
        Task(name="Play Time", category="enrichment", duration=20, priority="medium"),
    ]
    scheduler = Scheduler(tasks=tasks, available_minutes=60)
    sorted_tasks = scheduler.sort_by_time()
    durations = [t.duration for t in sorted_tasks]
    assert durations == [5, 20, 45]


def test_sort_by_priority_orders_high_first():
    tasks = [
        Task(name="Brush Coat", category="grooming", duration=15, priority="low"),
        Task(name="Give Meds", category="meds", duration=5, priority="high"),
        Task(name="Play Session", category="enrichment", duration=20, priority="medium"),
    ]
    scheduler = Scheduler(tasks=tasks, available_minutes=60)
    sorted_tasks = scheduler.sort_by_priority()
    priorities = [t.priority for t in sorted_tasks]
    assert priorities == ["high", "medium", "low"]


# --- Recurrence logic ---

def test_daily_task_creates_next_day_occurrence():
    task = Task(name="Morning Walk", category="walk", duration=30, priority="high", frequency="daily")
    original_due = task.due_date
    next_task = task.mark_complete()
    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_date == original_due + timedelta(days=1)


def test_weekly_task_creates_next_week_occurrence():
    task = Task(name="Bath", category="grooming", duration=30, priority="medium", frequency="weekly")
    original_due = task.due_date
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == original_due + timedelta(weeks=1)


def test_as_needed_task_does_not_recur():
    task = Task(name="Vet Visit", category="meds", duration=60, priority="high", frequency="as-needed")
    next_task = task.mark_complete()
    assert task.completed is True
    assert next_task is None


def test_pet_mark_task_complete_adds_next_occurrence():
    pet = Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=4)
    pet.add_task(Task(name="Walk", category="walk", duration=30, priority="high", frequency="daily"))
    assert len(pet.tasks) == 1
    pet.mark_task_complete("Walk")
    # Original task is done, new one was added
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed is True
    assert pet.tasks[1].completed is False


# --- Conflict detection ---

def test_detects_duplicate_task_names():
    tasks = [
        Task(name="Morning Walk", category="walk", duration=30, priority="high"),
        Task(name="Morning Walk", category="walk", duration=30, priority="high"),
    ]
    scheduler = Scheduler(tasks=tasks, available_minutes=60)
    warnings = scheduler.detect_conflicts()
    assert any("more than once" in w for w in warnings)


def test_detects_same_category_conflict():
    tasks = [
        Task(name="Morning Walk", category="walk", duration=30, priority="high"),
        Task(name="Evening Walk", category="walk", duration=25, priority="medium"),
    ]
    scheduler = Scheduler(tasks=tasks, available_minutes=60)
    warnings = scheduler.detect_conflicts()
    assert any("both walk tasks" in w for w in warnings)


def test_detects_time_overload():
    tasks = [
        Task(name="Walk", category="walk", duration=40, priority="high"),
        Task(name="Play", category="enrichment", duration=40, priority="medium"),
    ]
    scheduler = Scheduler(tasks=tasks, available_minutes=30)
    warnings = scheduler.detect_conflicts()
    assert any("exceeds available time" in w for w in warnings)


# --- Edge cases ---

def test_empty_task_list_generates_empty_plan():
    scheduler = Scheduler(tasks=[], available_minutes=60)
    plan = scheduler.generate_plan()
    assert len(plan.scheduled_tasks) == 0
    assert len(plan.skipped_tasks) == 0
    assert plan.total_time_used == 0


def test_tasks_exceeding_time_skips_lower_priority():
    tasks = [
        Task(name="Give Meds", category="meds", duration=5, priority="high"),
        Task(name="Walk", category="walk", duration=30, priority="high"),
        Task(name="Play", category="enrichment", duration=20, priority="medium"),
        Task(name="Brush", category="grooming", duration=15, priority="low"),
    ]
    scheduler = Scheduler(tasks=tasks, available_minutes=40)
    plan = scheduler.generate_plan()
    # Should fit meds (5) + walk (30) = 35min, skip play and brush
    scheduled_names = [t.name for t in plan.scheduled_tasks]
    assert "Give Meds" in scheduled_names
    assert "Walk" in scheduled_names
    assert plan.total_time_used <= 40
    assert len(plan.skipped_tasks) > 0
