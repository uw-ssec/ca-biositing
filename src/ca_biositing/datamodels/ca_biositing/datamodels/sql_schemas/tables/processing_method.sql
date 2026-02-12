--
-- Name: processing_method; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS processing_method (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT processing_method_pkey PRIMARY KEY (id)
);
