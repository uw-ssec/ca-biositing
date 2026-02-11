--
-- Name: parameter_category; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS parameter_category (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT parameter_category_pkey PRIMARY KEY (id)
);
