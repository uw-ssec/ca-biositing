
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()
metadata = Base.metadata


class InfrastructureBiodieselPlants(Base):
    """
    Biodiesel plants infrastructure.
    """
    __tablename__ = 'infrastructure_biodiesel_plants'

    biodiesel_plant_id = Column(Integer(), primary_key=True, nullable=False )
    company = Column(Text())
    bbi_index = Column(Integer())
    city = Column(Text())
    state = Column(Text())
    capacity_mmg_per_y = Column(Integer())
    feedstock = Column(Text())
    status = Column(Text())
    address = Column(Text())
    coordinates = Column(Text())
    latitude = Column(Numeric())
    longitude = Column(Numeric())
    source = Column(Text())


    def __repr__(self):
        return f"InfrastructureBiodieselPlants(biodiesel_plant_id={self.biodiesel_plant_id},company={self.company},bbi_index={self.bbi_index},city={self.city},state={self.state},capacity_mmg_per_y={self.capacity_mmg_per_y},feedstock={self.feedstock},status={self.status},address={self.address},coordinates={self.coordinates},latitude={self.latitude},longitude={self.longitude},source={self.source},)"






class InfrastructureBiosolidsFacilities(Base):
    """
    Biosolids facilities infrastructure.
    """
    __tablename__ = 'infrastructure_biosolids_facilities'

    biosolid_facility_id = Column(Integer(), primary_key=True, nullable=False )
    report_submitted_date = Column(Date())
    latitude = Column(Numeric())
    longitude = Column(Numeric())
    facility = Column(Text())
    authority = Column(Text())
    plant_type = Column(Text())
    aqmd = Column(Text())
    facility_address = Column(Text())
    facility_city = Column(Text())
    state = Column(Text())
    facility_zip = Column(Text())
    facility_county = Column(Text())
    mailing_street_1 = Column(Text())
    mailing_city = Column(Text())
    mailing_state = Column(Text())
    mailing_zip = Column(Text())
    biosolids_number = Column(Text())
    biosolids_contact = Column(Text())
    biosolids_contact_phone = Column(Text())
    biosolids_contact_email = Column(Text())
    adwf = Column(Numeric())
    potw_biosolids_generated = Column(Integer())
    twtds_biosolids_treated = Column(Integer())
    class_b_land_app = Column(Integer())
    class_b_applier = Column(Text())
    class_a_compost = Column(Integer())
    class_a_heat_dried = Column(Integer())
    class_a_other = Column(Integer())
    class_a_other_applier = Column(Text())
    twtds_transfer_to_second_preparer = Column(Integer())
    twtds_second_preparer_name = Column(Text())
    adc_or_final_c = Column(Integer())
    landfill = Column(Integer())
    landfill_name = Column(Text())
    surface_disposal = Column(Integer())
    deepwell_injection = Column(Text())
    stored = Column(Integer())
    longterm_treatment = Column(Integer())
    other = Column(Integer())
    name_of_other = Column(Text())
    incineration = Column(Integer())


    def __repr__(self):
        return f"InfrastructureBiosolidsFacilities(biosolid_facility_id={self.biosolid_facility_id},report_submitted_date={self.report_submitted_date},latitude={self.latitude},longitude={self.longitude},facility={self.facility},authority={self.authority},plant_type={self.plant_type},aqmd={self.aqmd},facility_address={self.facility_address},facility_city={self.facility_city},state={self.state},facility_zip={self.facility_zip},facility_county={self.facility_county},mailing_street_1={self.mailing_street_1},mailing_city={self.mailing_city},mailing_state={self.mailing_state},mailing_zip={self.mailing_zip},biosolids_number={self.biosolids_number},biosolids_contact={self.biosolids_contact},biosolids_contact_phone={self.biosolids_contact_phone},biosolids_contact_email={self.biosolids_contact_email},adwf={self.adwf},potw_biosolids_generated={self.potw_biosolids_generated},twtds_biosolids_treated={self.twtds_biosolids_treated},class_b_land_app={self.class_b_land_app},class_b_applier={self.class_b_applier},class_a_compost={self.class_a_compost},class_a_heat_dried={self.class_a_heat_dried},class_a_other={self.class_a_other},class_a_other_applier={self.class_a_other_applier},twtds_transfer_to_second_preparer={self.twtds_transfer_to_second_preparer},twtds_second_preparer_name={self.twtds_second_preparer_name},adc_or_final_c={self.adc_or_final_c},landfill={self.landfill},landfill_name={self.landfill_name},surface_disposal={self.surface_disposal},deepwell_injection={self.deepwell_injection},stored={self.stored},longterm_treatment={self.longterm_treatment},other={self.other},name_of_other={self.name_of_other},incineration={self.incineration},)"






