from ...database import Base

from ...database import Base


from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.ext.associationproxy import association_proxy

metadata = Base.metadata


class BaseEntity(Base):
    """
    Base entity included in all main entity tables.
    """
    __tablename__ = 'base_entity'

    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
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






class ExperimentAnalysis(Base):
    """
    Link between Experiment and AnalysisType.
    """
    __tablename__ = 'experiment_analysis'

    id = Column(Integer(), primary_key=True, nullable=False )
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    analysis_type_id = Column(Integer(), ForeignKey('analysis_type.id'))


    def __repr__(self):
        return f"ExperimentAnalysis(id={self.id},experiment_id={self.experiment_id},analysis_type_id={self.analysis_type_id},)"






class ExperimentEquipment(Base):
    """
    Link between Experiment and Equipment.
    """
    __tablename__ = 'experiment_equipment'

    id = Column(Integer(), primary_key=True, nullable=False )
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    equipment_id = Column(Integer(), ForeignKey('equipment.id'))


    def __repr__(self):
        return f"ExperimentEquipment(id={self.id},experiment_id={self.experiment_id},equipment_id={self.equipment_id},)"






class ExperimentMethod(Base):
    """
    Link between Experiment and Method.
    """
    __tablename__ = 'experiment_method'

    id = Column(Integer(), primary_key=True, nullable=False )
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    method_id = Column(Integer(), ForeignKey('method.id'))


    def __repr__(self):
        return f"ExperimentMethod(id={self.id},experiment_id={self.experiment_id},method_id={self.method_id},)"






class ExperimentPreparedSample(Base):
    """
    Link between Experiment and PreparedSample.
    """
    __tablename__ = 'experiment_prepared_sample'

    id = Column(Integer(), primary_key=True, nullable=False )
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    prepared_sample_id = Column(Integer(), ForeignKey('prepared_sample.id'))


    def __repr__(self):
        return f"ExperimentPreparedSample(id={self.id},experiment_id={self.experiment_id},prepared_sample_id={self.prepared_sample_id},)"






class Place(Base):
    """
    Geographic location.
    """
    __tablename__ = 'place'

    geoid = Column(Text(), primary_key=True, nullable=False )
    state_name = Column(Text())
    state_fips = Column(Text())
    county_name = Column(Text())
    county_fips = Column(Text())
    region_name = Column(Text())
    agg_level_desc = Column(Text())


    def __repr__(self):
        return f"Place(geoid={self.geoid},state_name={self.state_name},state_fips={self.state_fips},county_name={self.county_name},county_fips={self.county_fips},region_name={self.region_name},agg_level_desc={self.agg_level_desc},)"






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






class LineageGroup(Base):
    """
    Grouping for lineage information.
    """
    __tablename__ = 'lineage_group'

    id = Column(Integer(), primary_key=True, nullable=False )
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    note = Column(Text())


    def __repr__(self):
        return f"LineageGroup(id={self.id},etl_run_id={self.etl_run_id},note={self.note},)"






class EntityLineage(Base):
    """
    Lineage information for a specific entity.
    """
    __tablename__ = 'entity_lineage'

    id = Column(Integer(), primary_key=True, nullable=False )
    lineage_group_id = Column(Integer())
    source_table = Column(Text())
    source_row_id = Column(Text())
    note = Column(Text())


    def __repr__(self):
        return f"EntityLineage(id={self.id},lineage_group_id={self.lineage_group_id},source_table={self.source_table},source_row_id={self.source_row_id},note={self.note},)"






class EtlRun(Base):
    """
    Information about an ETL run.
    """
    __tablename__ = 'etl_run'

    id = Column(Integer(), primary_key=True, nullable=False )
    run_id = Column(Text())
    started_at = Column(DateTime())
    completed_at = Column(DateTime())
    pipeline_name = Column(Text())
    status = Column(Text())
    records_ingested = Column(Integer())
    note = Column(Text())


    def __repr__(self):
        return f"EtlRun(id={self.id},run_id={self.run_id},started_at={self.started_at},completed_at={self.completed_at},pipeline_name={self.pipeline_name},status={self.status},records_ingested={self.records_ingested},note={self.note},)"






class ParameterCategoryParameter(Base):
    """
    Link between Parameter and ParameterCategory.
    """
    __tablename__ = 'parameter_category_parameter'

    id = Column(Integer(), primary_key=True, nullable=False )
    parameter_id = Column(Integer(), ForeignKey('parameter.id'))
    parameter_category_id = Column(Integer(), ForeignKey('parameter_category.id'))


    def __repr__(self):
        return f"ParameterCategoryParameter(id={self.id},parameter_id={self.parameter_id},parameter_category_id={self.parameter_category_id},)"






class ParameterUnit(Base):
    """
    Link between Parameter and Unit (alternate units).
    """
    __tablename__ = 'parameter_unit'

    id = Column(Integer(), primary_key=True, nullable=False )
    parameter_id = Column(Integer(), ForeignKey('parameter.id'))
    alternate_unit_id = Column(Integer(), ForeignKey('unit.id'))


    def __repr__(self):
        return f"ParameterUnit(id={self.id},parameter_id={self.parameter_id},alternate_unit_id={self.alternate_unit_id},)"






