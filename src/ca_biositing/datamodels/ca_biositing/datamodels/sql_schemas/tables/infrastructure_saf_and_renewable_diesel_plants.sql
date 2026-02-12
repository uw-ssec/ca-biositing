--
-- Name: infrastructure_saf_and_renewable_diesel_plants; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_saf_and_renewable_diesel_plants (
    ibcc_index SERIAL,
    company text,
    city text,
    state text,
    country text,
    capacity text,
    feedstock text,
    products text,
    status text,
    address text,
    coordinates text,
    latitude numeric,
    longitude numeric,
    CONSTRAINT infrastructure_saf_and_renewable_diesel_plants_pkey PRIMARY KEY (ibcc_index)
);
