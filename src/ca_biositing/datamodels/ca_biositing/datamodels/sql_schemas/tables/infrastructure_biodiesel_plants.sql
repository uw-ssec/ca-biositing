--
-- Name: infrastructure_biodiesel_plants; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_biodiesel_plants (
    biodiesel_plant_id SERIAL,
    company text,
    bbi_index integer,
    city text,
    state text,
    capacity_mmg_per_y integer,
    feedstock text,
    status text,
    address text,
    coordinates text,
    latitude numeric,
    longitude numeric,
    source text,
    CONSTRAINT infrastructure_biodiesel_plants_pkey PRIMARY KEY (biodiesel_plant_id)
);