class ResourceMorphology(Base):
    """
    Morphology of a resource.
    """
    __tablename__ = 'resource_morphology'

    id = Column(Integer(), primary_key=True, nullable=False )
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    morphology_uri = Column(Text())


    def __repr__(self):
        return f"ResourceMorphology(id={self.id},resource_id={self.resource_id},morphology_uri={self.morphology_uri},)"






class DataSource(BaseEntity):
    """
    Source of data.
    """
    __tablename__ = 'data_source'

    name = Column(Text())
    description = Column(Text())
    data_source_type_id = Column(Integer(), ForeignKey('data_source_type.id'))
    full_title = Column(Text())
    creator = Column(Text())
    subject = Column(Text())
    publisher = Column(Text())
    contributor = Column(Text())
    date = Column(DateTime())
    type = Column(Text())
    biocirv = Column(Boolean())
    format = Column(Text())
    language = Column(Text())
    relation = Column(Text())
    temporal_coverage = Column(Text())
    location_coverage_id = Column(Integer(), ForeignKey('location_resolution.id'))
    rights = Column(Text())
    license = Column(Text())
    uri = Column(Text())
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"DataSource(name={self.name},description={self.description},data_source_type_id={self.data_source_type_id},full_title={self.full_title},creator={self.creator},subject={self.subject},publisher={self.publisher},contributor={self.contributor},date={self.date},type={self.type},biocirv={self.biocirv},format={self.format},language={self.language},relation={self.relation},temporal_coverage={self.temporal_coverage},location_coverage_id={self.location_coverage_id},rights={self.rights},license={self.license},uri={self.uri},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class DataSourceType(BaseEntity):
    """
    Type of data source (e.g. database, literature).
    """
    __tablename__ = 'data_source_type'

    source_type_id = Column(Integer(), ForeignKey('source_type.id'))
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"DataSourceType(source_type_id={self.source_type_id},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class FileObjectMetadata(BaseEntity):
    """
    Metadata for a file object.
    """
    __tablename__ = 'file_object_metadata'

    data_source_id = Column(Integer(), ForeignKey('data_source.id'))
    bucket_path = Column(Text())
    file_format = Column(Text())
    file_size = Column(Integer())
    checksum_md5 = Column(Text())
    checksum_sha256 = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"FileObjectMetadata(data_source_id={self.data_source_id},bucket_path={self.bucket_path},file_format={self.file_format},file_size={self.file_size},checksum_md5={self.checksum_md5},checksum_sha256={self.checksum_sha256},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




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



