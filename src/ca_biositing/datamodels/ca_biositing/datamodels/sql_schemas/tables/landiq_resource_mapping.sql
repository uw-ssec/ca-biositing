--
-- Name: landiq_resource_mapping; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS landiq_resource_mapping (
    landiq_crop_name integer,
    resource_id integer,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT landiq_resource_mapping_pkey PRIMARY KEY (id),
    CONSTRAINT landiq_resource_mapping_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT landiq_resource_mapping_landiq_crop_name_fkey FOREIGN KEY (landiq_crop_name) REFERENCES primary_ag_product (id),
    CONSTRAINT landiq_resource_mapping_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);