class InfrastructureCafoManureLocations(Base):
    """
    CAFO manure locations infrastructure.
    """
    __tablename__ = 'infrastructure_cafo_manure_locations'

    cafo_manure_id = Column(Integer(), primary_key=True, nullable=False )
    latitude = Column(Numeric())
    longitude = Column(Numeric())
    owner_name = Column(Text())
    facility_name = Column(Text())
    address = Column(Text())
    town = Column(Text())
    state = Column(Text())
    zip = Column(Text())
    animal = Column(Text())
    animal_feed_operation_type = Column(Text())
    animal_units = Column(Integer())
    animal_count = Column(Integer())
    manure_total_solids = Column(Numeric())
    source = Column(Text())
    date_accessed = Column(Date())


    def __repr__(self):
        return f"InfrastructureCafoManureLocations(cafo_manure_id={self.cafo_manure_id},latitude={self.latitude},longitude={self.longitude},owner_name={self.owner_name},facility_name={self.facility_name},address={self.address},town={self.town},state={self.state},zip={self.zip},animal={self.animal},animal_feed_operation_type={self.animal_feed_operation_type},animal_units={self.animal_units},animal_count={self.animal_count},manure_total_solids={self.manure_total_solids},source={self.source},date_accessed={self.date_accessed},)"






class InfrastructureEthanolBiorefineries(Base):
    """
    Ethanol biorefineries infrastructure.
    """
    __tablename__ = 'infrastructure_ethanol_biorefineries'

    ethanol_biorefinery_id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    city = Column(Text())
    state = Column(Text())
    address = Column(Text())
    type = Column(Text())
    capacity_mgy = Column(Integer())
    production_mgy = Column(Integer())
    constr_exp = Column(Integer())


    def __repr__(self):
        return f"InfrastructureEthanolBiorefineries(ethanol_biorefinery_id={self.ethanol_biorefinery_id},name={self.name},city={self.city},state={self.state},address={self.address},type={self.type},capacity_mgy={self.capacity_mgy},production_mgy={self.production_mgy},constr_exp={self.constr_exp},)"






class InfrastructureLandfills(Base):
    """
    Landfills infrastructure.
    """
    __tablename__ = 'infrastructure_landfills'

    project_id = Column(Text(), primary_key=True, nullable=False )
    project_int_id = Column(Integer())
    ghgrp_id = Column(Text())
    landfill_id = Column(Integer())
    landfill_name = Column(Text())
    state = Column(Text())
    physical_address = Column(Text())
    city = Column(Text())
    county = Column(Text())
    zip_code = Column(Text())
    latitude = Column(Numeric())
    longitude = Column(Numeric())
    ownership_type = Column(Text())
    landfill_owner_orgs = Column(Text())
    landfill_opened_year = Column(Date())
    landfill_closure_year = Column(Date())
    landfill_status = Column(Text())
    waste_in_place = Column(Integer())
    waste_in_place_year = Column(Date())
    lfg_system_in_place = Column(Boolean())
    lfg_collected = Column(Numeric())
    lfg_flared = Column(Numeric())
    project_status = Column(Text())
    project_name = Column(Text())
    project_start_date = Column(Date())
    project_shutdown_date = Column(Date())
    project_type_category = Column(Text())
    lfg_energy_project_type = Column(Text())
    rng_delivery_method = Column(Text())
    actual_mw_generation = Column(Numeric())
    rated_mw_capacity = Column(Numeric())
    lfg_flow_to_project = Column(Numeric())
    direct_emission_reductions = Column(Numeric())
    avoided_emission_reductions = Column(Numeric())


    def __repr__(self):
        return f"InfrastructureLandfills(project_id={self.project_id},project_int_id={self.project_int_id},ghgrp_id={self.ghgrp_id},landfill_id={self.landfill_id},landfill_name={self.landfill_name},state={self.state},physical_address={self.physical_address},city={self.city},county={self.county},zip_code={self.zip_code},latitude={self.latitude},longitude={self.longitude},ownership_type={self.ownership_type},landfill_owner_orgs={self.landfill_owner_orgs},landfill_opened_year={self.landfill_opened_year},landfill_closure_year={self.landfill_closure_year},landfill_status={self.landfill_status},waste_in_place={self.waste_in_place},waste_in_place_year={self.waste_in_place_year},lfg_system_in_place={self.lfg_system_in_place},lfg_collected={self.lfg_collected},lfg_flared={self.lfg_flared},project_status={self.project_status},project_name={self.project_name},project_start_date={self.project_start_date},project_shutdown_date={self.project_shutdown_date},project_type_category={self.project_type_category},lfg_energy_project_type={self.lfg_energy_project_type},rng_delivery_method={self.rng_delivery_method},actual_mw_generation={self.actual_mw_generation},rated_mw_capacity={self.rated_mw_capacity},lfg_flow_to_project={self.lfg_flow_to_project},direct_emission_reductions={self.direct_emission_reductions},avoided_emission_reductions={self.avoided_emission_reductions},)"






