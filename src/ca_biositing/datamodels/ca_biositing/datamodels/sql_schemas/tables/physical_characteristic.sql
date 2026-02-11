--
-- Name: physical_characteristic; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS physical_characteristic (
    field_sample_id integer,
    particle_length numeric,
    particle_width numeric,
    particle_height numeric,
    particle_unit_id integer,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT physical_characteristic_pkey PRIMARY KEY (id),
    CONSTRAINT physical_characteristic_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT physical_characteristic_field_sample_id_fkey FOREIGN KEY (field_sample_id) REFERENCES field_sample (id),
    CONSTRAINT physical_characteristic_particle_unit_id_fkey FOREIGN KEY (particle_unit_id) REFERENCES unit (id)
);
