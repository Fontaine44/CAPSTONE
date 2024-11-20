SELECT
    o.id AS repository_id,
    o.url AS repository_url,
    COUNT(DISTINCT r.author) AS number_of_unique_authors
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
    sb.target_type = 'revision' AND
    r.author IS NOT NULL
GROUP BY
    o.id, o.url;