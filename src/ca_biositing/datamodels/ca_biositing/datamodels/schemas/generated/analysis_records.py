
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()
metadata = Base.metadata


class RecordBase(Base):
    """

    """
    __tablename__ = 'record_base'

    id = Column(Integer(), primary_key=True, nullable=False )
    dataset_id = Column(Integer())
    experiment_id = Column(Integer())
    resource_id = Column(Integer())
    sample_id = Column(Integer())
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer())
    raw_data_id = Column(Integer())
    qc_pass = Column(Boolean())
    note = Column(Text())


    def __repr__(self):
        return f"RecordBase(id={self.id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},sample_id={self.sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},)"






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






class Dataset(Base):
    """
    Dataset definition.
    """
    __tablename__ = 'dataset'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    record_type = Column(Text())
    source_id = Column(Integer())
    start_date = Column(DateTime())
    end_date = Column(DateTime())
    description = Column(Text())


    def __repr__(self):
        return f"Dataset(id={self.id},name={self.name},record_type={self.record_type},source_id={self.source_id},start_date={self.start_date},end_date={self.end_date},description={self.description},)"






class Observation(Base):
    """
    Observation data.
    """
    __tablename__ = 'observation'

    id = Column(Integer(), primary_key=True, nullable=False )
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


    def __repr__(self):
        return f"Observation(id={self.id},dataset_id={self.dataset_id},record_type={self.record_type},record_id={self.record_id},parameter_id={self.parameter_id},value={self.value},unit_id={self.unit_id},dimension_type_id={self.dimension_type_id},dimension_value={self.dimension_value},dimension_unit_id={self.dimension_unit_id},note={self.note},)"






