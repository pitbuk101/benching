MERGE INTO {{full_table}} AS target
USING (
    SELECT
        {{source_clause}}
) AS source
ON target.UPLOAD_ID = source.UPLOAD_ID

WHEN MATCHED THEN
    UPDATE SET
        {{update_set}}

WHEN NOT MATCHED THEN
    INSERT ({{insert_cols}})
    VALUES ({{insert_vals}});