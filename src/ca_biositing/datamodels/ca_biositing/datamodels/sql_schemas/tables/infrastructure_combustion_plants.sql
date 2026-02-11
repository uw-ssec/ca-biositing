--
-- Name: infrastructure_combustion_plants; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_combustion_plants (
    combustion_fid SERIAL,
    objectid integer,
    status text,
    city text,
    name text,
    county text,
    equivalent_generation numeric,
    np_mw numeric,
    cf numeric,
    yearload integer,
    fuel text,
    notes text,
    type text,
    wkt_geom text,
    geom text,
    latitude numeric,
    longitude numeric,
    CONSTRAINT infrastructure_combustion_plants_pkey PRIMARY KEY (combustion_fid)
);
