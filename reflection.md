# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Before jumping into code, I thought about what a pet owner would actually need to do with this app day to day. I came up with three core actions:

1. **Enter pet and owner info** — The user should be able to set up a profile with basic details about themselves and their pet. This gives the app context for generating a good plan.
2. **Add and edit care tasks** — The user needs to create tasks like walks, feeding, medications, grooming, etc., each with at least a duration and priority. They should also be able to update these as things change.
3. **Generate a daily schedule** — Given the tasks and any constraints (like how much time they have), the app should produce a smart daily plan and explain why it organized things that way.

I settled on five classes for the system:

- **Pet** — holds basic pet info (name, species, breed, age). Keeps things simple with just a summary method. I used a dataclass here since it's really just structured data.
- **Owner** — stores the owner's name, how many minutes they have available, and a reference to their Pet. Also a dataclass.
- **Task** — represents a single care task (like "morning walk" or "give meds"). Each task has a category, duration, priority, and a completed flag. This is the core unit that everything else works with.
- **Scheduler** — this is the brain. It takes a list of tasks and the available time, then figures out which tasks fit and in what order. It produces a DailyPlan.
- **DailyPlan** — the output of the scheduler. It holds the tasks that made the cut, the ones that got skipped, and can explain the reasoning behind the choices.

The main relationships are: Owner has a Pet, Scheduler takes in Tasks and outputs a DailyPlan.

**b. Design changes**

When I reviewed the skeleton with AI, one thing that came up was that the Owner class doesn't directly hold a list of tasks, there's no "Owner.tasks" attribute. I thought about adding one, but decided against it. The Streamlit app layer is a better place to manage the task list since that's where user interaction happens. Adding it to Owner would create tighter coupling without a real benefit. So I kept the design as-is, but it was good to think through that decision explicitly.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two main constraints: the owner's available time and task priority (high, medium, low). It sorts tasks by priority first, using duration as a tiebreaker, then greedily fills the available time starting with the most important tasks. I decided priority should matter most because with pet care, you really want to make sure the critical stuff (meds, walks) happens even if it means skipping the nice-to-haves.

**b. Tradeoffs**

One big tradeoff is in how conflict detection works. Our tasks have due dates but no specific start times, so the conflict checker flags any two tasks in the same category on the same day as a potential overlap. That means if you have a "Morning Walk" and an "Evening Walk," it'll warn you even though they clearly don't conflict in real life. I considered adding time-of-day scheduling, but it would add a lot of complexity for what's supposed to be a simple daily planner. The warning approach felt right — it nudges you to think about it without blocking you.

Another tradeoff is the greedy scheduling algorithm. It picks the highest priority tasks first, which means it might skip a bunch of small lower-priority tasks that could technically all fit. A more optimal approach (like a knapsack algorithm) could maximize total tasks completed, but for pet care, making sure the important things get done matters more than cramming in every little task.

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude Code (CLI) throughout the entire project instead of VS Code Copilot, but the workflow was similar. The most useful ways I used it:

- **Design brainstorming** — I described the app's purpose and had AI help me identify the core classes and their relationships. It was like having a whiteboard partner who could also write Mermaid diagrams.
- **Skeleton generation** — Once we agreed on the UML, AI translated the diagram into Python dataclass stubs really quickly. That saved a lot of boilerplate typing.
- **Algorithmic implementation** — For things like recurring task logic with `timedelta` and the greedy scheduling algorithm, I described what I wanted and AI wrote the first draft. I'd review it and adjust.
- **Test generation** — I outlined what behaviors to test, and AI drafted the actual test functions. This was probably where it saved me the most time.

The most helpful prompts were specific ones — "implement a method that does X given Y constraints" worked way better than vague asks like "make this better." Giving context about what the method needed to handle made the output much more usable.

**b. Judgment and verification**

One clear example: early in the design phase, AI initially set up Owner with a single Pet reference. When the Phase 2 instructions called for Owner to manage multiple pets, I had to rethink the relationship. I also pushed back on adding an `Owner.tasks` list — AI suggested it as a convenience, but I decided the tasks should live on each Pet instead, with Owner just aggregating them through its pets. That kept the data model cleaner and avoided having tasks stored in two places.

I verified suggestions by running the code each time. After every implementation step, we ran `main.py` or `pytest` to confirm things actually worked, not just that they looked right. The terminal output was my source of truth, not the AI's confidence.

---

## 4. Testing and Verification

**a. What you tested**

I tested 13 behaviors across five areas:

- **Task basics** — that `mark_complete()` actually flips the status, and `add_task()` increases the task count. These are foundational — if these break, nothing else matters.
- **Sorting** — that `sort_by_time` returns shortest first and `sort_by_priority` returns high before medium before low. The scheduler depends on correct ordering.
- **Recurrence** — that daily tasks create a next-day copy, weekly tasks create a next-week copy, and as-needed tasks don't recur at all. Also that `Pet.mark_task_complete` properly adds the new occurrence to the pet's task list.
- **Conflict detection** — that duplicate task names, same-category overlaps, and time overload all generate appropriate warnings.
- **Edge cases** — an empty task list should produce an empty plan without errors, and when tasks exceed available time, lower-priority ones should get skipped while staying within the time budget.

These tests were important because they cover the core contract of the app — if a user adds tasks and generates a plan, the output needs to be correct and predictable.

**b. Confidence**

I'd say 4 out of 5 stars. The backend logic is well tested and I'm confident the scheduling, sorting, recurrence, and conflict detection all work correctly. What's not tested is the Streamlit UI layer — things like session state persistence, button interactions, and edge cases around the form inputs. If I had more time, I'd add tests for multi-pet scheduling scenarios (like three pets with overlapping high-priority tasks) and test what happens when someone marks the same task complete twice.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with how the system design held up throughout the project. The five-class structure (Task, Pet, Owner, Scheduler, DailyPlan) that we sketched in Phase 1 mostly survived all the way to the final implementation. The classes grew — Task got `due_date` and recurrence, Pet gained `mark_task_complete`, Scheduler picked up sorting/filtering/conflict detection — but the core architecture didn't need to be torn apart. That felt like a win for taking the time to design before coding.

**b. What you would improve**

If I had another iteration, I'd add time-of-day scheduling. Right now tasks just have a duration and due date, but no start time. That's why the conflict detection is a bit blunt — it can't tell if two walks are actually at the same time or hours apart. Adding a `start_time` field to Task and doing real overlap detection would make the scheduler much smarter. I'd also want to build a way to save and load data so your pets and tasks persist between sessions.

**c. Key takeaway**

The biggest thing I learned is that AI is an incredible coding partner, but you have to stay in the driver's seat. It's tempting to just accept whatever it generates, but the moments where I pushed back — like keeping tasks on Pet instead of Owner, or choosing a greedy algorithm over something fancier — those decisions shaped the whole project. AI can write code fast, but it doesn't know your constraints, your users, or what "simple enough" means for your specific situation. Being the lead architect means knowing when to say "no, let's keep it simpler" and when to say "actually, let's make this smarter." That judgment is the human's job.