class Equipment(LookupBase):
    """
    Equipment used in experiments.
    """
    __tablename__ = 'equipment'

    equipment_location_id = Column(Integer(), ForeignKey('location_address.id'))
    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"Equipment(equipment_location_id={self.equipment_location_id},id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Experiment(BaseEntity):
    """
    Experiment definition.
    """
    __tablename__ = 'experiment'

    analyst_id = Column(Integer(), ForeignKey('contact.id'))
    exper_start_date = Column(Date())
    exper_duration = Column(Numeric())
    exper_duration_unit_id = Column(Integer(), ForeignKey('unit.id'))
    exper_location_id = Column(Integer(), ForeignKey('location_address.id'))
    description = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Experiment(analyst_id={self.analyst_id},exper_start_date={self.exper_start_date},exper_duration={self.exper_duration},exper_duration_unit_id={self.exper_duration_unit_id},exper_location_id={self.exper_location_id},description={self.description},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




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



class Method(BaseEntity):
    """
    method.
    """
    __tablename__ = 'method'

    name = Column(Text())
    method_abbrev_id = Column(Integer(), ForeignKey('method_abbrev.id'))
    method_category_id = Column(Integer(), ForeignKey('method_category.id'))
    method_standard_id = Column(Integer(), ForeignKey('method_standard.id'))
    description = Column(Text())
    detection_limits = Column(Text())
    source_id = Column(Integer(), ForeignKey('data_source.id'))
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Method(name={self.name},method_abbrev_id={self.method_abbrev_id},method_category_id={self.method_category_id},method_standard_id={self.method_standard_id},description={self.description},detection_limits={self.detection_limits},source_id={self.source_id},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class PreparedSample(BaseEntity):
    """
    Sample that has been prepared.
    """
    __tablename__ = 'prepared_sample'

    name = Column(Text())
    field_sample_id = Column(Integer(), ForeignKey('field_sample.id'))
    prep_method_id = Column(Integer(), ForeignKey('preparation_method.id'))
    prep_date = Column(Date())
    preparer_id = Column(Integer(), ForeignKey('contact.id'))
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"PreparedSample(name={self.name},field_sample_id={self.field_sample_id},prep_method_id={self.prep_method_id},prep_date={self.prep_date},preparer_id={self.preparer_id},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




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
    primary_ag_product_id = Column(Integer(), ForeignKey('primary_ag_product.id'))
    resource_class_id = Column(Integer(), ForeignKey('resource_class.id'))
    resource_subclass_id = Column(Integer(), ForeignKey('resource_subclass.id'))
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Resource(name={self.name},primary_ag_product_id={self.primary_ag_product_id},resource_class_id={self.resource_class_id},resource_subclass_id={self.resource_subclass_id},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




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



class BillionTon2023Record(BaseEntity):
    """
    Billion Ton 2023 record.
    """
    __tablename__ = 'billion_ton2023_record'

    subclass_id = Column(Integer(), ForeignKey('resource_subclass.id'))
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    geoid = Column(Text())
    county_square_miles = Column(Float())
    model_name = Column(Text())
    scenario_name = Column(Text())
    price_offered_usd = Column(Numeric())
    production = Column(Integer())
    production_unit_id = Column(Integer(), ForeignKey('unit.id'))
    btu_ton = Column(Integer())
    production_energy_content = Column(Integer())
    energy_content_unit_id = Column(Integer(), ForeignKey('unit.id'))
    product_density_dtpersqmi = Column(Numeric())
    land_source = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"BillionTon2023Record(subclass_id={self.subclass_id},resource_id={self.resource_id},geoid={self.geoid},county_square_miles={self.county_square_miles},model_name={self.model_name},scenario_name={self.scenario_name},price_offered_usd={self.price_offered_usd},production={self.production},production_unit_id={self.production_unit_id},btu_ton={self.btu_ton},production_energy_content={self.production_energy_content},energy_content_unit_id={self.energy_content_unit_id},product_density_dtpersqmi={self.product_density_dtpersqmi},land_source={self.land_source},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




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
    source_id = Column(Integer(), ForeignKey('data_source.id'))
    start_date = Column(Date())
    end_date = Column(Date())
    description = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Dataset(name={self.name},record_type={self.record_type},source_id={self.source_id},start_date={self.start_date},end_date={self.end_date},description={self.description},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Polygon(BaseEntity):
    """
    Geospatial polygon.
    """
    __tablename__ = 'polygon'

    geoid = Column(Text())
    geom = Column(Text())
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Polygon(geoid={self.geoid},geom={self.geom},dataset_id={self.dataset_id},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class PrimaryAgProduct(LookupBase):
    """
    Primary agricultural product definition.
    """
    __tablename__ = 'primary_ag_product'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"PrimaryAgProduct(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class LandiqRecord(BaseEntity):
    """
    LandIQ record.
    """
    __tablename__ = 'landiq_record'

    record_id = Column(Text(), primary_key=True, nullable=False )
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    polygon_id = Column(Integer(), ForeignKey('polygon.id'))
    main_crop = Column(Integer(), ForeignKey('primary_ag_product.id'))
    secondary_crop = Column(Integer(), ForeignKey('primary_ag_product.id'))
    tertiary_crop = Column(Integer(), ForeignKey('primary_ag_product.id'))
    quaternary_crop = Column(Integer(), ForeignKey('primary_ag_product.id'))
    confidence = Column(Integer())
    irrigated = Column(Boolean())
    acres = Column(Float())
    version = Column(Text())
    note = Column(Text())
    pct1 = Column(Float())
    pct2 = Column(Float())
    pct3 = Column(Float())
    pct4 = Column(Float())
    id = Column(Integer(), nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"LandiqRecord(record_id={self.record_id},dataset_id={self.dataset_id},polygon_id={self.polygon_id},main_crop={self.main_crop},secondary_crop={self.secondary_crop},tertiary_crop={self.tertiary_crop},quaternary_crop={self.quaternary_crop},confidence={self.confidence},irrigated={self.irrigated},acres={self.acres},version={self.version},note={self.note},pct1={self.pct1},pct2={self.pct2},pct3={self.pct3},pct4={self.pct4},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class UsdaCommodity(LookupBase):
    """
    USDA commodity.
    """
    __tablename__ = 'usda_commodity'

    usda_source = Column(Text())
    usda_code = Column(Text())
    parent_commodity_id = Column(Integer(), ForeignKey('usda_commodity.id'))
    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"UsdaCommodity(usda_source={self.usda_source},usda_code={self.usda_code},parent_commodity_id={self.parent_commodity_id},id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class ResourceUsdaCommodityMap(BaseEntity):
    """
    Mapping between resources/crops and USDA commodities.
    """
    __tablename__ = 'resource_usda_commodity_map'

    resource_id = Column(Integer(), ForeignKey('resource.id'))
    primary_ag_product_id = Column(Integer(), ForeignKey('primary_ag_product.id'))
    usda_commodity_id = Column(Integer(), ForeignKey('usda_commodity.id'))
    match_tier = Column(Text())
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"ResourceUsdaCommodityMap(resource_id={self.resource_id},primary_ag_product_id={self.primary_ag_product_id},usda_commodity_id={self.usda_commodity_id},match_tier={self.match_tier},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class UsdaCensusRecord(BaseEntity):
    """
    USDA census record.
    """
    __tablename__ = 'usda_census_record'

    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    geoid = Column(Text())
    commodity_code = Column(Integer(), ForeignKey('usda_commodity.id'))
    year = Column(Integer())
    source_reference = Column(Text())
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"UsdaCensusRecord(dataset_id={self.dataset_id},geoid={self.geoid},commodity_code={self.commodity_code},year={self.year},source_reference={self.source_reference},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class UsdaDomain(LookupBase):
    """
    USDA domain.
    """
    __tablename__ = 'usda_domain'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"UsdaDomain(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class UsdaMarketReport(BaseEntity):
    """
    USDA market report.
    """
    __tablename__ = 'usda_market_report'

    slug_id = Column(Integer())
    slug_name = Column(Text())
    report_series_title = Column(Text())
    frequency = Column(Text())
    office_name = Column(Text())
    office_city_id = Column(Integer(), ForeignKey('location_address.id'))
    office_state_fips = Column(Text())
    source_id = Column(Integer(), ForeignKey('data_source.id'))
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"UsdaMarketReport(slug_id={self.slug_id},slug_name={self.slug_name},report_series_title={self.report_series_title},frequency={self.frequency},office_name={self.office_name},office_city_id={self.office_city_id},office_state_fips={self.office_state_fips},source_id={self.source_id},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class UsdaMarketRecord(BaseEntity):
    """
    USDA market record.
    """
    __tablename__ = 'usda_market_record'

    report_id = Column(Integer(), ForeignKey('usda_market_report.id'))
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    report_begin_date = Column(DateTime())
    report_end_date = Column(DateTime())
    report_date = Column(DateTime())
    commodity_id = Column(Integer(), ForeignKey('usda_commodity.id'))
    market_type_id = Column(Integer())
    market_type_category = Column(Text())
    grp = Column(Text())
    market_category_id = Column(Integer())
    class_ = Column(Text())
    grade = Column(Text())
    variety = Column(Text())
    protein_pct = Column(Numeric())
    application = Column(Text())
    pkg = Column(Text())
    sale_type = Column(Text())
    price_unit_id = Column(Integer(), ForeignKey('unit.id'))
    freight = Column(Text())
    trans_mode = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"UsdaMarketRecord(report_id={self.report_id},dataset_id={self.dataset_id},report_begin_date={self.report_begin_date},report_end_date={self.report_end_date},report_date={self.report_date},commodity_id={self.commodity_id},market_type_id={self.market_type_id},market_type_category={self.market_type_category},grp={self.grp},market_category_id={self.market_category_id},class_={self.class_},grade={self.grade},variety={self.variety},protein_pct={self.protein_pct},application={self.application},pkg={self.pkg},sale_type={self.sale_type},price_unit_id={self.price_unit_id},freight={self.freight},trans_mode={self.trans_mode},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class LocationAddress(BaseEntity):
    """
    Physical address.
    """
    __tablename__ = 'location_address'

    geography_id = Column(Text(), ForeignKey('place.geoid'))
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
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"LocationAddress(geography_id={self.geography_id},address_line1={self.address_line1},address_line2={self.address_line2},city={self.city},zip={self.zip},lat={self.lat},lon={self.lon},is_anonymous={self.is_anonymous},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class UsdaStatisticCategory(LookupBase):
    """
    USDA statistic category.
    """
    __tablename__ = 'usda_statistic_category'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"UsdaStatisticCategory(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class UsdaSurveyProgram(LookupBase):
    """
    USDA survey program.
    """
    __tablename__ = 'usda_survey_program'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"UsdaSurveyProgram(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class UsdaSurveyRecord(BaseEntity):
    """
    USDA survey record.
    """
    __tablename__ = 'usda_survey_record'

    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    geoid = Column(Text())
    commodity_code = Column(Integer(), ForeignKey('usda_commodity.id'))
    year = Column(Integer())
    survey_program_id = Column(Integer(), ForeignKey('usda_survey_program.id'))
    survey_period = Column(Text())
    reference_month = Column(Text())
    seasonal_flag = Column(Boolean())
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"UsdaSurveyRecord(dataset_id={self.dataset_id},geoid={self.geoid},commodity_code={self.commodity_code},year={self.year},survey_program_id={self.survey_program_id},survey_period={self.survey_period},reference_month={self.reference_month},seasonal_flag={self.seasonal_flag},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class UsdaTermMap(BaseEntity):
    """
    Mapping of raw terms to USDA commodities.
    """
    __tablename__ = 'usda_term_map'

    source_system = Column(Text())
    source_context = Column(Text())
    raw_term = Column(Text())
    usda_commodity_id = Column(Integer(), ForeignKey('usda_commodity.id'))
    is_verified = Column(Boolean())
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"UsdaTermMap(source_system={self.source_system},source_context={self.source_context},raw_term={self.raw_term},usda_commodity_id={self.usda_commodity_id},is_verified={self.is_verified},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




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



class FieldSample(BaseEntity):
    """
    Sample collected from the field.
    """
    __tablename__ = 'field_sample'

    name = Column(Text())
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    provider_id = Column(Integer(), ForeignKey('provider.id'))
    collector_id = Column(Integer(), ForeignKey('contact.id'))
    sample_collection_source = Column(Text())
    amount_collected = Column(Numeric())
    amount_collected_unit_id = Column(Integer(), ForeignKey('unit.id'))
    sampling_location_id = Column(Integer(), ForeignKey('location_address.id'))
    field_storage_method_id = Column(Integer(), ForeignKey('field_storage_method.id'))
    field_storage_duration_value = Column(Numeric())
    field_storage_duration_unit_id = Column(Integer(), ForeignKey('unit.id'))
    field_storage_location_id = Column(Integer(), ForeignKey('location_address.id'))
    collection_timestamp = Column(DateTime())
    collection_method_id = Column(Integer(), ForeignKey('collection_method.id'))
    harvest_method_id = Column(Integer(), ForeignKey('harvest_method.id'))
    harvest_date = Column(Date())
    field_sample_storage_location_id = Column(Integer(), ForeignKey('location_address.id'))
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"FieldSample(name={self.name},resource_id={self.resource_id},provider_id={self.provider_id},collector_id={self.collector_id},sample_collection_source={self.sample_collection_source},amount_collected={self.amount_collected},amount_collected_unit_id={self.amount_collected_unit_id},sampling_location_id={self.sampling_location_id},field_storage_method_id={self.field_storage_method_id},field_storage_duration_value={self.field_storage_duration_value},field_storage_duration_unit_id={self.field_storage_duration_unit_id},field_storage_location_id={self.field_storage_location_id},collection_timestamp={self.collection_timestamp},collection_method_id={self.collection_method_id},harvest_method_id={self.harvest_method_id},harvest_date={self.harvest_date},field_sample_storage_location_id={self.field_sample_storage_location_id},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




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



class FieldSampleCondition(BaseEntity):
    """
    Condition of the field sample.
    """
    __tablename__ = 'field_sample_condition'

    field_sample_id = Column(Integer(), ForeignKey('field_sample.id'))
    ag_treatment_id = Column(Integer(), ForeignKey('ag_treatment.id'))
    last_application_date = Column(Date())
    treatment_amount_per_acre = Column(Float())
    processing_method_id = Column(Integer(), ForeignKey('processing_method.id'))
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"FieldSampleCondition(field_sample_id={self.field_sample_id},ag_treatment_id={self.ag_treatment_id},last_application_date={self.last_application_date},treatment_amount_per_acre={self.treatment_amount_per_acre},processing_method_id={self.processing_method_id},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




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



class LocationSoilType(BaseEntity):
    """
    Soil type at a location.
    """
    __tablename__ = 'location_soil_type'

    location_id = Column(Integer(), ForeignKey('location_address.id'))
    soil_type_id = Column(Integer(), ForeignKey('soil_type.id'))
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"LocationSoilType(location_id={self.location_id},soil_type_id={self.soil_type_id},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class PhysicalCharacteristic(BaseEntity):
    """
    Physical characteristics of a sample.
    """
    __tablename__ = 'physical_characteristic'

    field_sample_id = Column(Integer(), ForeignKey('field_sample.id'))
    particle_length = Column(Numeric())
    particle_width = Column(Numeric())
    particle_height = Column(Numeric())
    particle_unit_id = Column(Integer(), ForeignKey('unit.id'))
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"PhysicalCharacteristic(field_sample_id={self.field_sample_id},particle_length={self.particle_length},particle_width={self.particle_width},particle_height={self.particle_height},particle_unit_id={self.particle_unit_id},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




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

    record_id = Column(Text(), primary_key=True, nullable=False , unique=True)
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    record_type = Column(Text())
    parameter_id = Column(Integer(), ForeignKey('parameter.id'))
    value = Column(Numeric())
    unit_id = Column(Integer(), ForeignKey('unit.id'))
    dimension_type_id = Column(Integer(), ForeignKey('dimension_type.id'))
    dimension_value = Column(Numeric())
    dimension_unit_id = Column(Integer(), ForeignKey('unit.id'))
    note = Column(Text())
    id = Column(Integer(), nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Observation(record_id={self.record_id},dataset_id={self.dataset_id},record_type={self.record_type},parameter_id={self.parameter_id},value={self.value},unit_id={self.unit_id},dimension_type_id={self.dimension_type_id},dimension_value={self.dimension_value},dimension_unit_id={self.dimension_unit_id},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class FacilityRecord(BaseEntity):
    """
    Facility record.
    """
    __tablename__ = 'facility_record'

    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    facility_name = Column(Text())
    location_id = Column(Integer(), ForeignKey('location_address.id'))
    capacity_mw = Column(Numeric())
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    operator = Column(Text())
    start_year = Column(Integer())
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"FacilityRecord(dataset_id={self.dataset_id},facility_name={self.facility_name},location_id={self.location_id},capacity_mw={self.capacity_mw},resource_id={self.resource_id},operator={self.operator},start_year={self.start_year},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




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
    standard_unit_id = Column(Integer(), ForeignKey('unit.id'))
    calculated = Column(Boolean())
    description = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
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



class Contact(BaseEntity):
    """
    Contact information for a person.
    """
    __tablename__ = 'contact'

    first_name = Column(Text())
    last_name = Column(Text())
    email = Column(Text())
    affiliation = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Contact(first_name={self.first_name},last_name={self.last_name},email={self.email},affiliation={self.affiliation},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Provider(BaseEntity):
    """
    Provider information.
    """
    __tablename__ = 'provider'

    codename = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Provider(codename={self.codename},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Aim1RecordBase(BaseEntity):
    """

    """
    __tablename__ = 'aim1_record_base'

    record_id = Column(Text(), primary_key=True, nullable=False , unique=True)
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    prepared_sample_id = Column(Integer(), ForeignKey('prepared_sample.id'))
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer(), ForeignKey('method.id'))
    analyst_id = Column(Integer(), ForeignKey('contact.id'))
    raw_data_id = Column(Integer(), ForeignKey('file_object_metadata.id'))
    qc_pass = Column(Text())
    note = Column(Text())
    id = Column(Integer(), nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Aim1RecordBase(record_id={self.record_id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},prepared_sample_id={self.prepared_sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},analyst_id={self.analyst_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Aim2RecordBase(BaseEntity):
    """

    """
    __tablename__ = 'aim2_record_base'

    record_id = Column(Text(), primary_key=True, nullable=False , unique=True)
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    prepared_sample_id = Column(Integer(), ForeignKey('prepared_sample.id'))
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer(), ForeignKey('method.id'))
    analyst_id = Column(Integer(), ForeignKey('contact.id'))
    raw_data_id = Column(Integer(), ForeignKey('file_object_metadata.id'))
    qc_pass = Column(Text())
    note = Column(Text())
    id = Column(Integer(), nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Aim2RecordBase(record_id={self.record_id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},prepared_sample_id={self.prepared_sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},analyst_id={self.analyst_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Strain(LookupBase):
    """
    Strain used in fermentation.
    """
    __tablename__ = 'strain'

    parent_strain_id = Column(Integer())
    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"Strain(parent_strain_id={self.parent_strain_id},id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class ResourceAvailability(BaseEntity):
    """
    Availability of a resource in a location.
    """
    __tablename__ = 'resource_availability'

    resource_id = Column(Integer(), ForeignKey('resource.id'))
    geoid = Column(Text())
    from_month = Column(Integer())
    to_month = Column(Integer())
    year_round = Column(Boolean())
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"ResourceAvailability(resource_id={self.resource_id},geoid={self.geoid},from_month={self.from_month},to_month={self.to_month},year_round={self.year_round},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




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



class PreparationMethod(BaseEntity):
    """
    Method of sample preparation.
    """
    __tablename__ = 'preparation_method'

    name = Column(Text())
    description = Column(Text())
    prep_method_abbrev_id = Column(Integer(), ForeignKey('preparation_method_abbreviation.id'))
    prep_temp_c = Column(Numeric())
    uri = Column(Text())
    drying_step = Column(Boolean())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"PreparationMethod(name={self.name},description={self.description},prep_method_abbrev_id={self.prep_method_abbrev_id},prep_temp_c={self.prep_temp_c},uri={self.uri},drying_step={self.drying_step},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class PreparationMethodAbbreviation(LookupBase):
    """
    Abbreviation for preparation method.
    """
    __tablename__ = 'preparation_method_abbreviation'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"PreparationMethodAbbreviation(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class ProximateRecord(Aim1RecordBase):
    """
    Proximate analysis record.
    """
    __tablename__ = 'proximate_record'

    record_id = Column(Text(), primary_key=True, nullable=False , unique=True)
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    prepared_sample_id = Column(Integer(), ForeignKey('prepared_sample.id'))
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer(), ForeignKey('method.id'))
    analyst_id = Column(Integer(), ForeignKey('contact.id'))
    raw_data_id = Column(Integer(), ForeignKey('file_object_metadata.id'))
    qc_pass = Column(Text())
    note = Column(Text())
    id = Column(Integer(), nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"ProximateRecord(record_id={self.record_id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},prepared_sample_id={self.prepared_sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},analyst_id={self.analyst_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class UltimateRecord(Aim1RecordBase):
    """
    Ultimate analysis record.
    """
    __tablename__ = 'ultimate_record'

    record_id = Column(Text(), primary_key=True, nullable=False , unique=True)
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    prepared_sample_id = Column(Integer(), ForeignKey('prepared_sample.id'))
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer(), ForeignKey('method.id'))
    analyst_id = Column(Integer(), ForeignKey('contact.id'))
    raw_data_id = Column(Integer(), ForeignKey('file_object_metadata.id'))
    qc_pass = Column(Text())
    note = Column(Text())
    id = Column(Integer(), nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"UltimateRecord(record_id={self.record_id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},prepared_sample_id={self.prepared_sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},analyst_id={self.analyst_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class CompositionalRecord(Aim1RecordBase):
    """
    Compositional analysis record.
    """
    __tablename__ = 'compositional_record'

    record_id = Column(Text(), primary_key=True, nullable=False , unique=True)
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    prepared_sample_id = Column(Integer(), ForeignKey('prepared_sample.id'))
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer(), ForeignKey('method.id'))
    analyst_id = Column(Integer(), ForeignKey('contact.id'))
    raw_data_id = Column(Integer(), ForeignKey('file_object_metadata.id'))
    qc_pass = Column(Text())
    note = Column(Text())
    id = Column(Integer(), nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"CompositionalRecord(record_id={self.record_id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},prepared_sample_id={self.prepared_sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},analyst_id={self.analyst_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class IcpRecord(Aim1RecordBase):
    """
    ICP analysis record.
    """
    __tablename__ = 'icp_record'

    record_id = Column(Text(), primary_key=True, nullable=False , unique=True)
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    prepared_sample_id = Column(Integer(), ForeignKey('prepared_sample.id'))
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer(), ForeignKey('method.id'))
    analyst_id = Column(Integer(), ForeignKey('contact.id'))
    raw_data_id = Column(Integer(), ForeignKey('file_object_metadata.id'))
    qc_pass = Column(Text())
    note = Column(Text())
    id = Column(Integer(), nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"IcpRecord(record_id={self.record_id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},prepared_sample_id={self.prepared_sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},analyst_id={self.analyst_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class XrfRecord(Aim1RecordBase):
    """
    XRF analysis record.
    """
    __tablename__ = 'xrf_record'

    wavelength_nm = Column(Numeric())
    intensity = Column(Numeric())
    energy_slope = Column(Numeric())
    energy_offset = Column(Numeric())
    record_id = Column(Text(), primary_key=True, nullable=False , unique=True)
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    prepared_sample_id = Column(Integer(), ForeignKey('prepared_sample.id'))
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer(), ForeignKey('method.id'))
    analyst_id = Column(Integer(), ForeignKey('contact.id'))
    raw_data_id = Column(Integer(), ForeignKey('file_object_metadata.id'))
    qc_pass = Column(Text())
    note = Column(Text())
    id = Column(Integer(), nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"XrfRecord(wavelength_nm={self.wavelength_nm},intensity={self.intensity},energy_slope={self.energy_slope},energy_offset={self.energy_offset},record_id={self.record_id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},prepared_sample_id={self.prepared_sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},analyst_id={self.analyst_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class XrdRecord(Aim1RecordBase):
    """
    XRD analysis record.
    """
    __tablename__ = 'xrd_record'

    scan_low_nm = Column(Integer())
    scan_high_nm = Column(Integer())
    record_id = Column(Text(), primary_key=True, nullable=False , unique=True)
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    prepared_sample_id = Column(Integer(), ForeignKey('prepared_sample.id'))
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer(), ForeignKey('method.id'))
    analyst_id = Column(Integer(), ForeignKey('contact.id'))
    raw_data_id = Column(Integer(), ForeignKey('file_object_metadata.id'))
    qc_pass = Column(Text())
    note = Column(Text())
    id = Column(Integer(), nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"XrdRecord(scan_low_nm={self.scan_low_nm},scan_high_nm={self.scan_high_nm},record_id={self.record_id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},prepared_sample_id={self.prepared_sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},analyst_id={self.analyst_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class CalorimetryRecord(Aim1RecordBase):
    """
    Calorimetry analysis record.
    """
    __tablename__ = 'calorimetry_record'

    record_id = Column(Text(), primary_key=True, nullable=False , unique=True)
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    prepared_sample_id = Column(Integer(), ForeignKey('prepared_sample.id'))
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer(), ForeignKey('method.id'))
    analyst_id = Column(Integer(), ForeignKey('contact.id'))
    raw_data_id = Column(Integer(), ForeignKey('file_object_metadata.id'))
    qc_pass = Column(Text())
    note = Column(Text())
    id = Column(Integer(), nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"CalorimetryRecord(record_id={self.record_id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},prepared_sample_id={self.prepared_sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},analyst_id={self.analyst_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class FtnirRecord(Aim1RecordBase):
    """
    FT-NIR analysis record.
    """
    __tablename__ = 'ftnir_record'

    record_id = Column(Text(), primary_key=True, nullable=False , unique=True)
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    prepared_sample_id = Column(Integer(), ForeignKey('prepared_sample.id'))
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer(), ForeignKey('method.id'))
    analyst_id = Column(Integer(), ForeignKey('contact.id'))
    raw_data_id = Column(Integer(), ForeignKey('file_object_metadata.id'))
    qc_pass = Column(Text())
    note = Column(Text())
    id = Column(Integer(), nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"FtnirRecord(record_id={self.record_id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},prepared_sample_id={self.prepared_sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},analyst_id={self.analyst_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class RgbRecord(Aim1RecordBase):
    """
    RGB analysis record.
    """
    __tablename__ = 'rgb_record'

    record_id = Column(Text(), primary_key=True, nullable=False , unique=True)
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    prepared_sample_id = Column(Integer(), ForeignKey('prepared_sample.id'))
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer(), ForeignKey('method.id'))
    analyst_id = Column(Integer(), ForeignKey('contact.id'))
    raw_data_id = Column(Integer(), ForeignKey('file_object_metadata.id'))
    qc_pass = Column(Text())
    note = Column(Text())
    id = Column(Integer(), nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"RgbRecord(record_id={self.record_id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},prepared_sample_id={self.prepared_sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},analyst_id={self.analyst_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class PretreatmentRecord(Aim2RecordBase):
    """
    Pretreatment record.
    """
    __tablename__ = 'pretreatment_record'

    pretreatment_method_id = Column(Integer())
    eh_method_id = Column(Integer())
    reaction_block_id = Column(Integer())
    block_position = Column(Text())
    temperature = Column(Numeric())
    replicate_no = Column(Integer())
    record_id = Column(Text(), primary_key=True, nullable=False , unique=True)
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    prepared_sample_id = Column(Integer(), ForeignKey('prepared_sample.id'))
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer(), ForeignKey('method.id'))
    analyst_id = Column(Integer(), ForeignKey('contact.id'))
    raw_data_id = Column(Integer(), ForeignKey('file_object_metadata.id'))
    qc_pass = Column(Text())
    note = Column(Text())
    id = Column(Integer(), nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"PretreatmentRecord(pretreatment_method_id={self.pretreatment_method_id},eh_method_id={self.eh_method_id},reaction_block_id={self.reaction_block_id},block_position={self.block_position},temperature={self.temperature},replicate_no={self.replicate_no},record_id={self.record_id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},prepared_sample_id={self.prepared_sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},analyst_id={self.analyst_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class FermentationRecord(Aim2RecordBase):
    """
    Fermentation record.
    """
    __tablename__ = 'fermentation_record'

    strain_id = Column(Integer())
    pretreatment_method_id = Column(Integer())
    eh_method_id = Column(Integer())
    well_position = Column(Text())
    temperature = Column(Numeric())
    agitation_rpm = Column(Numeric())
    vessel_id = Column(Integer())
    analyte_detection_equipment_id = Column(Integer())
    record_id = Column(Text(), primary_key=True, nullable=False , unique=True)
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    prepared_sample_id = Column(Integer(), ForeignKey('prepared_sample.id'))
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer(), ForeignKey('method.id'))
    analyst_id = Column(Integer(), ForeignKey('contact.id'))
    raw_data_id = Column(Integer(), ForeignKey('file_object_metadata.id'))
    qc_pass = Column(Text())
    note = Column(Text())
    id = Column(Integer(), nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"FermentationRecord(strain_id={self.strain_id},pretreatment_method_id={self.pretreatment_method_id},eh_method_id={self.eh_method_id},well_position={self.well_position},temperature={self.temperature},agitation_rpm={self.agitation_rpm},vessel_id={self.vessel_id},analyte_detection_equipment_id={self.analyte_detection_equipment_id},record_id={self.record_id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},prepared_sample_id={self.prepared_sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},analyst_id={self.analyst_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class GasificationRecord(Aim2RecordBase):
    """
    Gasification record.
    """
    __tablename__ = 'gasification_record'

    feedstock_mass = Column(Numeric())
    bed_temperature = Column(Numeric())
    gas_flow_rate = Column(Numeric())
    record_id = Column(Text(), primary_key=True, nullable=False , unique=True)
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    prepared_sample_id = Column(Integer(), ForeignKey('prepared_sample.id'))
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer(), ForeignKey('method.id'))
    analyst_id = Column(Integer(), ForeignKey('contact.id'))
    raw_data_id = Column(Integer(), ForeignKey('file_object_metadata.id'))
    qc_pass = Column(Text())
    note = Column(Text())
    id = Column(Integer(), nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"GasificationRecord(feedstock_mass={self.feedstock_mass},bed_temperature={self.bed_temperature},gas_flow_rate={self.gas_flow_rate},record_id={self.record_id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},prepared_sample_id={self.prepared_sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},analyst_id={self.analyst_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class AutoclaveRecord(Aim2RecordBase):
    """
    Autoclave record.
    """
    __tablename__ = 'autoclave_record'

    record_id = Column(Text(), primary_key=True, nullable=False , unique=True)
    dataset_id = Column(Integer(), ForeignKey('dataset.id'))
    experiment_id = Column(Integer(), ForeignKey('experiment.id'))
    resource_id = Column(Integer(), ForeignKey('resource.id'))
    prepared_sample_id = Column(Integer(), ForeignKey('prepared_sample.id'))
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer(), ForeignKey('method.id'))
    analyst_id = Column(Integer(), ForeignKey('contact.id'))
    raw_data_id = Column(Integer(), ForeignKey('file_object_metadata.id'))
    qc_pass = Column(Text())
    note = Column(Text())
    id = Column(Integer(), nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Integer(), ForeignKey('etl_run.id'))
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"AutoclaveRecord(record_id={self.record_id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},prepared_sample_id={self.prepared_sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},analyst_id={self.analyst_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
