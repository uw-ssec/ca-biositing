--
-- Name: infrastructure_livestock_anaerobic_digesters; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_livestock_anaerobic_digesters (
    digester_id SERIAL,
    project_name text,
    project_type text,
    city text,
    state text,
    digester_type text,
    profile text,
    year_operational date,
    animal_type_class text,
    animal_types text,
    pop_feeding_digester text,
    total_pop_feeding_digester integer,
    cattle integer,
    dairy integer,
    poultry integer,
    swine integer,
    codigestion text,
    biogas_generation_estimate integer,
    electricity_generated integer,
    biogas_end_uses text,
    methane_emission_reductions integer,
    latitude numeric,
    longitude numeric,
    CONSTRAINT infrastructure_livestock_anaerobic_digesters_pkey PRIMARY KEY (digester_id)
);
