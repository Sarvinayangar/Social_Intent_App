import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

# --------------------------------------------------
# Page setup
# --------------------------------------------------
st.set_page_config(page_title="Social Intention Annotation Tool", layout="centered")

# --------------------------------------------------
# Taxonomy based on Action Label document
# --------------------------------------------------
ACTION_TAXONOMY = {
    "Object Manipulation Interaction": [
        "Lift Together",
        "Carry Together",
        "Rotate Object",
        "Reposition Object",
        "Stabilize Object",
    ],
    "Load Transfer Interaction": [
        "Pass Object",
        "Receive Object",
        "Load Transfer",
        "Delayed Acceptance",
    ],
    "Force Conflict Interaction": [
        "Pulling Interaction",
        "Resistance",
        "Force Mismatch",
        "Object Tugging",
    ],
    "Physical Guidance Interaction": [
        "Hand Guidance",
        "Correcting Grip",
        "Tap to Prompt",
        "Assist Grip",
    ],
    "Encouragement / Social Gesture": [
        "Thumbs Up",
        "Clapping",
        "Supportive Touch",
    ],
    "Attention / Warning Gestures": [
        "Tap to Alert",
        "Stop Gesture",
        "Pointing",
    ],
}

HIGH_LEVEL_SOCIAL_INTENTION = [
    "Affiliative",
    "Dominant / Assertive",
    "Instructional",
    "Avoidant / Defensive",
    "Cooperative / Symmetrical",
    "Other / Unclear",
]

TACTILE_SPECIFIC_INTENTION = [
    "Supportive",
    "Coercive",
    "Hesitant",
    "Consoling",
    "Struggle",
    "Not applicable / unclear",
]

AUDIO_CONTEXT = [
    "Urgent",
    "Formal",
    "None",
    "Unclear",
]

ROLE_BASED_LABEL = [
    "Initiator",
    "Recipient",
    "Synchronous",
    "Mismatch Intent",
    "Unclear",
]

# --------------------------------------------------
# Example scenarios but can be updated later when real scenarios are determined 
# --------------------------------------------------
INTERACTIONS = [
    {
        "interaction_id": "I01",
        "title": "Object handover during collaboration",
        "description": "One human passes an object to another human during a collaborative task.",
    },
    {
        "interaction_id": "I02",
        "title": "Joint object transport",
        "description": "Two humans jointly carry or reposition a shared object from one location to another.",
    },
    {
        "interaction_id": "I03",
        "title": "Physical correction during task",
        "description": "One human physically guides or corrects the other human's hand position during a task.",
    },
    {
        "interaction_id": "I04",
        "title": "Attention or warning gesture",
        "description": "One human uses a gesture or touch to attract attention or signal caution.",
    },
]

OUTPUT_FILE = Path("social_intention_annotations.csv")

# --------------------------------------------------
# Helper functions
# --------------------------------------------------
def save_response(row: dict):
    df_new = pd.DataFrame([row])
    if OUTPUT_FILE.exists():
        df_new.to_csv(OUTPUT_FILE, mode="a", header=False, index=False)
    else:
        df_new.to_csv(OUTPUT_FILE, index=False)


def load_saved_data():
    if OUTPUT_FILE.exists():
        return pd.read_csv(OUTPUT_FILE)
    return pd.DataFrame()


# --------------------------------------------------
# UI
# --------------------------------------------------
st.title("Social Intention Annotation Tool")
st.write(
    "This app is used to record the social intention labels associated with an observed action. "
    "It replaces free-text descriptors with a structured annotation during Participation."
)

with st.expander("Instructions", expanded=True):
    st.markdown(
        """
        1. Enter annotator and trial information.
        2. Select the interaction or scenario.
        3. Choose the action category and specific action.
        4. Record the high-level social intention.
        5. Record the tactile-specific intention if relevant.
        6. Record audio context and role-based label.
        7. Add confidence and notes.
        8. Save the annotation.
        """
    )