class InfrastructureLivestockAnaerobicDigesters(Base):
    """
    Livestock anaerobic digesters infrastructure.
    """
    __tablename__ = 'infrastructure_livestock_anaerobic_digesters'

    digester_id = Column(Integer(), primary_key=True, nullable=False )
    project_name = Column(Text())
    project_type = Column(Text())
    city = Column(Text())
    state = Column(Text())
    digester_type = Column(Text())
    profile = Column(Text())
    year_operational = Column(Date())
    animal_type_class = Column(Text())
    animal_types = Column(Text())
    pop_feeding_digester = Column(Text())
    total_pop_feeding_digester = Column(Integer())
    cattle = Column(Integer())
    dairy = Column(Integer())
    poultry = Column(Integer())
    swine = Column(Integer())
    codigestion = Column(Text())
    biogas_generation_estimate = Column(Integer())
    electricity_generated = Column(Integer())
    biogas_end_uses = Column(Text())
    methane_emission_reductions = Column(Integer())
    latitude = Column(Numeric())
    longitude = Column(Numeric())


    def __repr__(self):
        return f"InfrastructureLivestockAnaerobicDigesters(digester_id={self.digester_id},project_name={self.project_name},project_type={self.project_type},city={self.city},state={self.state},digester_type={self.digester_type},profile={self.profile},year_operational={self.year_operational},animal_type_class={self.animal_type_class},animal_types={self.animal_types},pop_feeding_digester={self.pop_feeding_digester},total_pop_feeding_digester={self.total_pop_feeding_digester},cattle={self.cattle},dairy={self.dairy},poultry={self.poultry},swine={self.swine},codigestion={self.codigestion},biogas_generation_estimate={self.biogas_generation_estimate},electricity_generated={self.electricity_generated},biogas_end_uses={self.biogas_end_uses},methane_emission_reductions={self.methane_emission_reductions},latitude={self.latitude},longitude={self.longitude},)"






class InfrastructureSafAndRenewableDieselPlants(Base):
    """
    SAF and renewable diesel plants infrastructure.
    """
    __tablename__ = 'infrastructure_saf_and_renewable_diesel_plants'

    ibcc_index = Column(Integer(), primary_key=True, nullable=False )
    company = Column(Text())
    city = Column(Text())
    state = Column(Text())
    country = Column(Text())
    capacity = Column(Text())
    feedstock = Column(Text())
    products = Column(Text())
    status = Column(Text())
    address = Column(Text())
    coordinates = Column(Text())
    latitude = Column(Numeric())
    longitude = Column(Numeric())


    def __repr__(self):
        return f"InfrastructureSafAndRenewableDieselPlants(ibcc_index={self.ibcc_index},company={self.company},city={self.city},state={self.state},country={self.country},capacity={self.capacity},feedstock={self.feedstock},products={self.products},status={self.status},address={self.address},coordinates={self.coordinates},latitude={self.latitude},longitude={self.longitude},)"






