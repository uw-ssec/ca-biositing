
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()
metadata = Base.metadata


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



class DataSource(BaseEntity):
    """
    Source of data.
    """
    __tablename__ = 'data_source'

    name = Column(Text())
    description = Column(Text())
    data_source_type_id = Column(Integer())
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
    location_coverage_id = Column(Integer())
    rights = Column(Text())
    license = Column(Text())
    uri = Column(Text())
    note = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"DataSource(name={self.name},description={self.description},data_source_type_id={self.data_source_type_id},full_title={self.full_title},creator={self.creator},subject={self.subject},publisher={self.publisher},contributor={self.contributor},date={self.date},type={self.type},biocirv={self.biocirv},format={self.format},language={self.language},relation={self.relation},temporal_coverage={self.temporal_coverage},location_coverage_id={self.location_coverage_id},rights={self.rights},license={self.license},uri={self.uri},note={self.note},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




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
    Type of data source (e.g. database, literature).
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



class Contact(BaseEntity):
    """
    Contact information for a person.
    """
    __tablename__ = 'contact'

    id = Column(Integer(), primary_key=True, nullable=False )
    first_name = Column(Text())
    last_name = Column(Text())
    email = Column(Text())
    affiliation = Column(Text())
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Contact(id={self.id},first_name={self.first_name},last_name={self.last_name},email={self.email},affiliation={self.affiliation},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Provider(BaseEntity):
    """
    Provider information.
    """
    __tablename__ = 'provider'

    id = Column(Integer(), primary_key=True, nullable=False )
    codename = Column(Text())
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Provider(id={self.id},codename={self.codename},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




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
