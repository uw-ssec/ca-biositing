--
-- Name: infrastructure_wastewater_treatment_plants; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_wastewater_treatment_plants (
    plant_id SERIAL,
    name text,
    state text,
    codigestion text,
    flow_design_adjusted numeric,
    flow_average numeric,
    biosolids numeric,
    excess_flow numeric,
    biogas_utilized boolean,
    flaring boolean,
    excess_mass_loading_rate numeric,
    excess_mass_loading_rate_wet numeric,
    methane_production numeric,
    energy_content numeric,
    electric_kw numeric,
    thermal_mmbtu_d numeric,
    electric_kwh numeric,
    thermal_annual_mmbtu_y numeric,
    anaerobic_digestion_facility text,
    county text,
    dayload_bdt numeric,
    dayload numeric,
    equivalent_generation numeric,
    facility_type text,
    feedstock text,
    type text,
    city text,
    latitude numeric,
    longitude numeric,
    zipcode text,
    CONSTRAINT infrastructure_wastewater_treatment_plants_pkey PRIMARY KEY (plant_id)
);
