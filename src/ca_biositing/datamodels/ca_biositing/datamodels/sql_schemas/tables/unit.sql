--
-- Name: unit; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS unit (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT unit_pkey PRIMARY KEY (id)
);
