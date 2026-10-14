# Study Group Formation — Unsupervised Clustering

This submission implements K-Means study-group formation and compares it with Ward Hierarchical Clustering.

## Required outputs included

- `study_group_students.csv` — 60-record dataset.
- `data_dictionary.md` — field roles, descriptions, missing-data and privacy notes.
- `knime_workflow.md` and `knime_workflow_blueprint.json` — expanded KNIME node plan.
- `KNIME_MIDTERM_REQUIREMENT.knwf` —  KNIME workflow archive with the six-feature filter, Normalizer, k-Means seed 42/k=3, Hierarchical branch, and corrected scatter axes.
- `study_group_colab.py` — Python implementation for preparation, K-Means, Hierarchical Clustering, evaluation, and group formation.
- `study_group_clustering.ipynb` — Colab-ready notebook with the Streamlit launcher.
- `streamlit_app.py` — blue/light-blue interface with validation, master list, default mode, and selected-attribute mode.
- `comparison_table.csv` and `comparison_chart.svg` — Part 6 algorithm comparison.



## Two grouping modes

1. Leave **Attributes to match** empty for the default K-Means grouping across the whole dataset.
2. Select attributes and values to require matching students before groups are formed. For example, Programming = 7 and Communication = 5 keeps only students within the configured tolerance of both values. Students who do not match are not added to fill a group.

The selected group size controls the exact number of students per complete group. If there are not enough matching records, the app reports the issue and shows the matching records instead of mixing in unrelated students.

## Colab launch

Upload `study_group_clustering.ipynb` and `study_group_students.csv` to Google Colab, run the data-analysis cell, then run the final Streamlit launcher cell. The launcher prints a direct Colab proxy link.
