--
-- Contains SQL statements to set up the database.
--

-- noinspection SqlNoDataSourceInspectionForFile
CREATE TABLE detections
(
    id          uuid                     NOT NULL PRIMARY KEY,
    device_name character varying(255)   NOT NULL,
    created_on  timestamp with time zone NOT NULL,
    recorded_on timestamp with time zone NOT NULL,
    min_confidence  double precision     NOT NULL,
    people_in_frame integer              NOT NULL,
    activity character varying(255)      NOT NULL
);

CREATE INDEX CONCURRENTLY recorded_on_index ON detections (recorded_on DESC NULLS LAST);
