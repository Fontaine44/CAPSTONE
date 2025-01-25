import streamlit as st
import pyarrow.dataset as ds
import duckdb

def main():

    dataset_root_path = r'../../Dataset'

    with duckdb.connect() as con:
        # Define table names and dataset path
        table_names = [
            "origin",
            "origin_visit_status",
            "snapshot_branch",
            "revision"
        ]

        # Register tables
        for table in table_names:
            dataset_path = f"{dataset_root_path}/{table}"
            con.register(table, ds.dataset(dataset_path, format="orc").to_table())

        st.title("Software Heritage Dataset Analysis")
        st.write("Analyze repository data interactively using your own SQL queries.")

        dataset_root = st.text_input(
            "Enter the path to the dataset root:",
            dataset_root_path,
        )

        if st.button("Load Tables"):
            try:
                # Register tables
                for table in table_names:
                    con.execute(f"DROP VIEW IF EXISTS {table}")
                    dataset_path = f"{dataset_root}/{table}"
                    con.register(table, ds.dataset(dataset_path, format="orc").to_table())
                st.success("Tables successfully loaded!")
            except Exception as e:
                st.error(f"An error occurred while loading tables: {e}")
                return

        # Query input section
        query = st.text_area(
            "Enter your SQL query:",
            value="""SELECT
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
        o.url;""",
            height=200,
        )

        if st.button("Run Query"):
            try:
                # Execute the user query
                results = con.execute(query).arrow()
                results_df = results.to_pandas()

                # Display the results
                st.subheader("Query Results")
                st.dataframe(results_df)

            except Exception as e:
                st.error(f"An error occurred while executing the query: {e}")

if __name__ == "__main__":
    main()