class Geography(Base):
    """
    Geographic region definition (e.g. county, state).
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






class Polygon(Base):
    """
    Geospatial polygon definition.
    """
    __tablename__ = 'polygon'

    id = Column(Integer(), primary_key=True, nullable=False )
    geoid = Column(Text())
    geom = Column(Text())


    def __repr__(self):
        return f"Polygon(id={self.id},geoid={self.geoid},geom={self.geom},)"






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






class ParameterCategoryParameter(Base):
    """
    Link between parameter and category.
    """
    __tablename__ = 'parameter_category_parameter'

    id = Column(Integer(), primary_key=True, nullable=False )
    parameter_id = Column(Integer())
    parameter_category_id = Column(Integer())


    def __repr__(self):
        return f"ParameterCategoryParameter(id={self.id},parameter_id={self.parameter_id},parameter_category_id={self.parameter_category_id},)"






class ParameterUnit(Base):
    """
    Link between parameter and alternate units.
    """
    __tablename__ = 'parameter_unit'

    id = Column(Integer(), primary_key=True, nullable=False )
    parameter_id = Column(Integer())
    alternate_unit_id = Column(Integer())


    def __repr__(self):
        return f"ParameterUnit(id={self.id},parameter_id={self.parameter_id},alternate_unit_id={self.alternate_unit_id},)"






class ExperimentEquipment(Base):
    """
    Link between experiment and equipment.
    """
    __tablename__ = 'experiment_equipment'

    id = Column(Integer(), primary_key=True, nullable=False )
    experiment_id = Column(Integer())
    equipment_id = Column(Integer())


    def __repr__(self):
        return f"ExperimentEquipment(id={self.id},experiment_id={self.experiment_id},equipment_id={self.equipment_id},)"






class ExperimentAnalysis(Base):
    """
    Link between experiment and analysis type.
    """
    __tablename__ = 'experiment_analysis'

    id = Column(Integer(), primary_key=True, nullable=False )
    experiment_id = Column(Integer())
    analysis_type_id = Column(Integer())


    def __repr__(self):
        return f"ExperimentAnalysis(id={self.id},experiment_id={self.experiment_id},analysis_type_id={self.analysis_type_id},)"






class ExperimentPreparedSample(Base):
    """
    Link between experiment and prepared sample.
    """
    __tablename__ = 'experiment_prepared_sample'

    id = Column(Integer(), primary_key=True, nullable=False )
    experiment_id = Column(Integer())
    prepared_sample_id = Column(Integer())


    def __repr__(self):
        return f"ExperimentPreparedSample(id={self.id},experiment_id={self.experiment_id},prepared_sample_id={self.prepared_sample_id},)"






class ExperimentMethod(Base):
    """
    Link between experiment and method.
    """
    __tablename__ = 'experiment_method'

    id = Column(Integer(), primary_key=True, nullable=False )
    experiment_id = Column(Integer())
    method_id = Column(Integer())


    def __repr__(self):
        return f"ExperimentMethod(id={self.id},experiment_id={self.experiment_id},method_id={self.method_id},)"






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






class ProximateRecord(RecordBase):
    """
    Proximate analysis record.
    """
    __tablename__ = 'proximate_record'

    id = Column(Integer(), primary_key=True, nullable=False )
    dataset_id = Column(Integer())
    experiment_id = Column(Integer())
    resource_id = Column(Integer())
    sample_id = Column(Integer())
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer())
    raw_data_id = Column(Integer())
    qc_pass = Column(Boolean())
    note = Column(Text())


    def __repr__(self):
        return f"ProximateRecord(id={self.id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},sample_id={self.sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class UltimateRecord(RecordBase):
    """
    Ultimate analysis record.
    """
    __tablename__ = 'ultimate_record'

    id = Column(Integer(), primary_key=True, nullable=False )
    dataset_id = Column(Integer())
    experiment_id = Column(Integer())
    resource_id = Column(Integer())
    sample_id = Column(Integer())
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer())
    raw_data_id = Column(Integer())
    qc_pass = Column(Boolean())
    note = Column(Text())


    def __repr__(self):
        return f"UltimateRecord(id={self.id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},sample_id={self.sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class CompositionalRecord(RecordBase):
    """
    Compositional analysis record.
    """
    __tablename__ = 'compositional_record'

    id = Column(Integer(), primary_key=True, nullable=False )
    dataset_id = Column(Integer())
    experiment_id = Column(Integer())
    resource_id = Column(Integer())
    sample_id = Column(Integer())
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer())
    raw_data_id = Column(Integer())
    qc_pass = Column(Boolean())
    note = Column(Text())


    def __repr__(self):
        return f"CompositionalRecord(id={self.id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},sample_id={self.sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class IcpRecord(RecordBase):
    """
    ICP analysis record.
    """
    __tablename__ = 'icp_record'

    id = Column(Integer(), primary_key=True, nullable=False )
    dataset_id = Column(Integer())
    experiment_id = Column(Integer())
    resource_id = Column(Integer())
    sample_id = Column(Integer())
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer())
    raw_data_id = Column(Integer())
    qc_pass = Column(Boolean())
    note = Column(Text())


    def __repr__(self):
        return f"IcpRecord(id={self.id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},sample_id={self.sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class XrfRecord(RecordBase):
    """
    XRF analysis record.
    """
    __tablename__ = 'xrf_record'

    maybe_wavelength_nm = Column(Numeric())
    maybe_intensity = Column(Numeric())
    maybe_energy_slope = Column(Numeric())
    maybe_energy_offset = Column(Numeric())
    id = Column(Integer(), primary_key=True, nullable=False )
    dataset_id = Column(Integer())
    experiment_id = Column(Integer())
    resource_id = Column(Integer())
    sample_id = Column(Integer())
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer())
    raw_data_id = Column(Integer())
    qc_pass = Column(Boolean())
    note = Column(Text())


    def __repr__(self):
        return f"XrfRecord(maybe_wavelength_nm={self.maybe_wavelength_nm},maybe_intensity={self.maybe_intensity},maybe_energy_slope={self.maybe_energy_slope},maybe_energy_offset={self.maybe_energy_offset},id={self.id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},sample_id={self.sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class XrdRecord(RecordBase):
    """
    XRD analysis record.
    """
    __tablename__ = 'xrd_record'

    maybe_scan_low_nm = Column(Integer())
    maybe_scan_high_nm = Column(Integer())
    id = Column(Integer(), primary_key=True, nullable=False )
    dataset_id = Column(Integer())
    experiment_id = Column(Integer())
    resource_id = Column(Integer())
    sample_id = Column(Integer())
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer())
    raw_data_id = Column(Integer())
    qc_pass = Column(Boolean())
    note = Column(Text())


    def __repr__(self):
        return f"XrdRecord(maybe_scan_low_nm={self.maybe_scan_low_nm},maybe_scan_high_nm={self.maybe_scan_high_nm},id={self.id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},sample_id={self.sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class CalorimetryRecord(RecordBase):
    """
    Calorimetry analysis record.
    """
    __tablename__ = 'calorimetry_record'

    id = Column(Integer(), primary_key=True, nullable=False )
    dataset_id = Column(Integer())
    experiment_id = Column(Integer())
    resource_id = Column(Integer())
    sample_id = Column(Integer())
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer())
    raw_data_id = Column(Integer())
    qc_pass = Column(Boolean())
    note = Column(Text())


    def __repr__(self):
        return f"CalorimetryRecord(id={self.id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},sample_id={self.sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class FtnirRecord(RecordBase):
    """
    FT-NIR analysis record.
    """
    __tablename__ = 'ftnir_record'

    id = Column(Integer(), primary_key=True, nullable=False )
    dataset_id = Column(Integer())
    experiment_id = Column(Integer())
    resource_id = Column(Integer())
    sample_id = Column(Integer())
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer())
    raw_data_id = Column(Integer())
    qc_pass = Column(Boolean())
    note = Column(Text())


    def __repr__(self):
        return f"FtnirRecord(id={self.id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},sample_id={self.sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class RgbRecord(RecordBase):
    """
    RGB analysis record.
    """
    __tablename__ = 'rgb_record'

    id = Column(Integer(), primary_key=True, nullable=False )
    dataset_id = Column(Integer())
    experiment_id = Column(Integer())
    resource_id = Column(Integer())
    sample_id = Column(Integer())
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer())
    raw_data_id = Column(Integer())
    qc_pass = Column(Boolean())
    note = Column(Text())


    def __repr__(self):
        return f"RgbRecord(id={self.id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},sample_id={self.sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class PretreatmentRecord(RecordBase):
    """
    Pretreatment record.
    """
    __tablename__ = 'pretreatment_record'

    pretreatment_method = Column(Integer())
    eh_method_id = Column(Integer())
    reaction_block_id = Column(Integer())
    block_position = Column(Text())
    temperature = Column(Numeric())
    replicate_no = Column(Integer())
    analyst_id = Column(Integer())
    id = Column(Integer(), primary_key=True, nullable=False )
    dataset_id = Column(Integer())
    experiment_id = Column(Integer())
    resource_id = Column(Integer())
    sample_id = Column(Integer())
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer())
    raw_data_id = Column(Integer())
    qc_pass = Column(Boolean())
    note = Column(Text())


    def __repr__(self):
        return f"PretreatmentRecord(pretreatment_method={self.pretreatment_method},eh_method_id={self.eh_method_id},reaction_block_id={self.reaction_block_id},block_position={self.block_position},temperature={self.temperature},replicate_no={self.replicate_no},analyst_id={self.analyst_id},id={self.id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},sample_id={self.sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class FermentationRecord(RecordBase):
    """
    Fermentation record.
    """
    __tablename__ = 'fermentation_record'

    strain_id = Column(Integer())
    pretreatement_method_id = Column(Integer())
    eh_method_id = Column(Integer())
    replicate_no = Column(Integer())
    well_position = Column(Text())
    temperature = Column(Numeric())
    agitation_rpm = Column(Numeric())
    vessel_id = Column(Integer())
    analyte_detection_equipment_id = Column(Integer())
    analyst_id = Column(Integer())
    id = Column(Integer(), primary_key=True, nullable=False )
    dataset_id = Column(Integer())
    experiment_id = Column(Integer())
    resource_id = Column(Integer())
    sample_id = Column(Integer())
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer())
    raw_data_id = Column(Integer())
    qc_pass = Column(Boolean())
    note = Column(Text())


    def __repr__(self):
        return f"FermentationRecord(strain_id={self.strain_id},pretreatement_method_id={self.pretreatement_method_id},eh_method_id={self.eh_method_id},replicate_no={self.replicate_no},well_position={self.well_position},temperature={self.temperature},agitation_rpm={self.agitation_rpm},vessel_id={self.vessel_id},analyte_detection_equipment_id={self.analyte_detection_equipment_id},analyst_id={self.analyst_id},id={self.id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},sample_id={self.sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class GasificationRecord(RecordBase):
    """
    Gasification record.
    """
    __tablename__ = 'gasification_record'

    feedstock_mass = Column(Numeric())
    bed_temperature = Column(Numeric())
    gas_flow_rate = Column(Numeric())
    analyst_id = Column(Integer())
    id = Column(Integer(), primary_key=True, nullable=False )
    dataset_id = Column(Integer())
    experiment_id = Column(Integer())
    resource_id = Column(Integer())
    sample_id = Column(Integer())
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer())
    raw_data_id = Column(Integer())
    qc_pass = Column(Boolean())
    note = Column(Text())


    def __repr__(self):
        return f"GasificationRecord(feedstock_mass={self.feedstock_mass},bed_temperature={self.bed_temperature},gas_flow_rate={self.gas_flow_rate},analyst_id={self.analyst_id},id={self.id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},sample_id={self.sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class AutoclaveRecord(RecordBase):
    """
    Autoclave record.
    """
    __tablename__ = 'autoclave_record'

    analyst_id = Column(Integer())
    id = Column(Integer(), primary_key=True, nullable=False )
    dataset_id = Column(Integer())
    experiment_id = Column(Integer())
    resource_id = Column(Integer())
    sample_id = Column(Integer())
    technical_replicate_no = Column(Integer())
    technical_replicate_total = Column(Integer())
    method_id = Column(Integer())
    raw_data_id = Column(Integer())
    qc_pass = Column(Boolean())
    note = Column(Text())


    def __repr__(self):
        return f"AutoclaveRecord(analyst_id={self.analyst_id},id={self.id},dataset_id={self.dataset_id},experiment_id={self.experiment_id},resource_id={self.resource_id},sample_id={self.sample_id},technical_replicate_no={self.technical_replicate_no},technical_replicate_total={self.technical_replicate_total},method_id={self.method_id},raw_data_id={self.raw_data_id},qc_pass={self.qc_pass},note={self.note},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class DimensionType(LookupBase):
    """
    Type of dimension (e.g. timepoint, wavelength).
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



