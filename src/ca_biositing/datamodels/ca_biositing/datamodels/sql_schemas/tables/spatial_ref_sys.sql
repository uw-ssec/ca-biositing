--
-- Name: spatial_ref_sys; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS spatial_ref_sys (
    srid integer,
    auth_name varchar(256),
    auth_srid integer,
    srtext varchar(2048),
    proj4text varchar(2048),
    CONSTRAINT spatial_ref_sys_pkey PRIMARY KEY (srid),
    CONSTRAINT spatial_ref_sys_srid_check CHECK (srid > 0 AND srid <= 998999)
);
