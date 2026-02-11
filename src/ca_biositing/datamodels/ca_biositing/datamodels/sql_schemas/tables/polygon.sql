--
-- Name: polygon; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS polygon (
    geoid text,
    geom text,
    dataset_id integer,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT polygon_pkey PRIMARY KEY (id),
    CONSTRAINT polygon_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT polygon_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id)
);

--
-- Name: unique_geom_dataset_md5; Type: INDEX; Schema: -; Owner: -
--

CREATE UNIQUE INDEX IF NOT EXISTS unique_geom_dataset_md5 ON polygon (md5(geom), dataset_id);
