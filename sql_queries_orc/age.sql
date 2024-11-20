SELECT
    o.id AS repository_id,
    o.url AS repository_url,
    MIN(r.date) AS earliest_commit_date,
    MAX(r.date) AS latest_commit_date,
    DATE_DIFF('day', MIN(r.date), MAX(r.date)) AS days_between_first_and_last_commit
FROM
    origin AS o
JOIN
    origin_visit_status AS ov
    ON o.id = ov.origin
JOIN
    snapshot_branch AS sb
    ON ov.snapshot = sb.snapshot_id
JOIN
    (SELECT id, message, author, date, date_offset, date_raw_offset_bytes, directory, type, raw_manifest FROM "orc_python"."revision") AS r
    ON sb.target = r.id
WHERE
    sb.target_type = 'revision'
GROUP BY
    o.id, o.url;