class InfrastructureWastewaterTreatmentPlants(Base):
    """
    Wastewater treatment plants infrastructure.
    """
    __tablename__ = 'infrastructure_wastewater_treatment_plants'

    plant_id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    state = Column(Text())
    codigestion = Column(Text())
    flow_design_adjusted = Column(Numeric())
    flow_average = Column(Numeric())
    biosolids = Column(Numeric())
    excess_flow = Column(Numeric())
    biogas_utilized = Column(Boolean())
    flaring = Column(Boolean())
    excess_mass_loading_rate = Column(Numeric())
    excess_mass_loading_rate_wet = Column(Numeric())
    methane_production = Column(Numeric())
    energy_content = Column(Numeric())
    electric_kw = Column(Numeric())
    thermal_mmbtu_d = Column(Numeric())
    electric_kwh = Column(Numeric())
    thermal_annual_mmbtu_y = Column(Numeric())
    anaerobic_digestion_facility = Column(Text())
    county = Column(Text())
    dayload_bdt = Column(Numeric())
    dayload = Column(Numeric())
    equivalent_generation = Column(Numeric())
    facility_type = Column(Text())
    feedstock = Column(Text())
    type = Column(Text())
    city = Column(Text())
    latitude = Column(Numeric())
    longitude = Column(Numeric())
    zipcode = Column(Text())


    def __repr__(self):
        return f"InfrastructureWastewaterTreatmentPlants(plant_id={self.plant_id},name={self.name},state={self.state},codigestion={self.codigestion},flow_design_adjusted={self.flow_design_adjusted},flow_average={self.flow_average},biosolids={self.biosolids},excess_flow={self.excess_flow},biogas_utilized={self.biogas_utilized},flaring={self.flaring},excess_mass_loading_rate={self.excess_mass_loading_rate},excess_mass_loading_rate_wet={self.excess_mass_loading_rate_wet},methane_production={self.methane_production},energy_content={self.energy_content},electric_kw={self.electric_kw},thermal_mmbtu_d={self.thermal_mmbtu_d},electric_kwh={self.electric_kwh},thermal_annual_mmbtu_y={self.thermal_annual_mmbtu_y},anaerobic_digestion_facility={self.anaerobic_digestion_facility},county={self.county},dayload_bdt={self.dayload_bdt},dayload={self.dayload},equivalent_generation={self.equivalent_generation},facility_type={self.facility_type},feedstock={self.feedstock},type={self.type},city={self.city},latitude={self.latitude},longitude={self.longitude},zipcode={self.zipcode},)"






class InfrastructureCombustionPlants(Base):
    """
    Combustion plants infrastructure.
    """
    __tablename__ = 'infrastructure_combustion_plants'

    combustion_fid = Column(Integer(), primary_key=True, nullable=False )
    objectid = Column(Integer())
    status = Column(Text())
    city = Column(Text())
    name = Column(Text())
    county = Column(Text())
    equivalent_generation = Column(Numeric())
    np_mw = Column(Numeric())
    cf = Column(Numeric())
    yearload = Column(Integer())
    fuel = Column(Text())
    notes = Column(Text())
    type = Column(Text())
    wkt_geom = Column(Text())
    geom = Column(Text())
    latitude = Column(Numeric())
    longitude = Column(Numeric())


    def __repr__(self):
        return f"InfrastructureCombustionPlants(combustion_fid={self.combustion_fid},objectid={self.objectid},status={self.status},city={self.city},name={self.name},county={self.county},equivalent_generation={self.equivalent_generation},np_mw={self.np_mw},cf={self.cf},yearload={self.yearload},fuel={self.fuel},notes={self.notes},type={self.type},wkt_geom={self.wkt_geom},geom={self.geom},latitude={self.latitude},longitude={self.longitude},)"






class InfrastructureDistrictEnergySystems(Base):
    """
    District energy systems infrastructure.
    """
    __tablename__ = 'infrastructure_district_energy_systems'

    des_fid = Column(Integer(), primary_key=True, nullable=False )
    cbg_id = Column(Integer())
    name = Column(Text())
    system = Column(Text())
    object_id = Column(Integer())
    city = Column(Text())
    state = Column(Text())
    primary_fuel = Column(Text())
    secondary_fuel = Column(Text())
    usetype = Column(Text())
    cap_st = Column(Numeric())
    cap_hw = Column(Numeric())
    cap_cw = Column(Numeric())
    chpcg_cap = Column(Numeric())
    excess_c = Column(Numeric())
    excess_h = Column(Numeric())
    type = Column(Text())
    wkt_geom = Column(Text())
    geom = Column(Text())
    latitude = Column(Numeric())
    longitude = Column(Numeric())


    def __repr__(self):
        return f"InfrastructureDistrictEnergySystems(des_fid={self.des_fid},cbg_id={self.cbg_id},name={self.name},system={self.system},object_id={self.object_id},city={self.city},state={self.state},primary_fuel={self.primary_fuel},secondary_fuel={self.secondary_fuel},usetype={self.usetype},cap_st={self.cap_st},cap_hw={self.cap_hw},cap_cw={self.cap_cw},chpcg_cap={self.chpcg_cap},excess_c={self.excess_c},excess_h={self.excess_h},type={self.type},wkt_geom={self.wkt_geom},geom={self.geom},latitude={self.latitude},longitude={self.longitude},)"






