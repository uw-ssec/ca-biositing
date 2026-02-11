--
-- Name: usda_domain; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_domain (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT usda_domain_pkey PRIMARY KEY (id)
);
