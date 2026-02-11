--
-- Name: method_category; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS method_category (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT method_category_pkey PRIMARY KEY (id)
);