class InfrastructureFoodProcessingFacilities(Base):
    """
    Food processing facilities infrastructure.
    """
    __tablename__ = 'infrastructure_food_processing_facilities'

    processing_facility_id = Column(Integer(), primary_key=True, nullable=False )
    address = Column(Text())
    county = Column(Text())
    city = Column(Text())
    company = Column(Text())
    join_count = Column(Integer())
    master_type = Column(Text())
    state = Column(Text())
    subtype = Column(Text())
    target_fid = Column(Integer())
    processing_type = Column(Text())
    zip = Column(Text())
    type = Column(Text())
    wkt_geom = Column(Text())
    geom = Column(Text())
    latitude = Column(Numeric())
    longitude = Column(Numeric())


    def __repr__(self):
        return f"InfrastructureFoodProcessingFacilities(processing_facility_id={self.processing_facility_id},address={self.address},county={self.county},city={self.city},company={self.company},join_count={self.join_count},master_type={self.master_type},state={self.state},subtype={self.subtype},target_fid={self.target_fid},processing_type={self.processing_type},zip={self.zip},type={self.type},wkt_geom={self.wkt_geom},geom={self.geom},latitude={self.latitude},longitude={self.longitude},)"






class InfrastructureMswToEnergyAnaerobicDigesters(Base):
    """
    MSW to energy anaerobic digesters infrastructure.
    """
    __tablename__ = 'infrastructure_msw_to_energy_anaerobic_digesters'

    wte_id = Column(Integer(), primary_key=True, nullable=False )
    city = Column(Text())
    county = Column(Text())
    equivalent_generation = Column(Numeric())
    feedstock = Column(Text())
    dayload = Column(Numeric())
    dayload_bdt = Column(Numeric())
    facility_type = Column(Text())
    status = Column(Text())
    notes = Column(Text())
    source = Column(Text())
    type = Column(Text())
    wkt_geom = Column(Text())
    geom = Column(Text())
    latitude = Column(Numeric())
    longitude = Column(Numeric())


    def __repr__(self):
        return f"InfrastructureMswToEnergyAnaerobicDigesters(wte_id={self.wte_id},city={self.city},county={self.county},equivalent_generation={self.equivalent_generation},feedstock={self.feedstock},dayload={self.dayload},dayload_bdt={self.dayload_bdt},facility_type={self.facility_type},status={self.status},notes={self.notes},source={self.source},type={self.type},wkt_geom={self.wkt_geom},geom={self.geom},latitude={self.latitude},longitude={self.longitude},)"






class BaseEntity(Base):
    """
    Base entity included in all main entity tables.
    """
    __tablename__ = 'base_entity'

    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"BaseEntity(id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"






class LookupBase(Base):
    """
    Base class for enum/ontology-like tables.
    """
    __tablename__ = 'lookup_base'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"LookupBase(id={self.id},name={self.name},description={self.description},uri={self.uri},)"






class Geography(Base):
    """
    Geographic location.
    """
    __tablename__ = 'geography'

    geoid = Column(Text(), primary_key=True, nullable=False )
    state_name = Column(Text())
    state_fips = Column(Text())
    county_name = Column(Text())
    county_fips = Column(Text())
    region_name = Column(Text())
    agg_level_desc = Column(Text())


    def __repr__(self):
        return f"Geography(geoid={self.geoid},state_name={self.state_name},state_fips={self.state_fips},county_name={self.county_name},county_fips={self.county_fips},region_name={self.region_name},agg_level_desc={self.agg_level_desc},)"






class Contact(Base):
    """
    Contact information for a person.
    """
    __tablename__ = 'contact'

    id = Column(Integer(), primary_key=True, nullable=False )
    first_name = Column(Text())
    last_name = Column(Text())
    email = Column(Text())
    affiliation = Column(Text())


    def __repr__(self):
        return f"Contact(id={self.id},first_name={self.first_name},last_name={self.last_name},email={self.email},affiliation={self.affiliation},)"






class Provider(Base):
    """
    Provider information.
    """
    __tablename__ = 'provider'

    id = Column(Integer(), primary_key=True, nullable=False )
    codename = Column(Text())


    def __repr__(self):
        return f"Provider(id={self.id},codename={self.codename},)"






class ResourceMorphology(Base):
    """
    Morphology of a resource.
    """
    __tablename__ = 'resource_morphology'

    id = Column(Integer(), primary_key=True, nullable=False )
    resource_id = Column(Integer())
    morphology_uri = Column(Text())


    def __repr__(self):
        return f"ResourceMorphology(id={self.id},resource_id={self.resource_id},morphology_uri={self.morphology_uri},)"






