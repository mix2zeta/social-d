#!/bin/bash
set -eux

dropdb -U postgres $PGDBNAME || echo "Database $PGDBNAME hasn't created before"

createuser -U postgres -dl $PGUSER || echo "User $PGUSER already exists, skipping"
createdb -U postgres -O $PGUSER $PGDBNAME || echo "Database $PGDBNAME already exists, skipping"
psql -v ON_ERROR_STOP=1 -U postgres -d $PGDBNAME <<-COMM
    ALTER user $PGUSER with encrypted password '$PGPASSWORD';
COMM


psql -v ON_ERROR_STOP=1 -U $PGUSER -d $PGDBNAME <<-MIGG
BEGIN;
`cat /app/schema/001.sql`
COMMIT;
MIGG
