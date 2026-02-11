--
-- Name: method_abbrev; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS method_abbrev (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT method_abbrev_pkey PRIMARY KEY (id)
);