# --------------------------------------------------
# Annotator and trial information
# --------------------------------------------------
st.subheader("Annotator and trial information")
annotator_id = st.text_input("Annotator ID", placeholder="e.g. A01")
participant_id = st.text_input("Participant ID (optional)", placeholder="e.g. P01")
trial_id = st.text_input("Trial ID (optional)", placeholder="e.g. T01")

selected_interaction_title = st.selectbox(
    "Select interaction / scenario",
    options=[item["title"] for item in INTERACTIONS],
)

selected_interaction = next(
    item for item in INTERACTIONS if item["title"] == selected_interaction_title
)

st.markdown(f"**Interaction ID:** {selected_interaction['interaction_id']}")
st.markdown(f"**Scenario description:** {selected_interaction['description']}")

custom_scenario = st.text_area(
    "Additional interaction context (optional)",
    placeholder="Add any extra context about what happened in this trial..."
)

st.divider()

# --------------------------------------------------
# Action annotation
# --------------------------------------------------
st.subheader("Action annotation")
action_category = st.selectbox(
    "Action category",
    options=list(ACTION_TAXONOMY.keys()) + ["Other"],
)

if action_category != "Other":
    specific_action = st.selectbox(
        "Specific action",
        options=ACTION_TAXONOMY[action_category] + ["Other"],
    )
else:
    specific_action = "Other"

custom_action = ""
if action_category == "Other" or specific_action == "Other":
    custom_action = st.text_input(
        "Custom action label",
        placeholder="Enter the observed action"
    )

st.divider()

# --------------------------------------------------
# Social intention annotation
# --------------------------------------------------
st.subheader("Social intention annotation")
high_level_intention = st.radio(
    "High-level social intention",
    options=HIGH_LEVEL_SOCIAL_INTENTION,
    index=None,
)

tactile_intention = st.radio(
    "Tactile-specific intention",
    options=TACTILE_SPECIFIC_INTENTION,
    index=None,
)

audio_context = st.radio(
    "Audio context",
    options=AUDIO_CONTEXT,
    index=None,
)

role_label = st.radio(
    "Role-based label",
    options=ROLE_BASED_LABEL,
    index=None,
)

confidence = st.slider(
    "Annotation confidence",
    min_value=1,
    max_value=5,
    value=3,
)

notes = st.text_area(
    "Notes",
    placeholder="Add any uncertainty, reasoning, or extra observation here..."
)

st.divider()

# --------------------------------------------------
# Save annotation
# --------------------------------------------------
if st.button("Save annotation"):
    missing = []

    final_action = specific_action
    if action_category == "Other" or specific_action == "Other":
        if not custom_action.strip():
            missing.append("Custom action label")
        else:
            final_action = custom_action.strip()

    if not annotator_id.strip():
        missing.append("Annotator ID")
    if high_level_intention is None:
        missing.append("High-level social intention")
    if tactile_intention is None:
        missing.append("Tactile-specific intention")
    if audio_context is None:
        missing.append("Audio context")
    if role_label is None:
        missing.append("Role-based label")

    if missing:
        st.error("Please complete: " + ", ".join(missing))
    else:
        row = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "annotator_id": annotator_id,
            "participant_id": participant_id,
            "trial_id": trial_id,
            "interaction_id": selected_interaction["interaction_id"],
            "interaction_title": selected_interaction["title"],
            "interaction_description": selected_interaction["description"],
            "additional_context": custom_scenario,
            "action_category": action_category,
            "specific_action": final_action,
            "high_level_social_intention": high_level_intention,
            "tactile_specific_intention": tactile_intention,
            "audio_context": audio_context,
            "role_based_label": role_label,
            "confidence": confidence,
            "notes": notes,
        }
        save_response(row)
        st.success("Annotation saved successfully.")

# --------------------------------------------------
# Saved annotations
# --------------------------------------------------
st.subheader("Saved annotations")
saved_df = load_saved_data()

if not saved_df.empty:
    st.dataframe(saved_df, use_container_width=True)
    st.download_button(
        label="Download annotations as CSV",
        data=saved_df.to_csv(index=False).encode("utf-8"),
        file_name="social_intention_annotations.csv",
        mime="text/csv",
    )
else:
    st.info("No annotations saved yet.")
