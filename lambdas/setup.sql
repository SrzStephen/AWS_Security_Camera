--
-- Contains SQL statements to set up the database.
--

-- noinspection SqlNoDataSourceInspectionForFile
## TODO INSERT STATEMENT
CREATE TABLE data
(
    id          uuid                     NOT NULL PRIMARY KEY,
    device_name character varying(255)   NOT NULL,
);

CREATE INDEX CONCURRENTLY geohash_index ON pothole (geohash ASC NULLS LAST);
CREATE INDEX CONCURRENTLY recorded_on_index ON pothole (recorded_on DESC NULLS LAST);
