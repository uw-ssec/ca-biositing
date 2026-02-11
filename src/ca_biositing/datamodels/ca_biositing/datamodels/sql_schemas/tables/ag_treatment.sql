--
-- Name: ag_treatment; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS ag_treatment (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT ag_treatment_pkey PRIMARY KEY (id)
);
