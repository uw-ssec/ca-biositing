--
-- Name: collection_method; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS collection_method (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT collection_method_pkey PRIMARY KEY (id)
);
