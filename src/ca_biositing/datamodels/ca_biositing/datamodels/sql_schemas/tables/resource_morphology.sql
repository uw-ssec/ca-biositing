--
-- Name: resource_morphology; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS resource_morphology (
    id SERIAL,
    resource_id integer,
    morphology_uri text,
    CONSTRAINT resource_morphology_pkey PRIMARY KEY (id),
    CONSTRAINT resource_morphology_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);
