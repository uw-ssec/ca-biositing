--
-- Name: usda_statistic_category; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_statistic_category (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT usda_statistic_category_pkey PRIMARY KEY (id)
);