class ParameterCategoryParameter(Base):
    """
    Link between Parameter and ParameterCategory.
    """
    __tablename__ = 'parameter_category_parameter'

    id = Column(Integer(), primary_key=True, nullable=False )
    parameter_id = Column(Integer())
    parameter_category_id = Column(Integer())


    def __repr__(self):
        return f"ParameterCategoryParameter(id={self.id},parameter_id={self.parameter_id},parameter_category_id={self.parameter_category_id},)"






class ParameterUnit(Base):
    """
    Link between Parameter and Unit (alternate units).
    """
    __tablename__ = 'parameter_unit'

    id = Column(Integer(), primary_key=True, nullable=False )
    parameter_id = Column(Integer())
    alternate_unit_id = Column(Integer())


    def __repr__(self):
        return f"ParameterUnit(id={self.id},parameter_id={self.parameter_id},alternate_unit_id={self.alternate_unit_id},)"






class FacilityRecord(BaseEntity):
    """
    Facility record.
    """
    __tablename__ = 'facility_record'

    dataset_id = Column(Integer())
    facility_name = Column(Text())
    location_id = Column(Integer())
    capacity_mw = Column(Numeric())
    resource_id = Column(Integer())
    operator = Column(Text())
    start_year = Column(Integer())
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"FacilityRecord(dataset_id={self.dataset_id},facility_name={self.facility_name},location_id={self.location_id},capacity_mw={self.capacity_mw},resource_id={self.resource_id},operator={self.operator},start_year={self.start_year},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class DataSource(BaseEntity):
    """
    Source of data.
    """
    __tablename__ = 'data_source'

    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())
    publication_date = Column(Date())
    version = Column(Text())
    publisher = Column(Text())
    author = Column(Text())
    license = Column(Text())
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"DataSource(name={self.name},description={self.description},uri={self.uri},publication_date={self.publication_date},version={self.version},publisher={self.publisher},author={self.author},license={self.license},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class FileObjectMetadata(BaseEntity):
    """
    Metadata for a file object.
    """
    __tablename__ = 'file_object_metadata'

    data_source_id = Column(Integer())
    bucket_path = Column(Text())
    file_format = Column(Text())
    file_size = Column(Integer())
    checksum_md5 = Column(Text())
    checksum_sha256 = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"FileObjectMetadata(data_source_id={self.data_source_id},bucket_path={self.bucket_path},file_format={self.file_format},file_size={self.file_size},checksum_md5={self.checksum_md5},checksum_sha256={self.checksum_sha256},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class DataSourceType(BaseEntity):
    """
    Type of data source.
    """
    __tablename__ = 'data_source_type'

    source_type_id = Column(Integer())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"DataSourceType(source_type_id={self.source_type_id},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class LocationResolution(LookupBase):
    """
    Resolution of the location (e.g. nation, state, county).
    """
    __tablename__ = 'location_resolution'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"LocationResolution(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class SourceType(LookupBase):
    """
    Type of source (e.g. database, literature).
    """
    __tablename__ = 'source_type'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"SourceType(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class LocationAddress(BaseEntity):
    """
    Physical address.
    """
    __tablename__ = 'location_address'

    geography_id = Column(Text())
    address_line1 = Column(Text())
    address_line2 = Column(Text())
    city = Column(Text())
    zip = Column(Text())
    lat = Column(Float())
    lon = Column(Float())
    is_anonymous = Column(Boolean())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"LocationAddress(geography_id={self.geography_id},address_line1={self.address_line1},address_line2={self.address_line2},city={self.city},zip={self.zip},lat={self.lat},lon={self.lon},is_anonymous={self.is_anonymous},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Resource(BaseEntity):
    """
    Biomass resource definition.
    """
    __tablename__ = 'resource'

    name = Column(Text())
    primary_crop_id = Column(Integer())
    resource_class_id = Column(Integer())
    resource_subclass_id = Column(Integer())
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Resource(name={self.name},primary_crop_id={self.primary_crop_id},resource_class_id={self.resource_class_id},resource_subclass_id={self.resource_subclass_id},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class ResourceClass(LookupBase):
    """
    Classification of resources.
    """
    __tablename__ = 'resource_class'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"ResourceClass(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class ResourceSubclass(LookupBase):
    """
    Sub-classification of resources.
    """
    __tablename__ = 'resource_subclass'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"ResourceSubclass(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class PrimaryCrop(LookupBase):
    """
    Primary crop definition.
    """
    __tablename__ = 'primary_crop'

    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"PrimaryCrop(note={self.note},id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class ResourceAvailability(BaseEntity):
    """
    Availability of a resource in a location.
    """
    __tablename__ = 'resource_availability'

    resource_id = Column(Integer())
    geoid = Column(Text())
    from_month = Column(Integer())
    to_month = Column(Integer())
    year_round = Column(Boolean())
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"ResourceAvailability(resource_id={self.resource_id},geoid={self.geoid},from_month={self.from_month},to_month={self.to_month},year_round={self.year_round},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class ResourceCounterfactual(BaseEntity):
    """
    Counterfactual uses of a resource.
    """
    __tablename__ = 'resource_counterfactual'

    geoid = Column(Text())
    resource_id = Column(Integer())
    counterfactual_description = Column(Text())
    animal_bedding_percent = Column(Numeric())
    animal_bedding_source_id = Column(Integer())
    animal_feed_percent = Column(Numeric())
    animal_feed_source_id = Column(Integer())
    bioelectricty_percent = Column(Numeric())
    bioelectricty_source_id = Column(Integer())
    burn_percent = Column(Numeric())
    burn_source_id = Column(Integer())
    compost_percent = Column(Numeric())
    compost_source_id = Column(Integer())
    landfill_percent = Column(Numeric())
    landfill_source_id = Column(Integer())
    counterfactual_date = Column(Date())
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"ResourceCounterfactual(geoid={self.geoid},resource_id={self.resource_id},counterfactual_description={self.counterfactual_description},animal_bedding_percent={self.animal_bedding_percent},animal_bedding_source_id={self.animal_bedding_source_id},animal_feed_percent={self.animal_feed_percent},animal_feed_source_id={self.animal_feed_source_id},bioelectricty_percent={self.bioelectricty_percent},bioelectricty_source_id={self.bioelectricty_source_id},burn_percent={self.burn_percent},burn_source_id={self.burn_source_id},compost_percent={self.compost_percent},compost_source_id={self.compost_source_id},landfill_percent={self.landfill_percent},landfill_source_id={self.landfill_source_id},counterfactual_date={self.counterfactual_date},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Unit(LookupBase):
    """
    Unit of measurement.
    """
    __tablename__ = 'unit'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"Unit(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Method(BaseEntity):
    """
    Analytical method.
    """
    __tablename__ = 'method'

    name = Column(Text())
    method_abbrev_id = Column(Integer())
    method_category_id = Column(Integer())
    method_standard_id = Column(Integer())
    description = Column(Text())
    detection_limits = Column(Text())
    source_id = Column(Integer())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Method(name={self.name},method_abbrev_id={self.method_abbrev_id},method_category_id={self.method_category_id},method_standard_id={self.method_standard_id},description={self.description},detection_limits={self.detection_limits},source_id={self.source_id},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class MethodAbbrev(LookupBase):
    """
    Abbreviation for method.
    """
    __tablename__ = 'method_abbrev'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"MethodAbbrev(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class MethodCategory(LookupBase):
    """
    Category of method.
    """
    __tablename__ = 'method_category'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"MethodCategory(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class MethodStandard(LookupBase):
    """
    Standard associated with the method.
    """
    __tablename__ = 'method_standard'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"MethodStandard(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Parameter(BaseEntity):
    """
    Parameter being measured.
    """
    __tablename__ = 'parameter'

    name = Column(Text())
    standard_unit_id = Column(Integer())
    calculated = Column(Boolean())
    description = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Parameter(name={self.name},standard_unit_id={self.standard_unit_id},calculated={self.calculated},description={self.description},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class ParameterCategory(LookupBase):
    """
    Category of parameter.
    """
    __tablename__ = 'parameter_category'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"ParameterCategory(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class FieldSample(BaseEntity):
    """
    Sample collected from the field.
    """
    __tablename__ = 'field_sample'

    name = Column(Text())
    resource_id = Column(Integer())
    provider_id = Column(Integer())
    collector_id = Column(Integer())
    sample_collection_source = Column(Text())
    amount_collected = Column(Numeric())
    amount_collected_unit_id = Column(Integer())
    sampling_location_id = Column(Integer())
    field_storage_method_id = Column(Integer())
    field_storage_duration_value = Column(Numeric())
    field_storage_duration_unit_id = Column(Integer())
    field_storage_location_id = Column(Integer())
    collection_timestamp = Column(DateTime())
    collection_method_id = Column(Integer())
    harvest_method_id = Column(Integer())
    harvest_date = Column(Date())
    field_sample_storage_location_id = Column(Integer())
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"FieldSample(name={self.name},resource_id={self.resource_id},provider_id={self.provider_id},collector_id={self.collector_id},sample_collection_source={self.sample_collection_source},amount_collected={self.amount_collected},amount_collected_unit_id={self.amount_collected_unit_id},sampling_location_id={self.sampling_location_id},field_storage_method_id={self.field_storage_method_id},field_storage_duration_value={self.field_storage_duration_value},field_storage_duration_unit_id={self.field_storage_duration_unit_id},field_storage_location_id={self.field_storage_location_id},collection_timestamp={self.collection_timestamp},collection_method_id={self.collection_method_id},harvest_method_id={self.harvest_method_id},harvest_date={self.harvest_date},field_sample_storage_location_id={self.field_sample_storage_location_id},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class FieldStorageMethod(LookupBase):
    """
    Method of field storage.
    """
    __tablename__ = 'field_storage_method'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"FieldStorageMethod(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class CollectionMethod(LookupBase):
    """
    Method of collection.
    """
    __tablename__ = 'collection_method'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"CollectionMethod(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class HarvestMethod(LookupBase):
    """
    Method of harvest.
    """
    __tablename__ = 'harvest_method'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"HarvestMethod(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class ProcessingMethod(LookupBase):
    """
    Method of processing.
    """
    __tablename__ = 'processing_method'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"ProcessingMethod(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class PhysicalCharacteristic(BaseEntity):
    """
    Physical characteristics of a sample.
    """
    __tablename__ = 'physical_characteristic'

    field_sample_id = Column(Integer())
    particle_length = Column(Numeric())
    particle_width = Column(Numeric())
    particle_height = Column(Numeric())
    particle_unit_id = Column(Integer())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"PhysicalCharacteristic(field_sample_id={self.field_sample_id},particle_length={self.particle_length},particle_width={self.particle_width},particle_height={self.particle_height},particle_unit_id={self.particle_unit_id},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class SoilType(LookupBase):
    """
    Type of soil.
    """
    __tablename__ = 'soil_type'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"SoilType(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class AgTreatment(LookupBase):
    """
    Agricultural treatment.
    """
    __tablename__ = 'ag_treatment'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"AgTreatment(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class FieldSampleCondition(BaseEntity):
    """
    Condition of the field sample.
    """
    __tablename__ = 'field_sample_condition'

    field_sample_id = Column(Integer())
    ag_treatment_id = Column(Integer())
    last_application_date = Column(Date())
    treatment_amount_per_acre = Column(Float())
    processing_method_id = Column(Integer())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"FieldSampleCondition(field_sample_id={self.field_sample_id},ag_treatment_id={self.ag_treatment_id},last_application_date={self.last_application_date},treatment_amount_per_acre={self.treatment_amount_per_acre},processing_method_id={self.processing_method_id},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class LocationSoilType(BaseEntity):
    """
    Soil type at a location.
    """
    __tablename__ = 'location_soil_type'

    location_id = Column(Integer())
    soil_type_id = Column(Integer())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"LocationSoilType(location_id={self.location_id},soil_type_id={self.soil_type_id},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class AnalysisType(LookupBase):
    """
    Type of analysis.
    """
    __tablename__ = 'analysis_type'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"AnalysisType(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Dataset(BaseEntity):
    """
    Dataset definition.
    """
    __tablename__ = 'dataset'

    name = Column(Text())
    record_type = Column(Text())
    source_id = Column(Integer())
    start_date = Column(Date())
    end_date = Column(Date())
    description = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Dataset(name={self.name},record_type={self.record_type},source_id={self.source_id},start_date={self.start_date},end_date={self.end_date},description={self.description},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class DimensionType(LookupBase):
    """
    Type of dimension.
    """
    __tablename__ = 'dimension_type'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"DimensionType(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Observation(BaseEntity):
    """
    Observation data.
    """
    __tablename__ = 'observation'

    dataset_id = Column(Integer())
    record_type = Column(Text())
    record_id = Column(Integer())
    parameter_id = Column(Integer())
    value = Column(Numeric())
    unit_id = Column(Integer())
    dimension_type_id = Column(Integer())
    dimension_value = Column(Numeric())
    dimension_unit_id = Column(Integer())
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Observation(dataset_id={self.dataset_id},record_type={self.record_type},record_id={self.record_id},parameter_id={self.parameter_id},value={self.value},unit_id={self.unit_id},dimension_type_id={self.dimension_type_id},dimension_value={self.dimension_value},dimension_unit_id={self.dimension_unit_id},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
