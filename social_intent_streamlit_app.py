import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

# ==================================================
# Page setup
# ==================================================
st.set_page_config(page_title="Social Intention Annotation Tool", layout="centered")

# ==================================================
# File paths
# ==================================================
ANNOTATION_OUTPUT_FILE = Path("social_intention_annotations.csv")
POST_SURVEY_OUTPUT_FILE = Path("post_task_questionnaire_responses.csv")

# ==================================================
# Scenario-driven annotation taxonomy
# The hierarchy is:
# Scenario -> Action family -> Specific action
# ==================================================
SCENARIO_TAXONOMY = {
    "Object handover during collaboration": {
        "interaction_id": "I01",
        "description": "One human passes an object to another human during a collaborative task.",
        "action_families": {
            "Load Transfer / Handovers": [
                "Pass Object",
                "Receive Object",
                "Load Transfer",
                "Passing and Receiving Object",
                "Delayed Handover",
                "Interrupted Handover",
                "Failed Handover",
                "Delayed Acceptance",
            ],
            "Attention / Warning Gestures": [
                "Pointing",
                "Tap to Alert",
                "Warning gesture",
            ],
            "Encouragement / Social Gesture": [
                "Supportive Touch",
                "Handshake",
            ],
        },
    },
    "Joint object transport": {
        "interaction_id": "I02",
        "description": "Two humans jointly carry or reposition a shared object from one location to another.",
        "action_families": {
            "Object Manipulation Interaction": [
                "Lift Together",
                "Carry Together",
                "Rotate Object",
                "Reposition Object",
                "Lower Object Together",
                "Stabilize Object",
                "Steadily Hold Object",
                "Support partner with object",
                "Assist while partner adjusts object",
            ],
            "Force Conflict Interaction": [
                "Force Mismatch",
                "Resistance",
                "Object Tugging",
            ],
            "Load Transfer / Handovers": [
                "Load Transfer",
                "Pass Object",
                "Receive Object",
            ],
        },
    },
    "Physical correction during task": {
        "interaction_id": "I03",
        "description": "One human physically guides or corrects the other human's hand position during a task.",
        "action_families": {
            "Physical Guidance Interaction": [
                "Hand Guidance",
                "Correcting Grip",
                "Tap to Prompt",
                "Assist Grip",
                "Physically moving partner's hand",
            ],
            "Encouragement / Social Gesture": [
                "Supportive Touch",
                "Thumbs Up",
            ],
            "Attention / Warning Gestures": [
                "Pointing",
                "Stop Gesture",
            ],
        },
    },
    "Attention or warning gesture": {
        "interaction_id": "I04",
        "description": "One human uses a gesture or touch to attract attention or signal caution.",
        "action_families": {
            "Attention / Warning Gestures": [
                "Tap to Alert",
                "Stop Gesture",
                "Pointing",
                "Warning gesture",
            ],
            "Encouragement / Social Gesture": [
                "Supportive Touch",
                "Thumbs Up",
                "Clapping",
            ],
        },
    },
    "Cooperative game or shared task": {
        "interaction_id": "I05",
        "description": "Two humans cooperate in a shared activity such as ball exchange, Jenga, hand games, cooking, or assistance tasks.",
        "action_families": {
            "Collaboration / Cooperative Tasks": [
                "Kicking ball to partner",
                "Throwing ball to partner",
                "Building Jenga together",
                "Playing Jenga together",
                "Hand game",
                "Cooking together",
                "Acquiring ingredient from storage",
                "Sorting ingredients",
                "Healing partner",
                "Applying bandage to partner",
                "Using epi-pen on partner",
                "Assisting blind partner",
                "Assisting elderly partner",
                "Carrying object to rescue partner",
            ],
            "Load Transfer / Handovers": [
                "Pass Object",
                "Receive Object",
                "Passing and Receiving Object",
            ],
            "Encouragement / Social Gesture": [
                "Thumbs Up",
                "Clapping",
                "Supportive Touch",
            ],
        },
    },
    "Emotional or behavioural interaction": {
        "interaction_id": "I06",
        "description": "An interaction involving emotional escalation, defensive behaviour, or lifting/carrying another person for excitement, aggression, or aid.",
        "action_families": {
            "Emotional / Behavioural Tasks": [
                "Shouting",
                "Defensive stance",
                "Lifting another person",
                "Carrying another person",
                "Excited lift/carry",
                "Aggressive lift/carry",
                "Aid-based lift/carry",
            ],
            "Force Conflict Interaction": [
                "Resistance",
                "Pulling Interaction",
                "Object Tugging",
            ],
            "Physical Guidance Interaction": [
                "Hand Guidance",
                "Physically moving partner's hand",
            ],
        },
    },
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

# ==================================================
# Participant-facing post-task questionnaire items
# Replace these examples later with VLM-generated items
# ==================================================
POST_TASK_SURVEY_ITEMS = [
    {
        "item_id": "Q1",
        "question_type": "Goal Inference",
        "question": "At 00:15, when you handed the red cup to your partner, what was your primary goal?",
        "options": [
            "To clear space on my side of the table.",
            "To allow my partner to pour water into it.",
            "To show the cup to my partner.",
            "To indicate that I was finished with my task.",
        ],
    },
    {
        "item_id": "Q2",
        "question_type": "Belief Inference",
        "question": "Right before your partner reached for the cutting board at 00:30, what did you believe they were trying to achieve?",
        "options": [
            "I believed they were going to move it out of the way.",
            "I believed they needed it to start preparing the next item.",
            "I believed they thought it was my turn to use it.",
            "I did not notice their action at the time.",
        ],
    },
    {
        "item_id": "Q3",
        "question_type": "Action Grounding",
        "question": "Instead of placing the tool on the table, why did you choose to hold the tool out for your partner at 01:00?",
        "options": [
            "I anticipated they would need it immediately for their next step.",
            "There was no space left on the table.",
            "I wanted them to take it from me so I could rest my hand.",
            "It was an unconscious habit.",
        ],
    },
    {
        "item_id": "Q4",
        "question_type": "Intent Recognition",
        "question": "When your partner looked at the empty plate and extended their open hand at 01:30, how did you interpret their immediate intention?",
        "options": [
            "They wanted me to pass them the apple.",
            "They were pointing out where I should place the next item.",
            "They were pausing to rest their arm.",
            "I was unsure of their intention at that exact moment.",
        ],
    },
    {
        "item_id": "Q5",
        "question_type": "Partner Trust in Collaboration",
        "question": "During the collaborative handover of the water bottle at 01:45, to what extent did you trust that your partner had a secure grip before you released your hands?",
        "options": [
            "Completely - I waited to feel the tactile resistance or a visual cue before letting go.",
            "Mostly - I let go as soon as our hands touched, assuming they would grab it.",
            "Somewhat - I released it quickly to speed up the task without confirming.",
            "Not at all - I kept supporting the weight until they pulled it away.",
        ],
    },
]

# ==================================================
# Helpers
# ==================================================
def append_to_csv(output_file: Path, row: dict) -> None:
    df_new = pd.DataFrame([row])
    if output_file.exists():
        df_new.to_csv(output_file, mode="a", header=False, index=False)
    else:
        df_new.to_csv(output_file, index=False)


def load_saved_data(output_file: Path) -> pd.DataFrame:
    if output_file.exists():
        return pd.read_csv(output_file)
    return pd.DataFrame()


def reset_action_family() -> None:
    st.session_state["action_family"] = ""
    st.session_state["specific_action"] = ""
    st.session_state["custom_action"] = ""


def reset_specific_action() -> None:
    st.session_state["specific_action"] = ""
    st.session_state["custom_action"] = ""


# ==================================================
# Tabs
# ==================================================
annotation_tab, survey_tab = st.tabs([
    "Annotation Tool",
    "Post-Task Questionnaire",
])

# ==================================================
# Annotation tool
# ==================================================
with annotation_tab:
    st.title("Social Intention Annotation Tool")
    st.write(
        "This tool is used by the researcher to record the social intention associated with an observed action. "
        "The fields are linked so the available action options depend on the chosen recording scenario."
    )

    with st.expander("Instructions", expanded=True):
        st.markdown(
            """
            1. Enter annotator and trial information.
            2. Choose the recording scenario.
            3. Choose an action family that fits that scenario.
            4. Choose the specific action from the filtered list.
            5. Record the social intention labels.
            6. Add confidence and notes.
            7. Save the annotation.
            """
        )

    st.subheader("Annotator and trial information")
    annotator_id = st.text_input("Annotator ID", placeholder="e.g. A01")
    participant_id = st.text_input("Participant ID (optional)", placeholder="e.g. P01")
    trial_id = st.text_input("Trial ID (optional)", placeholder="e.g. T01")

    scenario_name = st.selectbox(
        "Select interaction / scenario",
        options=list(SCENARIO_TAXONOMY.keys()),
        key="scenario_name",
        on_change=reset_action_family,
    )

    scenario_data = SCENARIO_TAXONOMY[scenario_name]
    st.markdown(f"**Interaction ID:** {scenario_data['interaction_id']}")
    st.markdown(f"**Scenario description:** {scenario_data['description']}")

    additional_context = st.text_area(
        "Additional interaction context (optional)",
        placeholder="Add any extra context about what happened in this trial..."
    )

    st.divider()

    st.subheader("Action annotation")
    available_families = list(scenario_data["action_families"].keys()) + ["Other"]

    current_family = st.session_state.get("action_family", "")
    if current_family not in available_families:
        st.session_state["action_family"] = ""

    action_family = st.selectbox(
        "Action family",
        options=[""] + available_families,
        key="action_family",
        on_change=reset_specific_action,
    )

    available_actions = []
    if action_family and action_family != "Other":
        available_actions = scenario_data["action_families"][action_family] + ["Other"]

    current_action = st.session_state.get("specific_action", "")
    if available_actions and current_action not in available_actions + [""]:
        st.session_state["specific_action"] = ""

    if action_family and action_family != "Other":
        specific_action = st.selectbox(
            "Specific action",
            options=[""] + available_actions,
            key="specific_action",
        )
    elif action_family == "Other":
        specific_action = "Other"
    else:
        specific_action = ""
        st.info("Choose an action family first to see the relevant action options.")

    custom_action = ""
    if action_family == "Other" or specific_action == "Other":
        custom_action = st.text_input(
            "Custom action label",
            placeholder="Enter the observed action",
            key="custom_action",
        )

    st.divider()

    st.subheader("Social intention annotation")
    high_level_intention = st.selectbox(
        "High-level social intention",
        options=[""] + HIGH_LEVEL_SOCIAL_INTENTION,
    )
    tactile_intention = st.selectbox(
        "Tactile-specific intention",
        options=[""] + TACTILE_SPECIFIC_INTENTION,
    )
    audio_context = st.selectbox(
        "Audio context",
        options=[""] + AUDIO_CONTEXT,
    )
    role_label = st.selectbox(
        "Role-based label",
        options=[""] + ROLE_BASED_LABEL,
    )

    confidence = st.slider("Annotation confidence", 1, 5, 3)
    notes = st.text_area(
        "Notes",
        placeholder="Add any uncertainty, reasoning, or extra observation here..."
    )

    st.divider()

    if st.button("Save annotation"):
        missing = []

        final_action = specific_action
        if not action_family:
            missing.append("Action family")
        if action_family == "Other" or specific_action == "Other":
            if not custom_action.strip():
                missing.append("Custom action label")
            else:
                final_action = custom_action.strip()
        elif not specific_action:
            missing.append("Specific action")

        if not annotator_id.strip():
            missing.append("Annotator ID")
        if not high_level_intention:
            missing.append("High-level social intention")
        if not tactile_intention:
            missing.append("Tactile-specific intention")
        if not audio_context:
            missing.append("Audio context")
        if not role_label:
            missing.append("Role-based label")

        if missing:
            st.error("Please complete: " + ", ".join(missing))
        else:
            row = {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "annotator_id": annotator_id,
                "participant_id": participant_id,
                "trial_id": trial_id,
                "interaction_id": scenario_data["interaction_id"],
                "interaction_title": scenario_name,
                "interaction_description": scenario_data["description"],
                "additional_context": additional_context,
                "action_family": action_family,
                "specific_action": final_action,
                "high_level_social_intention": high_level_intention,
                "tactile_specific_intention": tactile_intention,
                "audio_context": audio_context,
                "role_based_label": role_label,
                "confidence": confidence,
                "notes": notes,
            }
            append_to_csv(ANNOTATION_OUTPUT_FILE, row)
            st.success("Annotation saved successfully.")

    st.subheader("Saved annotations")
    saved_annotations = load_saved_data(ANNOTATION_OUTPUT_FILE)
    if not saved_annotations.empty:
        st.dataframe(saved_annotations, use_container_width=True)
        st.download_button(
            label="Download annotations as CSV",
            data=saved_annotations.to_csv(index=False).encode("utf-8"),
            file_name="social_intention_annotations.csv",
            mime="text/csv",
        )
    else:
        st.info("No annotations saved yet.")

# ==================================================
# Participant-facing post-task questionnaire
# ==================================================
with survey_tab:
    st.title("Post-Task Interaction Intent Questionnaire")
    st.write(
        "This questionnaire is for participants after the task. Please read each question and select the option "
        "that best matches what you intended, believed, or understood during the interaction."
    )

    with st.expander("Participant instructions", expanded=True):
        st.markdown(
            """
            Please answer every question by selecting the option that best matches your experience.
            There are no typed answers required for the questionnaire itself.
            """
        )

    survey_participant_id = st.text_input("Participant ID", placeholder="e.g. P01", key="survey_pid")
    survey_trial_id = st.text_input("Trial ID", placeholder="e.g. T01", key="survey_tid")

    st.divider()

    survey_responses = {}

    for item in POST_TASK_SURVEY_ITEMS:
        st.subheader(f"{item['item_id']}: {item['question_type']}")
        st.markdown(item["question"])
        survey_responses[item["item_id"]] = st.radio(
            "Select one option:",
            options=item["options"],
            index=None,
            key=f"survey_{item['item_id']}",
        )
        st.divider()

    survey_notes = st.text_area(
        "Researcher notes (optional)",
        placeholder="Optional notes only...",
        key="survey_notes"
    )

    if st.button("Submit questionnaire"):
        missing = []
        if not survey_participant_id.strip():
            missing.append("Participant ID")
        if not survey_trial_id.strip():
            missing.append("Trial ID")

        for item in POST_TASK_SURVEY_ITEMS:
            if survey_responses[item["item_id"]] is None:
                missing.append(item["item_id"])

        if missing:
            st.error("Please complete: " + ", ".join(missing))
        else:
            row = {
                "timestamp_saved": datetime.now().isoformat(timespec="seconds"),
                "participant_id": survey_participant_id,
                "trial_id": survey_trial_id,
                "notes": survey_notes,
            }

            for item in POST_TASK_SURVEY_ITEMS:
                row[f"{item['item_id']}_type"] = item["question_type"]
                row[f"{item['item_id']}_question"] = item["question"]
                row[f"{item['item_id']}_response"] = survey_responses[item["item_id"]]

            append_to_csv(POST_SURVEY_OUTPUT_FILE, row)
            st.success("Questionnaire submitted successfully.")

    st.subheader("Saved questionnaire responses")
    saved_surveys = load_saved_data(POST_SURVEY_OUTPUT_FILE)
    if not saved_surveys.empty:
        st.dataframe(saved_surveys, use_container_width=True)
        st.download_button(
            label="Download questionnaire responses as CSV",
            data=saved_surveys.to_csv(index=False).encode("utf-8"),
            file_name="post_task_questionnaire_responses.csv",
            mime="text/csv",
        )
    else:
        st.info("No questionnaire responses saved yet.")
