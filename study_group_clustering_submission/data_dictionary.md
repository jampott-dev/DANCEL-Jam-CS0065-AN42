# Data dictionary

| Field | Role | Description |
|---|---|---|
| student_id | reference/display | Unique pseudonymous identifier; excluded from modeling. |
| display_name | reference/display | Human-readable label; excluded from modeling. |
| interest_tags | reference/display | Interest tags; excluded from numeric distance calculations. |
| programming, design, communication, analytics | analytical input | Self-rated skill scores, 1–10. |
| availability_hours | analytical input | Weekly availability, 2–25 hours. |
| preferred_group_size | analytical input | Preferred size, 2–8. |
| kmeans_cluster | generated output | K-Means assignment for k=3. |
| hierarchical_cluster | generated output | Ward hierarchical assignment for k=3. |
| formed_group | generated output | Exact-size group number produced after optional attribute matching. |
| match_score / tolerance | interface control | Selected attributes can be required within a configurable tolerance; non-matching students are excluded from formed groups. |

Missing values: none intentionally generated; code validates and imputes numeric missing values with medians. IDs are unique. Use pseudonymous IDs, collect only study-relevant attributes, explain assignments as recommendations, and provide readable validation messages.
