--
-- Name: strain; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS strain (
    parent_strain_id integer,
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT strain_pkey PRIMARY KEY (id)
);
