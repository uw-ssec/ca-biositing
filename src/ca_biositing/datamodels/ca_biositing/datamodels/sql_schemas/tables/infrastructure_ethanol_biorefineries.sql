--
-- Name: infrastructure_ethanol_biorefineries; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_ethanol_biorefineries (
    ethanol_biorefinery_id SERIAL,
    name text,
    city text,
    state text,
    address text,
    type text,
    capacity_mgy integer,
    production_mgy integer,
    constr_exp integer,
    CONSTRAINT infrastructure_ethanol_biorefineries_pkey PRIMARY KEY (ethanol_biorefinery_id)
);
