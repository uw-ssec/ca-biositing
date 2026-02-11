--
-- Name: primary_ag_product; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS primary_ag_product (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT primary_ag_product_pkey PRIMARY KEY (id)
);
