import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Initialize session state - only runs once per session
if "owner" not in st.session_state:
    st.session_state.owner = None

st.title("🐾 PawPal+")

st.markdown("A pet care planning assistant that helps you stay on top of daily tasks.")

st.divider()

# --- Owner Setup ---
st.subheader("Owner Setup")

if st.session_state.owner is None:
    owner_name = st.text_input("Your name", value="")
    available_minutes = st.number_input("Available minutes today", min_value=10, max_value=480, value=60)

    if st.button("Save Owner Profile"):
        if owner_name.strip():
            st.session_state.owner = Owner(name=owner_name.strip(), available_minutes=available_minutes)
            st.rerun()
        else:
            st.warning("Please enter your name.")
else:
    owner = st.session_state.owner
    st.success(f"Owner: {owner.name} | Available time: {owner.available_minutes} minutes")
    if st.button("Reset Profile"):
        st.session_state.owner = None
        st.rerun()

st.divider()

# --- Add a Pet ---
st.subheader("Add a Pet")

if st.session_state.owner is None:
    st.info("Set up your owner profile first.")
else:
    owner = st.session_state.owner

    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name", value="")
        species = st.selectbox("Species", ["Dog", "Cat", "Other"])
    with col2:
        breed = st.text_input("Breed", value="")
        age = st.number_input("Age", min_value=0, max_value=30, value=1)

    if st.button("Add Pet"):
        if pet_name.strip():
            new_pet = Pet(name=pet_name.strip(), species=species, breed=breed.strip(), age=age)
            owner.add_pet(new_pet)
            st.rerun()
        else:
            st.warning("Please enter a pet name.")

    # Show current pets
    if owner.pets:
        st.markdown("**Your Pets:**")
        for pet in owner.pets:
            st.write(f"- {pet.get_summary()}")
    else:
        st.info("No pets added yet.")

st.divider()

# --- Add Tasks ---
st.subheader("Add Tasks")

if st.session_state.owner is None or not st.session_state.owner.pets:
    st.info("Add at least one pet before creating tasks.")
else:
    owner = st.session_state.owner
    pet_names = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Assign task to pet", pet_names)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_name = st.text_input("Task name", value="")
    with col2:
        category = st.selectbox("Category", ["walk", "feeding", "meds", "grooming", "enrichment"])
    with col3:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=15)

    priority = st.selectbox("Priority", ["high", "medium", "low"])

    if st.button("Add Task"):
        if task_name.strip():
            new_task = Task(
                name=task_name.strip(),
                category=category,
                duration=int(duration),
                priority=priority,
            )
            # Find the selected pet and add the task
            for pet in owner.pets:
                if pet.name == selected_pet_name:
                    pet.add_task(new_task)
                    break
            st.rerun()
        else:
            st.warning("Please enter a task name.")

    # Show all tasks grouped by pet
    for pet in owner.pets:
        if pet.tasks:
            st.markdown(f"**{pet.name}'s Tasks:**")
            for task in pet.tasks:
                st.write(f"- {task.get_summary()}")

st.divider()

# --- Generate Schedule ---
st.subheader("Generate Daily Schedule")

if st.session_state.owner is None:
    st.info("Set up your profile and add tasks first.")
elif not st.session_state.owner.get_all_tasks():
    st.info("Add some tasks before generating a schedule.")
else:
    owner = st.session_state.owner

    if st.button("Generate Schedule"):
        all_tasks = owner.get_all_pending_tasks()
        scheduler = Scheduler(tasks=all_tasks, available_minutes=owner.available_minutes)
        plan = scheduler.generate_plan()

        st.markdown("### Today's Plan")
        st.text(plan.display())

        with st.expander("Why this plan?"):
            st.text(plan.get_reasoning())
