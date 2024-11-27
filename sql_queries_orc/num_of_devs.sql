SELECT
    o.url AS repository_url,
    COUNT(DISTINCT r.author) AS number_of_unique_authors
FROM
    origin AS o
JOIN
    origin_visit_status AS ov
    ON o.url = ov.origin
JOIN
    snapshot_branch AS sb
    ON ov.snapshot_id = sb.snapshot_id
JOIN
    revision AS r
    ON sb.target = r.id
WHERE
    sb.target_type = 'revision' AND
    r.author IS NOT NULL
GROUP BY
    o.url;