UPDATE "{{database}}"."{{schema}}"."{{table}}"
SET UPDATED_JSON = {{updated_json}} WHERE UPLOAD_ID = {{upload_id}};