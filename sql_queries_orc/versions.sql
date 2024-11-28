WITH LatestSnapshots AS (
    SELECT 
        ovs.origin,
        ovs.snapshot_id
    FROM origin_visit_status ovs
    INNER JOIN (
        SELECT origin, MAX(visit) as latest_visit
        FROM origin_visit_status
        WHERE type = 'full'  -- Only consider full visits
        GROUP BY origin
    ) latest ON ovs.origin = latest.origin AND ovs.visit = latest.latest_visit
),
BranchRevisions AS (
    SELECT 
        ls.origin,
        sb.target as revision_id
    FROM LatestSnapshots ls
    INNER JOIN snapshot_branch sb ON ls.snapshot_id = sb.snapshot_id
    WHERE sb.target_type = 'revision'  -- Only consider revision targets
),
CommitCounts AS (
    SELECT 
        o.url as repository_url,
        COUNT(DISTINCT br.revision_id) as commit_count
    FROM origin o
    INNER JOIN BranchRevisions br ON o.url = br.origin
    GROUP BY o.url
)
SELECT 
    repository_url, 
    commit_count 
FROM CommitCounts 
ORDER BY commit_count DESC
LIMIT 100;
