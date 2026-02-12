--
-- Name: resource_subclass; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS resource_subclass (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT resource_subclass_pkey PRIMARY KEY (id)
);
