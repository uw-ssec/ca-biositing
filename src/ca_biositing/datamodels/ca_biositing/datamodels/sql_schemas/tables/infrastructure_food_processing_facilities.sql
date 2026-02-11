--
-- Name: infrastructure_food_processing_facilities; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_food_processing_facilities (
    processing_facility_id SERIAL,
    address text,
    county text,
    city text,
    company text,
    join_count integer,
    master_type text,
    state text,
    subtype text,
    target_fid integer,
    processing_type text,
    zip text,
    type text,
    wkt_geom text,
    geom text,
    latitude numeric,
    longitude numeric,
    CONSTRAINT infrastructure_food_processing_facilities_pkey PRIMARY KEY (processing_facility_id)
);
