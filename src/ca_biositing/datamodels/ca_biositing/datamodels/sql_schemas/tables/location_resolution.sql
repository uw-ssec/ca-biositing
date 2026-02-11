--
-- Name: location_resolution; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS location_resolution (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT location_resolution_pkey PRIMARY KEY (id)
);
