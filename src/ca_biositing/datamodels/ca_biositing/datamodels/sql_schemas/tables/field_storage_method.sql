--
-- Name: field_storage_method; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS field_storage_method (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT field_storage_method_pkey PRIMARY KEY (id)
);
