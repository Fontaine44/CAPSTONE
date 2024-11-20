SELECT
    o.id AS repository_id,
    o.url AS repository_url,
    MIN(r.date) AS earliest_commit_date,
    MAX(r.date) AS latest_commit_date,
    DATE_DIFF('day', MIN(r.date), MAX(r.date)) AS days_between_first_and_last_commit
FROM
    origin_parquet AS o
JOIN
    origin_visit_parquet AS ov
    ON o.id = ov.origin
JOIN
    snapshot_branches_parquet AS sbp
    ON ov.snapshot_id = sbp.snapshot_id
JOIN
    snapshot_branch_parquet AS sb
    ON sbp.branch_id = sb.object_id
JOIN
    revision_parquet AS r
    ON sb.target = r.id
WHERE
    sb.target_type = 'revision'
GROUP BY
    o.id, o.url;