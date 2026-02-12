--
-- Name: preparation_method_abbreviation; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS preparation_method_abbreviation (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT preparation_method_abbreviation_pkey PRIMARY KEY (id)
);
