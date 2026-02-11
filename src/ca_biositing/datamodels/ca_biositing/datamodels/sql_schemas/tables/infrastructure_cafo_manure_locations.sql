--
-- Name: infrastructure_cafo_manure_locations; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_cafo_manure_locations (
    cafo_manure_id SERIAL,
    latitude numeric,
    longitude numeric,
    owner_name text,
    facility_name text,
    address text,
    town text,
    state text,
    zip text,
    animal text,
    animal_feed_operation_type text,
    animal_units integer,
    animal_count integer,
    manure_total_solids numeric,
    source text,
    date_accessed date,
    CONSTRAINT infrastructure_cafo_manure_locations_pkey PRIMARY KEY (cafo_manure_id)
);
