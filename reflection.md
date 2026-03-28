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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
