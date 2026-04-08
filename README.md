# Social Intention Annotation Tool

This project is a Streamlit-based prototype for annotating and evaluating **social intention in human-human interaction tasks**.

It has two linked parts:

1. a **researcher-facing annotation tool** for recording structured labels for observed actions and social intention
2. a **participant-facing post-task questionnaire** for selecting multiple-choice answers about goals, partner awareness, action choice, intent recognition, and collaboration trust

The overall aim is to replace broad free-text descriptions with a more consistent and analysable structure for both annotation and post-task self-report.

---

## Project purpose

This tool was developed for human-human interaction research involving collaborative, physical, and socially meaningful actions recorded during task-based sessions.

The annotation side is designed to let a researcher record:
- the interaction scenario
- the action family
- the specific action
- the high-level social intention
- the tactile-specific intention
- the audio context
- the role-based label
- confidence and notes

The post-task questionnaire side is designed for participants to answer structured multiple-choice questions after the interaction. These questions target:
- **goal inference**
- **belief inference**
- **action grounding**
- **intent recognition**
- **partner trust in collaboration**

---

## App structure

The Streamlit app has **two tabs**.

### 1. Annotation Tool
This tab is for the researcher.

It uses a **scenario-driven hierarchy**:

**Scenario → Action family → Specific action**

This means the available action labels depend on the recording context. The lower dropdowns update based on the higher-level selection so the annotation process better matches the actual structure of recording sessions.

Example scenarios currently included:
- Object handover during collaboration
- Joint object transport
- Physical correction during task
- Attention or warning gesture
- Cooperative game or shared task
- Emotional or behavioural interaction

### 2. Post-Task Questionnaire
This tab is for participants.

Participants are shown **all survey questions directly** and answer using multiple-choice selections only. They do not type the questionnaire content themselves.

The current prototype includes five question types:
- Goal Inference
- Belief Inference
- Action Grounding
- Intent Recognition
- Partner Trust in Collaboration

At this stage, the questionnaire uses example fixed items based on the study design. In a later version, these may be dynamically generated from recorded interaction data using a Vision-Language Model.

---

## Annotation framework

The researcher-facing annotation tool uses structured labels based on the project taxonomy.

### High-level social intention
- Affiliative
- Dominant / Assertive
- Instructional
- Avoidant / Defensive
- Cooperative / Symmetrical
- Other / Unclear

### Tactile-specific intention
- Supportive
- Coercive
- Hesitant
- Consoling
- Struggle
- Not applicable / unclear

### Audio context
- Urgent
- Formal
- None
- Unclear

### Role-based label
- Initiator
- Recipient
- Synchronous
- Mismatch Intent
- Unclear

### Example action families
Depending on the selected scenario, the annotation tool may include action families such as:
- Load Transfer / Handovers
- Object Manipulation Interaction
- Force Conflict Interaction
- Physical Guidance Interaction
- Encouragement / Social Gesture
- Attention / Warning Gestures
- Collaboration / Cooperative Tasks
- Emotional / Behavioural Tasks

---

## Example use cases

The prototype is intended for sessions involving actions such as:
- passing and receiving objects
- delayed, interrupted, or failed handovers
- lifting, carrying, rotating, or repositioning an object together
- stabilising or supporting a shared object
- physically guiding a partner’s hand
- tapping, pointing, or warning gestures
- cooperative games or shared task actions
- emotionally charged or defensive physical interactions

---

## Output files

The app currently saves responses into two CSV files:

- `social_intention_annotations.csv`  
  Stores researcher annotations from the Annotation Tool tab.

- `post_task_questionnaire_responses.csv`  
  Stores participant responses from the Post-Task Questionnaire tab.

These files can also be downloaded from within the app.

---

## Running the app locally

Install dependencies:

```bash
pip install -r requirements.txt
