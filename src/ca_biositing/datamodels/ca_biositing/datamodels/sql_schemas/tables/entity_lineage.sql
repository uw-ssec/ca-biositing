--
-- Name: entity_lineage; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS entity_lineage (
    id SERIAL,
    lineage_group_id integer,
    source_table text,
    source_row_id text,
    note text,
    CONSTRAINT entity_lineage_pkey PRIMARY KEY (id)
);
