import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(page_title="Study Group Formation", page_icon="🔵", layout="wide")
st.html("""
<style>
.stApp { background: #eff6ff; }
h1, h2, h3 { color: #1e3a8a; }
.stButton > button { background: #2563eb; color: white; }
</style>
""")

st.title("🔵 Study Group Formation")
st.caption("K-Means recommendations from study-relevant preferences")

features = [
    "programming", "design", "communication", "analytics",
    "availability_hours", "preferred_group_size"
]
df = pd.read_csv("study_group_students.csv")
label_to_feature = {
    "Programming skill": "programming",
    "Design skill": "design",
    "Communication skill": "communication",
    "Analytics skill": "analytics",
    "Availability (hours/week)": "availability_hours",
    "Preferred group size": "preferred_group_size",
}
with st.sidebar:
    st.header("Student inputs")
    input_values = {
        "programming": st.number_input("Programming skill", 1.0, 10.0, 6.0, step=0.1),
        "design": st.number_input("Design skill", 1.0, 10.0, 6.0, step=0.1),
        "communication": st.number_input("Communication skill", 1.0, 10.0, 6.0, step=0.1),
        "analytics": st.number_input("Analytics skill", 1.0, 10.0, 6.0, step=0.1),
        "availability_hours": st.number_input("Availability (hours/week)", 2.0, 25.0, 10.0, step=0.1),
        "preferred_group_size": st.number_input("Students per formed group", 2, 8, 4),
    }
    selected_labels = st.multiselect(
        "Attributes to match",
        list(label_to_feature),
        default=[],
        help="Selected attributes rank the closest students to your chosen values. All attributes still help K-Means organize the matched students.",
    )
    match_tolerance = st.number_input(
        "Skill matching tolerance",
        0.0,
        2.0,
        0.5,
        step=0.1,
        help="A tolerance of 0.5 matches skill values within ±0.5 of the selected value.",
    )
    if st.button("Find compatible group"):
        requested_size = int(input_values["preferred_group_size"])
        eligible = df.copy()
        for label in selected_labels:
            feature = label_to_feature[label]
            target = input_values[feature]
            if feature == "preferred_group_size":
                eligible = eligible[eligible[feature] == int(target)]
            else:
                tolerance = match_tolerance
                eligible = eligible[(eligible[feature] - target).abs() <= tolerance]
        st.session_state["matching_students"] = eligible.copy()
        full_count = (len(eligible) // requested_size) * requested_size

        if full_count < requested_size:
            st.session_state.pop("formed_groups", None)
            st.session_state["group_error"] = f"Only {len(eligible)} students match the selected attributes. At least {requested_size} matching students are needed. No unrelated students were added."
        else:
            group_count = full_count // requested_size
            eligible = eligible.iloc[:full_count].copy()
            group_base = eligible[features].fillna(eligible[features].median())
            group_scaler = StandardScaler().fit(group_base)
            profile_model = KMeans(
                n_clusters=group_count, random_state=42, n_init=20
            ).fit(group_scaler.transform(group_base))
            distances = profile_model.transform(group_scaler.transform(group_base))
            assignments = np.full(len(eligible), -1, dtype=int)
            capacities = np.full(group_count, requested_size, dtype=int)
            if group_count == 1:
                assignments[:] = 0
            else:
                ordered_distances = np.sort(distances, axis=1)
                margins = ordered_distances[:, 1] - ordered_distances[:, 0]
                assignment_order = np.argsort(-margins)
                for row_index in assignment_order:
                    available_groups = np.flatnonzero(capacities > 0)
                    chosen_group = available_groups[
                        np.argmin(distances[row_index, available_groups])
                    ]
                    assignments[row_index] = chosen_group
                    capacities[chosen_group] -= 1
            eligible["formed_group"] = assignments + 1
            st.session_state["formed_groups"] = eligible
            st.session_state["matched_attributes"] = selected_labels
            st.session_state.pop("group_error", None)
    st.divider()
    if st.button("Students Master List"):
        st.session_state["show_master_list"] = not st.session_state.get(
            "show_master_list", False
        )

if "group_error" in st.session_state:
    st.warning(st.session_state["group_error"])
elif "formed_groups" in st.session_state:
    grouped = st.session_state["formed_groups"]
    requested_size = int(input_values["preferred_group_size"])
    matched_attributes = st.session_state.get("matched_attributes", [])
    st.success(
        f"Formed {grouped['formed_group'].nunique()} complete groups of "
        f"{requested_size} using only students matching the selected attributes."
    )
    st.subheader("Formed study groups")
    st.caption(
        "Each group has the requested size. Hard matching: "
        + (", ".join(matched_attributes) if matched_attributes else "none — all students")
        + ". K-Means uses all available attributes to organize the matched students."
    )
    for group_id in sorted(grouped["formed_group"].unique()):
        group_students = grouped[grouped["formed_group"] == group_id].drop(
            columns=["formed_group"]
        )
        st.markdown(f"### Group {group_id} — {len(group_students)} students")
        st.dataframe(group_students, use_container_width=True, height=240)
else:
    st.info("Set valid inputs and click Find compatible group.")

if "group_error" in st.session_state and "matching_students" in st.session_state:
    st.subheader("Students that matched the selected attributes")
    st.dataframe(st.session_state["matching_students"], use_container_width=True, height=260)

if st.session_state.get("show_master_list", False):
    st.divider()
    st.subheader("Students Master List")
    st.metric("Students in dataset", len(df))
    st.caption(f"All {len(df)} students in the original dataset.")
    st.dataframe(df, use_container_width=True, height=520)
