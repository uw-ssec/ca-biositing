--
-- Name: usda_commodity; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_commodity (
    usda_source text,
    usda_code text,
    parent_commodity_id integer,
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT usda_commodity_pkey PRIMARY KEY (id),
    CONSTRAINT usda_commodity_parent_commodity_id_fkey FOREIGN KEY (parent_commodity_id) REFERENCES usda_commodity (id)
);
