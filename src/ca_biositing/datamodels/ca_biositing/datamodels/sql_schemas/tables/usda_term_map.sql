--
-- Name: usda_term_map; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_term_map (
    source_system text,
    source_context text,
    raw_term text,
    usda_commodity_id integer,
    is_verified boolean,
    note text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT usda_term_map_pkey PRIMARY KEY (id),
    CONSTRAINT usda_term_map_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT usda_term_map_usda_commodity_id_fkey FOREIGN KEY (usda_commodity_id) REFERENCES usda_commodity (id)
);
