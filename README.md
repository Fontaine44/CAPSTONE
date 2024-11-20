# CAPSTONE

In the ORC queries, instead of using the revision tables directly use `(SELECT id, message, author, date, date_offset, date_raw_offset_bytes, directory, type, raw_manifest FROM "orc_python"."revision")` because the columns with "commiter" are broken in the table.