--
-- Name: infrastructure_msw_to_energy_anaerobic_digesters; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_msw_to_energy_anaerobic_digesters (
    wte_id SERIAL,
    city text,
    county text,
    equivalent_generation numeric,
    feedstock text,
    dayload numeric,
    dayload_bdt numeric,
    facility_type text,
    status text,
    notes text,
    source text,
    type text,
    wkt_geom text,
    geom text,
    latitude numeric,
    longitude numeric,
    CONSTRAINT infrastructure_msw_to_energy_anaerobic_digesters_pkey PRIMARY KEY (wte_id)
);
