--
-- Name: equipment; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS equipment (
    equipment_location_id integer,
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT equipment_pkey PRIMARY KEY (id),
    CONSTRAINT equipment_equipment_location_id_fkey FOREIGN KEY (equipment_location_id) REFERENCES location_address (id)
);
