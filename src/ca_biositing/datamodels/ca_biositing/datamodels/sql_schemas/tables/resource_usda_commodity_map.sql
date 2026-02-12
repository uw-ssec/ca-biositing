--
-- Name: resource_usda_commodity_map; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS resource_usda_commodity_map (
    resource_id integer,
    primary_ag_product_id integer,
    usda_commodity_id integer,
    match_tier text,
    note text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT resource_usda_commodity_map_pkey PRIMARY KEY (id),
    CONSTRAINT resource_usda_commodity_map_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT resource_usda_commodity_map_primary_ag_product_id_fkey FOREIGN KEY (primary_ag_product_id) REFERENCES primary_ag_product (id),
    CONSTRAINT resource_usda_commodity_map_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id),
    CONSTRAINT resource_usda_commodity_map_usda_commodity_id_fkey FOREIGN KEY (usda_commodity_id) REFERENCES usda_commodity (id)
);
