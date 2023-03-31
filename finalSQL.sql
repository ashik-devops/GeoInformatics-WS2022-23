CREATE ROLE env_master WITH
	LOGIN
	SUPERUSER
	CREATEDB
	CREATEROLE
	INHERIT
	NOREPLICATION
	CONNECTION LIMIT -1
	PASSWORD 'M123xyz';

COMMENT ON ROLE env_master IS 'Superuser of the env_db database.';

/* Standard user for the env_db database */

CREATE ROLE env_user WITH
	LOGIN
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	INHERIT
	NOREPLICATION
	CONNECTION LIMIT -1
	PASSWORD 'U123xyz';
	
COMMENT ON ROLE env_user IS 'Standard user of the env_db database.';

CREATE DATABASE env_groundwater
    WITH 
    OWNER = env_master
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE env_db IS 'Environmental database.';

CREATE TABLE public."Masterdata"
(
    id SERIAL PRIMARY KEY,
    Stammdaten varchar(264),
    Pegelnummer varchar(128),
    Gewässer varchar(64) NULL,
    Flusskilometer decimal(10, 2) NULL,
    Pegelnullpunkt decimal(10, 2) NULL,
    Einzugsgebiet decimal(10, 2) NULL,
    Rechtswert decimal(10, 2) NULL,
    Hochwert decimal(10, 2) NULL,
    MHW decimal(10, 2) NULL,
    MW decimal(10, 2) NULL,
    MNW decimal(10, 2) NULL,
    filepath varchar(128),
)



CREATE TABLE public."Waterlevel"
(
    Sid varchar(32),
    Pegelnummer varchar(128),
    Place varchar(128),
    Timestamp TIMESTAMP WITHOUT TIME ZONE,
    Water_level decimal(10, 2) NULL,
    Discharge varchar(64) NULL
)
