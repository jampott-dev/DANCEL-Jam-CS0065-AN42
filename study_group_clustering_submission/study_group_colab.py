import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score

FEATURES = ["programming", "design", "communication", "analytics", "availability_hours", "preferred_group_size"]
df = pd.read_csv("study_group_students.csv")
assert df["student_id"].is_unique
X = df[FEATURES].fillna(df[FEATURES].median())
X_scaled = StandardScaler().fit_transform(X)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=20)
df["kmeans_cluster"] = kmeans.fit_predict(X_scaled) + 1
hierarchical = AgglomerativeClustering(n_clusters=3, linkage="ward")
df["hierarchical_cluster"] = hierarchical.fit_predict(X_scaled) + 1
comparison = pd.DataFrame({"method":["K-Means","Hierarchical"], "silhouette":[silhouette_score(X_scaled, kmeans.labels_), silhouette_score(X_scaled, hierarchical.labels_)]})
print(comparison.round(3))
df.to_csv("study_group_students_clustered.csv", index=False)


def form_study_groups(data, requested_group_size, targets=None,
                      selected_attributes=None, tolerance=0.5):
    """Form exact-size groups using the same two modes as the Streamlit app.

    With no selected attributes, all rows are eligible. With selected attributes,
    rows must fall within the tolerance of every selected target; non-matching
    rows are never added to complete a group.
    """
    selected_attributes = selected_attributes or []
    targets = targets or {}
    eligible = data.copy()
    for feature in selected_attributes:
        target = targets[feature]
        if feature == "preferred_group_size":
            eligible = eligible[eligible[feature] == int(target)]
        else:
            eligible = eligible[(eligible[feature] - target).abs() <= tolerance]

    complete_count = (len(eligible) // requested_group_size) * requested_group_size
    if complete_count < requested_group_size:
        return eligible.assign(formed_group=pd.Series(dtype="Int64")), {
            "complete": False,
            "matching_students": len(eligible),
        }

    eligible = eligible.iloc[:complete_count].copy()
    group_count = complete_count // requested_group_size
    group_X = eligible[FEATURES].fillna(eligible[FEATURES].median())
    group_scaled = StandardScaler().fit_transform(group_X)
    group_model = KMeans(n_clusters=group_count, random_state=42, n_init=20)
    labels = group_model.fit_predict(group_scaled)
    distances = group_model.transform(group_scaled)
    capacities = np.full(group_count, requested_group_size, dtype=int)
    assignments = np.full(len(eligible), -1, dtype=int)
    if group_count == 1:
        assignments[:] = 0
    else:
        ordered = np.sort(distances, axis=1)
        confidence = ordered[:, 1] - ordered[:, 0]
        for row_index in np.argsort(-confidence):
            available = np.flatnonzero(capacities > 0)
            chosen = available[np.argmin(distances[row_index, available])]
            assignments[row_index] = chosen
            capacities[chosen] -= 1
    eligible["formed_group"] = assignments + 1
    return eligible, {"complete": True, "matching_students": len(eligible)}
