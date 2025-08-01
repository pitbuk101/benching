UPDATE "{{ database }}"."{{ schema }}"."{{ table }}" 
SET ENTITY_JSON = {{ entity_json }} 
WHERE UPLOAD_ID = '{{ upload_id }}';