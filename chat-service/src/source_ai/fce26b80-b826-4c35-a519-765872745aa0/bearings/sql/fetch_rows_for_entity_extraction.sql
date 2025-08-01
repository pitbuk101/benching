SELECT UPLOAD_ID, DATA, CATEGORY, DOCUMENT_TYPE FROM "{{ database }}"."{{ schema }}"."{{ table }}"
WHERE UPLOAD_ID IN ({{ upload_ids_str }})