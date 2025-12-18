-- ============================================================
-- Edinburgh Finds – Initial Database Setup Script
-- Run once on a new machine or new PostgreSQL install.
--
-- IMPORTANT:
-- Replace <YOUR_PASSWORD_HERE> before running.
--
-- Execute using:
--   psql -U postgres -f scripts/create_database.sql
-- ============================================================

-- 1) Create a dedicated application role (database user)
-- This user will be used by your Python application.
CREATE ROLE ef_user LOGIN PASSWORD 'Fifteen!5e';

-- 2) Create the main application database
-- Using template0 ensures a clean Unicode + UK locale database.
CREATE DATABASE edinburgh_finds
    OWNER ef_user
    ENCODING 'UTF8'
    LC_COLLATE 'en_GB.UTF-8'
    LC_CTYPE 'en_GB.UTF-8'
    TEMPLATE template0;

-- (Optional but recommended)
-- 3) Grant privileges explicitly (safeguard correctness)
GRANT ALL PRIVILEGES ON DATABASE edinburgh_finds TO ef_user;

-- ============================================================
-- Done.
-- Connect from your app using:
--   postgresql://edf_user:<YOUR_PASSWORD_HERE>@localhost:5432/edinburgh_finds
-- ============================================================
