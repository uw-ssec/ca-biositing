--
-- Name: lookup_base; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS lookup_base (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT lookup_base_pkey PRIMARY KEY (id)
);
