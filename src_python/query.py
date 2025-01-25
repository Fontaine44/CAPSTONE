import pyarrow.dataset as ds
import duckdb

with duckdb.connect() as con:

    table_names = [
        "origin",
        "origin_visit_status",
        "snapshot_branch",
        "revision"
    ]

    # Path to the root directory of the dataset
    dataset_root = r'../../Dataset'

    for table in table_names:
        dataset_path = f"{dataset_root}/{table}"
        con.register(table, ds.dataset(dataset_path, format="orc").to_table())

    query = """
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
    ON ov.snapshot = sb.snapshot_id
JOIN
    revision AS r
    ON sb.target = r.id
WHERE
    sb.target_type = 'revision' AND
    r.author IS NOT NULL
GROUP BY
    o.url;
"""

    # # Print schema of origin_visit_status table
    # print(con.execute("SELECT * FROM origin_visit_status LIMIT 1").fetch_arrow_table().schema)
    
    results = con.execute(query).arrow()

    results_df = results.to_pandas()

    print(results_df.head())
    print(results_df.shape)
