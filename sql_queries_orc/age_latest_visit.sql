SELECT
    o.url AS repository_url,
    MIN(r.date) AS earliest_commit_date,
    MAX(r.date) AS latest_commit_date,
    DATE_DIFF('day', MIN(r.date), MAX(r.date)) AS days_between_first_and_last_commit
FROM
    origin AS o
JOIN
    (SELECT origin, snapshot_id, MAX(date) as latest_visit_date FROM origin_visit_status GROUP BY origin, snapshot_id) AS ov
    ON o.url = ov.origin
JOIN
    snapshot_branch AS sb
    ON ov.snapshot_id = sb.snapshot_id
JOIN
    revision AS r
    ON sb.target = r.id
WHERE
    sb.target_type = 'revision'
GROUP BY
    o.url;