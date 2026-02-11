--
-- Name: usda_survey_program; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_survey_program (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT usda_survey_program_pkey PRIMARY KEY (id)
);
