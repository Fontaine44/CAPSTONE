SELECT
        COUNT(DISTINCT r.committer)
FROM revision as r
LIMIT 10;

-- Count the total number of commit by authors in the revision table
SELECT r.author, COUNT(*) AS nb_commits
FROM revision AS r
GROUP BY r.author;

-- Count the total number of commit by authors in the revision table
SELECT r.author, r.id, COUNT(*) AS nb_commits
FROM revision AS r
GROUP BY r.author, r.id;

SELECT
        o.url AS repository_url,
        r.author,
        r.id
    FROM
        origin AS o
    JOIN
        origin_visit_status AS ov
        ON o.url = ov.origin
    JOIN
        snapshot_branch AS sb
        ON ov.snapshot = sb.snapshot_id
    JOIN
        revision AS r
        ON sb.target = r.id
    WHERE
        sb.target_type = 'revision' AND
        r.author IS NOT NULL
    GROUP BY
        o.url, r.author, r.id;