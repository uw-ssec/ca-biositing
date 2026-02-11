--
-- Name: infrastructure_district_energy_systems; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_district_energy_systems (
    des_fid SERIAL,
    cbg_id integer,
    name text,
    system text,
    object_id integer,
    city text,
    state text,
    primary_fuel text,
    secondary_fuel text,
    usetype text,
    cap_st numeric,
    cap_hw numeric,
    cap_cw numeric,
    chpcg_cap numeric,
    excess_c numeric,
    excess_h numeric,
    type text,
    wkt_geom text,
    geom text,
    latitude numeric,
    longitude numeric,
    CONSTRAINT infrastructure_district_energy_systems_pkey PRIMARY KEY (des_fid)
);
