--
-- Name: resource; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS resource (
    name text,
    primary_ag_product_id integer,
    resource_class_id integer,
    resource_subclass_id integer,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    resource_code text,
    description text,
    CONSTRAINT resource_pkey PRIMARY KEY (id),
    CONSTRAINT resource_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT resource_primary_ag_product_id_fkey FOREIGN KEY (primary_ag_product_id) REFERENCES primary_ag_product (id),
    CONSTRAINT resource_resource_class_id_fkey FOREIGN KEY (resource_class_id) REFERENCES resource_class (id),
    CONSTRAINT resource_resource_subclass_id_fkey FOREIGN KEY (resource_subclass_id) REFERENCES resource_subclass (id)
);
