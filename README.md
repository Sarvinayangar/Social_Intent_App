# Social_Intent_App
# Social Intention Annotation Tool

This project is a Streamlit-based annotation tool for recording the **social intention associated with an observed action** in human-human interaction tasks.

The aim is to replace free-text descriptors with a structured annotation interface so that actions and their social meaning can be labelled more consistently and analysed more easily.

## Purpose

The tool is designed for human interaction data collected in collaborative and social scenarios. It supports annotation of:

- the **observed action**
- the **action category**
- the **high-level social intention**
- the **tactile-specific intention**
- the **audio context**
- the **role-based label**
- annotator/trial metadata
- confidence and notes

The taxonomy used in the app is based on project notes covering collaborative tasks, handovers, object manipulation, force conflict, physical guidance, encouragement, and warning gestures, alongside social-intention categories such as affiliative, instructional, avoidant/defensive, and cooperative/symmetrical. :contentReference[oaicite:0]{index=0}

## Current annotation structure

### Action categories
- Object Manipulation Interaction
- Load Transfer Interaction
- Force Conflict Interaction
- Physical Guidance Interaction
- Encouragement / Social Gesture
- Attention / Warning Gestures :contentReference[oaicite:1]{index=1}

### High-level social intention
- Affiliative
- Dominant / Assertive
- Instructional
- Avoidant / Defensive
- Cooperative / Symmetrical :contentReference[oaicite:2]{index=2}

### Tactile-specific intention
- Supportive
- Coercive
- Hesitant
- Consoling
- Struggle :contentReference[oaicite:3]{index=3}

### Additional contextual labels
- Audio context
- Role-based label
- Confidence
- Notes :contentReference[oaicite:4]{index=4}

## Example use cases

Example scenarios include:
- passing and receiving objects
- delayed or failed handovers
- lifting or carrying objects together
- rotating or repositioning shared objects
- physically guiding another person’s hand
- signalling attention or warning through gesture or touch 

## Output

Annotations are currently saved to a CSV file:

`social_intention_annotations.csv`

This allows annotations to be reviewed in the app and downloaded for later analysis.

## Running the app locally

Install dependencies:

```bash
pip install -r requirements.txt
