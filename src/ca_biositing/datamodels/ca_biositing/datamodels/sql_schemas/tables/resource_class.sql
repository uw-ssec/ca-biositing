--
-- Name: resource_class; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS resource_class (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT resource_class_pkey PRIMARY KEY (id)
);
