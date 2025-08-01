#!/bin/bash
# Track start time
START_TIME=$(date +%s)

# Check if tenant_id and password are provided
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <tenant_id> <password>"
  exit 1
fi

TENANT_ID="$1"
PASSWORD="$2"
SQL_FILE="schema.sql"

# Ensure the SQL file exists
if [ ! -f "$SQL_FILE" ]; then
  echo "Error: SQL file '$SQL_FILE' not found!"
  exit 1
fi

# Replace placeholders ':tenant_id' and ':password' with the actual values in the SQL file
sed "s/:tenant_id/$TENANT_ID/g; s/:password/$PASSWORD/g" "$SQL_FILE" | PGPASSWORD="$PASSWORD" psql -h 0.0.0.0 -p 5432 -U postgres

# Track end time
END_TIME=$(date +%s)

# Calculate elapsed time
ELAPSED_TIME=$((END_TIME - START_TIME))

# Output the result
echo "Migration completed for tenant: $TENANT_ID"
echo "Total time taken: $ELAPSED_TIME seconds"
