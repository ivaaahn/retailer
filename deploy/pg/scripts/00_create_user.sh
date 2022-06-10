#!/bin/sh
set -e

POSTGRES="psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}"

echo "Revoking default privileges for public"
$POSTGRES <<-EOSQL
REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON DATABASE ${POSTGRES_DB} FROM PUBLIC;
EOSQL


echo "Creating database role and granting privileges: ${DEFAULT_USER}"
$POSTGRES <<-EOSQL
CREATE USER ${DEFAULT_USER} WITH PASSWORD '${DEFAULT_PSWD}';
GRANT CONNECT ON DATABASE ${POSTGRES_DB} TO ${DEFAULT_USER};
GRANT USAGE ON SCHEMA PUBLIC TO ${DEFAULT_USER};
GRANT ALL ON ALL TABLES IN SCHEMA PUBLIC TO ${DEFAULT_USER};
GRANT ALL ON ALL SEQUENCES IN SCHEMA PUBLIC TO ${DEFAULT_USER};
GRANT ALL ON ALL FUNCTIONS IN SCHEMA PUBLIC TO ${DEFAULT_USER};
EOSQL

echo "Creating database role and granting priveleges: ${ADMIN_USER}"
$POSTGRES <<-EOSQL
CREATE USER ${ADMIN_USER} WITH PASSWORD '${ADMIN_PSWD}';
GRANT ALL ON DATABASE ${POSTGRES_DB} TO ${ADMIN_USER};
GRANT USAGE ON SCHEMA PUBLIC TO ${ADMIN_USER};
GRANT ALL ON ALL TABLES IN SCHEMA PUBLIC TO ${ADMIN_USER};
GRANT ALL ON ALL SEQUENCES IN SCHEMA PUBLIC TO ${ADMIN_USER};
GRANT ALL ON ALL FUNCTIONS IN SCHEMA PUBLIC TO ${ADMIN_USER};
EOSQL

#alter default privileges in schema public grant all on tables to ${DEFAULT_USER};
#alter default privileges in schema public grant all on tables to ${ADMIN_USER};

echo "Altering default privileges for access to future objects..."
$POSTGRES <<-EOSQL
alter default privileges in schema public grant all on sequences to ${DEFAULT_USER};
alter default privileges in schema public grant all on sequences to ${ADMIN_USER};
alter default privileges in schema public grant execute on functions to ${DEFAULT_USER};
alter default privileges in schema public grant execute on functions to ${ADMIN_USER};
EOSQL