class LocationAddress(BaseEntity):
    """
    Specific physical location.
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
    Abbreviation for a method.
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
    Category of a method.
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
    Standard associated with a method.
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
    Parameter measured.
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
    Category of a parameter.
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



class PreparationMethod(BaseEntity):
    """
    Method of sample preparation.
    """
    __tablename__ = 'preparation_method'

    name = Column(Text())
    description = Column(Text())
    prep_method_abbrev_id = Column(Integer())
    prep_temp_c = Column(Numeric())
    uri = Column(Text())
    drying_step = Column(Boolean())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
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



class PreparedSample(BaseEntity):
    """
    Sample prepared for analysis.
    """
    __tablename__ = 'prepared_sample'

    name = Column(Text())
    field_sample_id = Column(Integer())
    prep_method_id = Column(Integer())
    prep_date = Column(Date())
    preparer_id = Column(Integer())
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"PreparedSample(name={self.name},field_sample_id={self.field_sample_id},prep_method_id={self.prep_method_id},prep_date={self.prep_date},preparer_id={self.preparer_id},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Experiment(BaseEntity):
    """
    Experiment definition.
    """
    __tablename__ = 'experiment'

    analyst_id = Column(Integer())
    exper_start_date = Column(Date())
    exper_duration = Column(Numeric())
    exper_duration_unit_id = Column(Integer())
    exper_location_id = Column(Integer())
    description = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Experiment(analyst_id={self.analyst_id},exper_start_date={self.exper_start_date},exper_duration={self.exper_duration},exper_duration_unit_id={self.exper_duration_unit_id},exper_location_id={self.exper_location_id},description={self.description},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Equipment(LookupBase):
    """
    Equipment used in experiments.
    """
    __tablename__ = 'equipment'

    equipment_location_id = Column(Integer())
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



class Strain(LookupBase):
    """
    Strain of organism.
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
