import uuid
from datetime import datetime, date

import streamlit as st

from pawpal_system import Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Session state initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(id=str(uuid.uuid4()))

# --- Owner setup ---
st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
owner_email = st.text_input("Owner email", value="jordan@example.com")

if st.button("Set Owner"):
    st.session_state.owner = Owner(
        id=str(uuid.uuid4()), name=owner_name, email=owner_email
    )
    st.success(f"Owner '{owner_name}' saved.")

# --- Add a Pet ---
if st.session_state.owner:
    st.divider()
    st.subheader("Add a Pet")

    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        species = st.selectbox("Species", ["Dog", "Cat", "Other"])
    with col3:
        breed = st.text_input("Breed", value="Mixed")
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=2)

    if st.button("Add Pet"):
        pet = Pet(
            id=str(uuid.uuid4()),
            name=pet_name,
            species=species,
            breed=breed,
            age=int(age),
        )
        st.session_state.owner.add_pet(pet)
        st.success(f"Added {pet_name} to {st.session_state.owner.name}'s pets.")

    if st.session_state.owner.pets:
        st.write("Pets:", [p.name for p in st.session_state.owner.pets])

# --- Schedule a Task ---
if st.session_state.owner and st.session_state.owner.pets:
    st.divider()
    st.subheader("Schedule a Task")

    pet_options = {p.name: p for p in st.session_state.owner.pets}
    selected_pet = pet_options[st.selectbox("Select pet", list(pet_options))]

    col1, col2 = st.columns(2)
    with col1:
        task_action = st.text_input("Task", value="Morning walk")
        task_description = st.text_input("Description", value="")
    with col2:
        task_date = st.date_input("Date", value=date.today())
        task_time = st.time_input("Time", value=datetime.now().replace(second=0, microsecond=0).time())

    if st.button("Add Task"):
        scheduled_at = datetime.combine(task_date, task_time)
        task = st.session_state.owner.create_task(selected_pet, task_action, scheduled_at)
        task.description = task_description
        st.session_state.scheduler.add_task(task)
        st.success(f"'{task_action}' scheduled for {scheduled_at.strftime('%b %d at %I:%M %p')}.")

# --- Generate Schedule ---
st.divider()
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    owner = st.session_state.owner
    if not owner or not owner.tasks:
        st.info("No tasks yet. Add an owner, pet, and tasks above.")
    else:
        all_tasks = sorted(owner.tasks, key=lambda t: t.scheduled_at)
        upcoming = st.session_state.scheduler.get_upcoming_tasks()

        st.markdown(f"**{owner.name}'s Schedule**")
        st.table(
            [
                {
                    "Time": t.scheduled_at.strftime("%b %d, %I:%M %p"),
                    "Pet": t.pet.name if t.pet else "—",
                    "Task": t.action,
                    "Description": t.description,
                    "Status": t.status,
                }
                for t in all_tasks
            ]
        )
        st.caption(f"{len(upcoming)} upcoming task(s) from now.")
