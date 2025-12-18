-- Run while connected to the edinburgh_finds database:
-- psql -U postgres -d edinburgh_finds

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

GRANT ALL ON SCHEMA public TO ef_user;
GRANT ALL ON SCHEMA public TO public;
