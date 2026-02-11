--
-- Name: place; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS place (
    geoid text,
    state_name text,
    state_fips text,
    county_name text,
    county_fips text,
    region_name text,
    agg_level_desc text,
    CONSTRAINT place_pkey PRIMARY KEY (geoid)
);
