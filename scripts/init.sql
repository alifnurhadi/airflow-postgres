-- Create an additional database for app data
CREATE DATABASE myapp;

-- Create a user for the additional database with privileges
CREATE USER myapp WITH PASSWORD 'myapp';
GRANT ALL PRIVILEGES ON DATABASE myapp TO myapp;
