SELECT
    o.id AS repository_id,
    o.url AS repository_url,
    COUNT(DISTINCT r.author) AS number_of_unique_authors
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
    sb.target_type = 'revision' AND
    r.author IS NOT NULL
GROUP BY
    o.id, o.url;