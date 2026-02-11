--
-- Name: method_standard; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS method_standard (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT method_standard_pkey PRIMARY KEY (id)
);
