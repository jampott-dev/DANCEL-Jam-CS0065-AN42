# KNIME workflow — matching and exact-size study groups

This workflow mirrors the website logic. With no attributes selected, it performs the default K-Means grouping across the dataset. When attributes are selected, their target values become hard matching criteria; only matching students can enter a formed group. The selected group size controls the number of students in each formed group.

## Main workflow

```text
CSV Reader → Column Filter → Missing Value → Normalizer → Row Filter
→ k-Means → balanced group assignment → Group Loop / output tables
```

## Node configuration

1. **CSV Reader** — read `study_group_students.csv`; verify numeric types.
2. **Column Filter** — retain `student_id`, `display_name`, and `interest_tags` for display. Use `programming`, `design`, `communication`, `analytics`, `availability_hours`, and `preferred_group_size` as model fields.
3. **Missing Value** — replace numeric missing values with the column median; do not remove the row.
4. **Normalizer** — use Z-score normalization on all six model fields.
5. **Row Filter / Rule Engine** — expose flow variables for the selected target values. If no attribute is selected, keep every row and use the default K-Means grouping. If attributes are selected, keep only rows within the configured tolerance (default ±0.5) for each selected skill; for `preferred_group_size`, keep only an exact match. Do not fill an incomplete group with non-matching students.
6. **Normalizer** — normalize the filtered table for the profile analysis.
7. **k-Means** — use seed `42`; set `k` to `floor(number_of_matching_students / requested_group_size)`.
8. **Balanced assignment** — assign only the filtered rows to the k-Means profiles while enforcing the requested capacity for every group.
9. **Rank** — create a sequential rank after the filtered/profile ordering.
10. **Math Formula** — create the exact-size group number:

   ```text
   formed_group = floor((rank - 1) / requested_group_size) + 1
   ```

   Keep only `floor(n / requested_group_size) * requested_group_size` rows so every group is complete.
11. **Group Loop / Row Splitter** — split rows by `formed_group`; every output table contains exactly the requested number of matching students.
12. **Scatter Plot** — plot `programming` versus `communication` or `design`, color by `formed_group`, and label with `student_id`.
13. **Evaluation** — retain the k-Means silhouette score and compare with Hierarchical Clustering using the same normalized six-field filtered table.

## Example

If the user enters Programming = 7 and Communication = 5, and selects those attributes, KNIME keeps only students within the configured tolerance of both values. If the requested group size is 5, it outputs complete groups of five from those matching students only. If fewer than five match, it reports that no complete group can be formed instead of adding unrelated students.

## Hierarchical comparison

Create a parallel branch:

```text
Normalizer → Hierarchical Clustering (Ward, Euclidean) → Cluster Assigner → Scatter Plot
```

Use the same features and compare silhouette score, group sizes, separation, and interpretation. Hierarchical Clustering remains the comparison method; the matching/ranking branch produces the exact-size groups.
