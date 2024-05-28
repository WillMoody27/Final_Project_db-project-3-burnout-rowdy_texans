-- CS3810: Principles of Database Systems
-- Instructor: Thyago Mota
-- Student(s): William Hellems-Moody, David Carter
-- Description: burnout database

-- Drop the database if it exists
DROP DATABASE IF EXISTS burnout;
DROP USER IF EXISTS burnout;
-- Remove All Privileges
DROP TABLE IF EXISTS results;
DROP TABLE IF EXISTS surveyees;
DROP TABLE IF EXISTS burnout_questions;
DROP ROLE IF EXISTS burnout;
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM burnout;

-- Create the database
CREATE DATABASE burnout;

-- Connect to the newly created database
\c burnout;

-- Create a user with password along with GRANT privileges
CREATE USER burnout WITH PASSWORD '1234';
-- Grant privileges to the user
-- Grant CREATE privilege on the public schema to user burnout
GRANT ALL PRIVILEGES ON DATABASE burnout TO burnout;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO burnout;
GRANT CREATE ON SCHEMA public TO burnout;

