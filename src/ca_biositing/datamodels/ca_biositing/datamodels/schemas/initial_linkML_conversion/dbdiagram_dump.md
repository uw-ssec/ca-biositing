/////////////////////////////////////////////////////////// // BASE ENTITY
(included in all main entity tables) // id int [pk, increment] // created_at
datetime [default: `current_timestamp`] // updated_at datetime [default:
`current_timestamp`] // etl_run_id string // lineage_group_id int [ref: >
lineage_group.id] ///////////////////////////////////////////////////////////

// LookupBase for enum/ontology-like tables // id int [pk, increment] // name
string [not null, unique] // description string // uri string
///////////////////////////////////////////////////////////

//===================TABLE GROUPS================== TableGroup "Resource
Information" [color: #1E69FD] { resource resource_class resource_subclass
primary_crop resource_availability resource_counterfactual resource_morphology }

TableGroup "Field Sampling" [color: #d35400] { field_sample field_storage_method
collection_method harvest_method physical_characteristic soil_type ag_treatment
field_sample_condition processing_method location_soil_type }

TableGroup "Places" { geography location_address }

TableGroup "People" { provider contact }

TableGroup "Lineage" { lineage_group entity_lineage etl_run }

TableGroup "Data Sources & Metadata" [color: #990D0D]{ data_source
data_source_type source_type file_object_metadata location_resolution }

TableGroup "Sample Preparation" [color:#F7AC5E] { preparation_method
preparation_method_abbreviation prepared_sample }

TableGroup "Methods, Parameters, Units" [color: #F0B7B7]{ unit method_abbrev
method_category method_standard parameter_category method parameter
parameter_unit

}

TableGroup "Experiment, Equipment" [color: #CDFC9F]{ experiment
experiment_method equipment experiment_analysis experiment_equipment
experiment_prepared_sample }

TableGroup "General Analysis" [color: #A15CF5]{ analysis_type observation
dataset dimension_type }

TableGroup "Aim2 Records" [color: #cc0000]{ fermentation_record
gasification_record pretreatment_record autoclave_record strain }

TableGroup "Aim1 Records" [color: #ffc84f] { proximate_record
compositional_record ultimate_record icp_record calorimetry_record xrf_record
xrd_record rgb_record ftnir_record }

TableGroup "External Data" [color:#20b2aa] { usda_census_record //usda_commodity
//usda_commodity_to_primary_crop usda_domain usda_statistic_category
usda_survey_program usda_survey_record usda_market_record
billion_ton_2023_record landiq_record polygon //I think this is used to
essentially get all polygons in a county?

}

TableGroup "Infrastructure" [color:#6495ed]{ facility_record
infrastructure_biodiesel_plants infrastructure_biosolids_facilities
infrastructure_cafo_manure_locations infrastructure_ethanol_biorefineries
infrastructure_landfills infrastructure_livestock_anaerobic_digesters
infrastructure_saf_and_renewable_diesel_plants
infrastructure_wastewater_treatment_plants infrastructure_combustion_plants
infrastructure_district_energy_systems infrastructure_food_processing_facilities
infrastructure_msw_to_energy_anaerobic_digesters }

/////////////////////////////////////////////////////////// // LINEAGE TABLES
///////////////////////////////////////////////////////////

Table lineage_group { id int [pk, increment] etl_run_id string [ref:>
etl_run.id] note text }

Table entity_lineage { id int [pk, increment] lineage_group_id int [not null,
ref: > lineage_group.id] source_table string [not null] // sheet or raw table
source_row_id string [not null] // row index or key note text }

Table etl_run { id string [pk] // UUID started_at datetime completed_at datetime
pipeline_name string status string // success/failure/partial records_ingested
int note text }

/////////////////////////////////////////////////////////// // RESOURCE
///////////////////////////////////////////////////////////

Table resource { // BaseEntity id int [pk, increment] created_at datetime
[default: `current_timestamp`] updated_at datetime [default:
`current_timestamp`] etl_run_id string lineage_group_id int [ref: >
lineage_group.id]

// Domain fields name string [not null, unique] primary_crop_id int [not null,
ref: > primary_crop.id] resource_class_id int [not null, ref: >
resource_class.id] resource_subclass_id int [ref: > resource_subclass.id] note
text }

Table resource_class { // LookupBase id int [pk, increment] name string [not
null, unique] description string uri string }

Table resource_subclass { // LookupBase id int [pk, increment] name string [not
null, unique] description string uri string }

/////////////////////////////////////////////////////////// // PRIMARY CROP
///////////////////////////////////////////////////////////

Table primary_crop { // LookupBase (+ ontology) id int [pk, increment] name
string [not null, unique] description string uri string note text }

/////////////////////////////////////////////////////////// // RESOURCE
AVAILABILITY ///////////////////////////////////////////////////////////

Table resource_availability { // BaseEntity id int [pk, increment] created_at
datetime [default: `current_timestamp`] updated_at datetime [default:
`current_timestamp`] etl_run_id string lineage_group_id int [ref: >
lineage_group.id]

// Domain fields resource_id int [not null, ref: > resource.id] geoid string
[not null, ref: > geography.geoid]

from_month int to_month int year_round boolean note text }

/////////////////////////////////////////////////////////// // RESOURCE
COUNTERFACTUAL ///////////////////////////////////////////////////////////

Table resource_counterfactual { // BaseEntity id int [pk, increment] created_at
datetime [default: `current_timestamp`] updated_at datetime [default:
`current_timestamp`] etl_run_id string lineage_group_id int [ref: >
lineage_group.id] // Domain fields geoid string [not null, ref: >
geography.geoid] //location resource_id int [not null, ref: > resource.id]
counterfactual_description text //animal is too broad. Want just livestock and
poultry animal_bedding_percent decimal animal_bedding_source_id int [ref:>
data_source.id] animal_feed_percent decimal animal_feed_source_id int [ref:>
data_source.id] bioelectricty_percent decimal bioelectricty_source_id int [ref:>
data_source.id] burn_percent decimal burn_source_id int [ref:> data_source.id]
compost_percent decimal compost_source_id int [ref:> data_source.id]
landfill_percent decimal landfill_source_id int [ref:> data_source.id]
counterfactual_date date //contained in source. Set a base year as a disclaimer
//scenario identifier note text }

/////////////////////////////////////////////////////////// // RESOURCE
MORPHOLOGY (many-to-many)
///////////////////////////////////////////////////////////

//'Check morphology ontology with Andrea' Table resource_morphology { id int
[pk, increment] resource_id int [not null, ref: > resource.id] morphology_uri
string [not null] // ontology URI for plant part (stem, shell, leaf…) }

/////////////////////////////////////////////////////////// // GEOGRAPHY /
PLACES ///////////////////////////////////////////////////////////

Table geography { geoid string [pk] state_name string state_fips string
county_name string county_fips string region_name string agg_level_desc string }

Table location_address { id int [pk, increment] geography_id string [ref: >
geography.geoid] address_line1 string address_line2 string city string zip
string lat float lon float is_anonymous boolean }

/////////////////////////////////////////////////////////// // NOTES
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////// // FIELD SAMPLES TABLE
GROUP ////////////////////////////////////////////////////////

Table field_sample [headercolor: #d35400] { //Base entity id int [pk, increment]
created_at datetime [default: `current_timestamp`] updated_at datetime [default:
`current_timestamp`] etl_run_id string lineage_group_id int [ref: >
lineage_group.id] //Domain Specific name string [not null, note: "e.g.,
Ene-WaHu018"] //Should link perfectly to Gsheet sample name resource_id integer
[not null, ref: > resource.id] provider_id integer [ref: > provider.id] // needs
to be anon //add this! collector_id integer [ref: > contact.id]
sample_collection_source text //this is kind of free for all in the sample
metadata gsheet amount_collected decimal //consider making not null
amount_collected_unit_id integer [ref:> unit.id] //consider making not null
//source_codename_id integer [note: "Anonymized source identifier"] //not sure
what to do with this? Should we keep? sampling_location_id integer [not null,
ref: > location_address.id] // needs to be anon. May be null if from external
sources //I think we can do this via permissions in the database itself...
field_storage_method_id integer [ref: > field_storage_method.id]
field_storage_duration_value decimal field_storage_duration_unit_id integer
[ref:> unit.id] field_storage_location_id integer [ref:> location_address.id] //
nullable; may be same as sampling_location_id collection_timestamp timestamp
collection_method_id integer [ref: > collection_method.id] harvest_method_id
integer [ref: > harvest_method.id] harvest_date date //soil_type_id integer
[ref:> soil_type.id] //I am not sure I like this here. Maybe morve to
field_sample_condition? field_sample_storage_location_id integer [ref:>
location_address.id] //Used to describe where the sample is now note text

indexes { resource_id //will we use this often enough to index?
//source_codename_id } }

Table field_storage_method [headercolor: #d35400]{ // LookupBase for
enum/ontology-like tables id int [pk, increment] name string [not null, unique]
description string uri string }

Table collection_method [headercolor: #d35400]{ // LookupBase for
enum/ontology-like tables id int [pk, increment] name string [not null, unique]
description string uri string }

Table harvest_method [headercolor: #d35400]{ // LookupBase for
enum/ontology-like tables id int [pk, increment] name string [not null, unique]
description string uri string }

Table processing_method [headercolor: #d35400]{ // LookupBase for
enum/ontology-like tables id int [pk, increment] name string [not null, unique]
description string uri string }

//consider moving this to the analysis table group Table physical_characteristic
[headercolor: #d35400]{ //Base entity id int [pk, increment] created_at datetime
[default: `current_timestamp`] updated_at datetime [default:
`current_timestamp`] etl_run_id string lineage_group_id int [ref: >
lineage_group.id] // field_sample_id integer [not null, ref: > field_sample.id]
particle_length decimal particle_width decimal particle_height decimal
particle_unit_id integer [ref:> unit.id] //Could add index in here }

Table soil_type [headercolor: #d35400] { // LookupBase for enum/ontology-like
tables id int [pk, increment] name string [not null, unique] description string
uri string //soil_location integer [ref: > geography.id] //not sure if this
should be in a different "Base" table }

Table ag_treatment [headercolor: #d35400] { // LookupBase for enum/ontology-like
tables id int [pk, increment] name string [not null, unique] description string
uri string }

Table field_sample_condition [headercolor: #d35400] { //Would like to find a
better name for this table, or maybe break it apart //Base entity id int [pk,
increment] created_at datetime [default: `current_timestamp`] updated_at
datetime [default: `current_timestamp`] etl_run_id string lineage_group_id int
[ref: > lineage_group.id] // field_sample_id int [not null, ref:>
field_sample.id] ag_treatment_id int [not null, ref:> ag_treatment.id]
last_application_date date [note: "if applicable"] treatment_amount_per_acre
float processing_method_id int [ref:> processing_method.id] }

Table location_soil_type [headercolor: #d35400] { //Base entity id int [pk,
increment] created_at datetime [default: `current_timestamp`] updated_at
datetime [default: `current_timestamp`] etl_run_id string lineage_group_id int
[ref: > lineage_group.id] //Domain specific location_id int [not null, ref:>
location_address.id] soil_type_id int [not null, ref:> soil_type.id] }

///////////////////////////////////////////////////////// ///////// UNITS
//////////////// ////////////////////////////////////////////////////////

Table unit { id int [pk, increment] name string [not null, unique] // e.g.,
"cm", "kg", "m3" description string //can be longform like centimeter,
kilograms, cubic meters uri url }

//////////////////////////////////////////////////////// ///////SAMPLE
PREPARATION/////////////
////////////////////////////////////////////////////////

Table preparation_method [headercolor: #F7AC5E] { //Base entity id int [pk,
increment] created_at datetime [default: `current_timestamp`] updated_at
datetime [default: `current_timestamp`] etl_run_id string lineage_group_id int
[ref: > lineage_group.id] // name string [note: "As Is, Knife Mill (2mm), Oven
Dry"] description text prep_method_abbrev_id integer [ref:-
preparation_method_abbreviation.id] prep_temp_c decimal //I feel like this
should just be in the method right? uri string //ideally a protocols.io linked
DOI drying_step boolean //I think this should also just be in the method
//method_ref_id integer //[ref: > references.reference_id] }

Table preparation_method_abbreviation [headercolor: #F7AC5E] { // LookupBase for
enum/ontology-like tables id int [pk, increment] name string [not null, unique]
description string uri string }

Table prepared_sample [headercolor: #f7ac5e] { //Base entity id int [pk,
increment] created_at datetime [default: `current_timestamp`] updated_at
datetime [default: `current_timestamp`] etl_run_id string lineage_group_id int
[ref: > lineage_group.id] // name string // this should correspond with
prepro_material_name in Gsheets. field_sample_id integer [not null, ref:-
field_sample.id] prep_method_id integer [not null, ref:- preparation_method.id]
//amount_before_drying decimal //amount_after_drying decimal prep_date date
//storage_location_id integer [ref: > location_address.id] //We may want this to
be location with a room. Need to ask James how specific the storage location is
for the samples cus in th Gsheets it is only the building //amount_remaining
decimal //amount_remaining_unit_id integer [ref:> unit.id] //amount_as_of_date
date preparer_id integer //[ref: > analysts_contact.analyst_id] note text

indexes { field_sample_id prep_method_id }

}

//////////////////////////////////////////////////////// ///////DATA SOURCES AND
METADATA///////////// ////////////////////////////////////////////////////////

Table data_source [headercolor: #990D0D] { //Base entity id int [pk, increment]
created_at datetime [default: `current_timestamp`] updated_at datetime [default:
`current_timestamp`] etl_run_id string lineage_group_id int [ref: >
lineage_group.id] // name string [not null] //a short english identifier for the
source, such as the in-text citation (e.g. "Smith 2019" "BT23" "ForageOne")
description text //purpose of the data maybe. Unabbreviated names
data_source_type_id int [not null, ref:- data_source_type.id] // Foreign key
referenceing source_types full_title string [not null] creator string subject
string publisher string contributor string date datetime type string [not null]
biocirv boolean // e.g. "External data" = FALSE, "Internal data" = TRUE format
string language string relation string temporal_coverage daterange //The spatial
or temporal topic of the resource. location_coverage int [ref:>
location_resolution.id] rights string uri string [not null] }

Table data_source_type [headercolor: #990D0D] { //Base entity id int [pk,
increment] created_at datetime [default: `current_timestamp`] updated_at
datetime [default: `current_timestamp`] etl_run_id string lineage_group_id int
[ref: > lineage_group.id] // source_type_id int [ref: > source_type.id] }

Table location_resolution [headercolor: #990D0D] { //nation, state, county,
region, etc // LookupBase for enum/ontology-like tables id int [pk, increment]
name string [not null, unique] //database, literature, internal, etc description
string uri string }

Table source_type [headercolor: #990D0D]{ // LookupBase for enum/ontology-like
tables id int [pk, increment] name string [not null, unique] //database,
literature, industry report, government report, etc description string uri
string }

Table file_object_metadata [headercolor: #990D0D] { //Base entity id int [pk,
increment] created_at datetime [default: `current_timestamp`] updated_at
datetime [default: `current_timestamp`] etl_run_id string lineage_group_id int
[ref: > lineage_group.id] // data_source_id int [ref: > data_source.id]
bucket_path string file_format string file_size int checksum_md5 string
checksum_sha256 string }

//THIS IS FOR LATER WHEN WE DO ANALYSIS RESULTS //analysis_result_file_object {
// analysis_result_id int [ref: > analysis_result.id] // file_object_id int
[ref: > file_object.id] // primary key (analysis_result_id, file_object_id) //}

///////////////////////// ////// METHODS, PARAMETERS, UNITS
/////////////////////////

Table method [headercolor: #F0B7B7] { //Base entity id int [pk, increment]
created_at datetime [default: `current_timestamp`] updated_at datetime [default:
`current_timestamp`] etl_run_id string lineage_group_id int [ref: >
lineage_group.id] //Domain fields name string [unique] method_abbrev_id int
[ref: > method_abbrev.id] // Foreign key referencing method_abbrevs
method_category_id int [ref: > method_category.id] // Foreign key referencing
method_categories method_standard_id int [ref: > method_standard.id] // Foreign
key referencing method_standards description text detection_limits text //maybe
make this substantial in the future source_id int [ref: > data_source.id]
//protocols.io

indexes { name } }

Table method_abbrev [headercolor: #F0B7B7] { // LookupBase for
enum/ontology-like tables id int [pk, increment] name string [not null, unique]
// e.g. ICP, Ult description string uri string }

Table method_category [headercolor: #F0B7B7] { //still need to better define
what this would be... // LookupBase for enum/ontology-like tables id int [pk,
increment] name string [not null, unique] //"ICP method, CompAna method, dry,
wet" description string uri string }

Table method_standard [headercolor: #F0B7B7] { // LookupBase for
enum/ontology-like tables id int [pk, increment] name string [not null, unique]
// Standard associated with the method (e.g., AOAC 997.02, TAPPI T203)
description string uri string }

Table parameter [headercolor:#F0B7B7] { //Base entity id int [pk, increment]
created_at datetime [default: `current_timestamp`] updated_at datetime [default:
`current_timestamp`] etl_run_id string lineage_group_id int [ref: >
lineage_group.id] // name string [not null, unique] //parameter_category_id
integer [ref: > parameter_catagory.id] //"Fermentation, Minerals, Elements,
Compositional Analysis, etc" standard_unit_id integer [ref : > unit.id]
//Expected unit of a result. Is this the right way to do this? Should we use a
different //table to facilitate the identification and coercing of mismathed
units across internal and external datasets? //alternate_units text [note: "JSON
array of alternative units"] //I think I have eled this in the parameter_units
bridge table calculated boolean [note:"if not calculated then it is measured
directly. E.g glucose vs glucan"] description text //typical_range_min decimal
//typical_range_max decimal }

Table parameter_catagory_parameter [headercolor: #F0B7B7] { id int [pk,
increment] parameter_id int [not null, ref: > parameter.id]
parameter_catagory_id int [not null, ref: > parameter_category.id] }

Table parameter_category [headercolor: #F0B7B7] { //need to better define //
LookupBase for enum/ontology-like tables id int [pk, increment] name string [not
null, unique] //[note: "Fermentation, Minerals, Elements, Compositional
Analysis, etc"] description string uri string }

Table parameter_unit [headercolor: #F0B7B7] { id integer [pk] parameter_id
integer [ref: > parameter.id] //contains the standard unit alternate_unit_id
integer [not null, ref:> unit.id] }

Ref: "experiment_prepared_sample"."id" <
"experiment_prepared_sample"."prepared_sample_id"

///////////////////////// ////// Experiments, Equipment
/////////////////////////

Table experiment { id int [pk, increment] // Primary key created_at datetime
[default: `current_timestamp`] // When this row was created updated_at datetime
[default: `current_timestamp`] // Last updated timestamp

// ETL tracking / provenance etl_run_id string [note: "ETL process that
generated this experiment row"] lineage_group_id int [ref: > lineage_group.id,
note: "Links to original source data (sheet, row, file, etc.)"]

// Domain-specific fields analyst_id int [note: "Person responsible for
experiment"] exper_start_date date [note: "Date the experiment started"]
exper_duration decimal [note: "Duration of experiment"] exper_duration_unit_id
int [ref: > unit.id, note: "Unit for exper_duration, e.g., days, hours"]
exper_location_id int [ref: > location_address.id, note: "Where the experiment
was performed"] description text [note: "Optional notes or description of the
experiment"] }

Table equipment [headercolor: #CDFC9F]{ // LookupBase for enum/ontology-like
tables id int [pk, increment] name string [not null, unique] // description
string uri string // equipment_location_id integer [ref: > location_address.id]
//from room can access building, affiliation, address, etc }

Table experiment_equipment [headercolor: #CDFC9F]{ id int [pk] experiment_id int
[not null, ref: > experiment.id] equipment_id int [not null, ref: >
equipment.id] }

Table experiment_analysis [headercolor: #CDFC9F] { id int [pk, increment]
experiment_id int [ref:> experiment.id] analysis_type_id int [ref:>
analysis_type.id] }

Table experiment_prepared_sample [headercolor: #CDFC9F] { id int [pk, increment]
experiment_id int [ref:> experiment.id] prepared_sample_id int [ref:>
prepared_sample.id] }

Table experiment_method [headercolor: #CDFC9F] { id int [pk] experiment_id int
[ref: > experiment.id] method_id int [ref: > method.id]

indexes { method_id experiment_id } } //======================================
// DATASET TABLE //======================================

//A dataset is defined by a publisher and the time //period over which it took
observations which are grouped //but non-redundant. //so that methodology and
observation space is the same.?

//Ex: LandIQ is a record_type but there are multiple years of //LandIQ data so
record_type is insufficient to differentiate //a polygon from 2020 and 2022.

//Ex. Phyllis2 is a publisher, but it releases data in sections //based on
analysis type so we will import "Phyllis 2 Proximate //analysis" "Phyllis 2
Ultimate Analysis" as datasets. //What is the problem though just have Phyllis2
as a dataset that //is an aggregation of those datasets?

//Ex: BioCirV is a publisher that takes data across a timeframe. //Should we
differentiate Aim1 and Aim2? I vote no.

Table dataset { id int [pk, increment] name string // Human-readable dataset
name record_type string [note: "Determines which child record table rows belong
to this dataset"] // e.g. "ultimate_record", "compositional_record"
//experiment_id int [ref: > experiment.id, note: "Nullable; only applies for
lab-produced datasets"] source_id int [ref:> data_source.id] start_date date
end_date date description text }

//=========================================================== // OBSERVATION
TABLE (parameter/value pairs)
//===========================================================

Table observation { id int [pk, increment] dataset_id int [ref: > dataset.id]

// Polymorphic link to child record table record_type string [note: "ENUM of
child record tables"] record_id int [note: "Points to ID in table defined by
record_type"]

parameter_id int [ref: > parameter.id] value decimal unit_id int [ref: >
unit.id]

// Optional dimensions (e.g., timepoint for timeseries data, wavelength,
replicate time) dimension_type_id int [ref: > dimension_type.id] dimension_value
decimal dimension_unit_id int [ref: > unit.id]

//observation_source_id int [ref: > data_source.id] note text

indexes { (dataset_id, record_id, parameter_id) } }

//=========================================================== // CHILD RECORD
TABLES – ANALYTICAL DATA
//===========================================================

//A record is the surrounding information needed to understand an observation.
//Record tables give context for the parameter + value + unit //from the
observation table. They explain which data groupings (samples, experiments,
//and datasets) that these observations belong to.

//A technical replicate is defined by a sample and a given experiment
//(analyst, on a day, at a time, on a machine)

//A sample replicate is defined by a sample and an analytical method

////////////////////////////////////////////////// ////// INTERNAL RECORD BASE
CLASS///////////////// //////////////////////////////////////////////////

//id int [pk, increment] //dataset_id int [ref: > dataset.id] //experiment_id
int [ref: > experiment.id] //resource_id int [ref:> resource.id] //sample_id int
[ref: > prepared_sample.id] //technical_replicate_no int //which replicate this
record represents //technical_replicate_total int //total number of replicates
for a sample //method_id int [ref: > method.id] //we suspect this will be
captured in the experiment_id //raw_data_id int [ref:> file_object_metadata.id]
//qc_pass boolean //note text

//////////////////////////////////////////////////

Table proximate_record { id int [pk, increment] dataset_id int [ref: >
dataset.id] experiment_id int [ref: > experiment.id] resource_id int [ref:>
resource.id] sample_id int [ref: > prepared_sample.id] technical_replicate_no
int //which replicate this record represents technical_replicate_total int
//total number of replicates for a sample method_id int [ref: > method.id] //we
suspect this will be captured in the experiment_id //equipment_id int [ref: >
equipment.id] //we suspect this will be captured in the experiment_id
//analyst_id int [ref: > contact.id] //we suspect this will be captured in the
experiment_id raw_data_id int [ref:> file_object_metadata.id] qc_pass boolean
note text }

Table ultimate_record { id int [pk, increment] dataset_id int [ref: >
dataset.id] experiment_id int [ref: > experiment.id] resource_id int [ref:>
resource.id] sample_id int [ref: > prepared_sample.id] technical_replicate_no
int //which replicate this record represents technical_replicate_total int
//total number of replicates for a sample method_id int [ref: > method.id]
//equipment_id int [ref: > equipment.id] //analyst_id int [ref: > contact.id]
raw_data_id int [ref:> file_object_metadata.id] qc_pass boolean note text }

Table compositional_record { id int [pk, increment] dataset_id int [ref: >
dataset.id] experiment_id int [ref: > experiment.id] resource_id int [ref:>
resource.id] sample_id int [ref: > prepared_sample.id] technical_replicate_no
int //which replicate this record represents technical_replicate_total int
//total number of replicates for a sample method_id int [ref: > method.id]
//equipment_id int [ref: > equipment.id] //analyst_id int [ref: > contact.id]
raw_data_id int [ref:> file_object_metadata.id] qc_pass boolean note text }

Table icp_record { id int [pk, increment] dataset_id int [ref: > dataset.id]
experiment_id int [ref: > experiment.id] resource_id int [ref:> resource.id]
sample_id int [ref: > prepared_sample.id] technical_replicate_no int //which
replicate this record represents technical_replicate_total int //total number of
replicates for a sample method_id int [ref: > method.id] //equipment_id int
[ref: > equipment.id] //analyst_id int [ref: > contact.id] raw_data_id int
[ref:> file_object_metadata.id] qc_pass boolean note text }

Table xrf_record { id int [pk, increment] dataset_id int [ref: > dataset.id]
experiment_id int [ref: > experiment.id] resource_id int [ref:> resource.id]
sample_id int [ref: > prepared_sample.id] technical_replicate_no int //which
replicate this record represents technical_replicate_total int //total number of
replicates for a sample method_id int [ref: > method.id] maybe_wavelength_nm
decimal ////might be in the method maybe_intensity decimal //might be in the
method maybe_energy_slope decimal //might be in the method maybe_energy_offset
decimal //might be in the method //equipment_id int [ref: > equipment.id]
//analyst_id int [ref: > contact.id] raw_data_id int [ref:>
file_object_metadata.id] qc_pass boolean note text }

Table xrd_record { id int [pk, increment] dataset_id int [ref: > dataset.id]
experiment_id int [ref: > experiment.id] resource_id int [ref:> resource.id]
sample_id int [ref: > prepared_sample.id] technical_replicate_no int //which
replicate this record represents technical_replicate_total int //total number of
replicates for a sample maybe_scan_low_nm int ////might be in the method
maybe_scan_high_nm int ////might be in the method method_id int [ref: >
method.id] //equipment_id int [ref: > equipment.id] //analyst_id int [ref: >
contact.id] raw_data_id int [ref:> file_object_metadata.id] qc_pass boolean note
text }

Table calorimetry_record { id int [pk, increment] dataset_id int [ref: >
dataset.id] experiment_id int [ref: > experiment.id] resource_id int [ref:>
resource.id] sample_id int [ref: > prepared_sample.id] technical_replicate_no
int //which replicate this record represents technical_replicate_total int
//total number of replicates for a sample method_id int [ref: > method.id]
//equipment_id int [ref: > equipment.id] //analyst_id int [ref: > contact.id]
raw_data_id int [ref:> file_object_metadata.id] qc_pass boolean note text }

Table ftnir_record { id int [pk, increment] dataset_id int [ref: > dataset.id]
experiment_id int [ref: > experiment.id] resource_id int [ref:> resource.id]
sample_id int [ref: > prepared_sample.id] technical_replicate_no int //which
replicate this record represents technical_replicate_total int //total number of
replicates for a sample method_id int [ref: > method.id] //equipment_id int
[ref: > equipment.id] //analyst_id int [ref: > contact.id] raw_data_id int
[ref:> file_object_metadata.id] qc_pass boolean note text }

Table rgb_record { id int [pk, increment] dataset_id int [ref: > dataset.id]
experiment_id int [ref: > experiment.id] resource_id int [ref:> resource.id]
sample_id int [ref: > prepared_sample.id] technical_replicate_no int //which
replicate this record represents technical_replicate_total int //total number of
replicates for a sample method_id int [ref: > method.id] //equipment_id int
[ref: > equipment.id] //analyst_id int [ref: > contact.id] raw_data_id int
[ref:> file_object_metadata.id] qc_pass boolean note text }

///////////////////////////////////// ////// AIM2 EXPERIMENTAL DATA
/////////////////////////////////////

Table pretreatment_record { id int [pk, increment] dataset_id int [ref: >
dataset.id] experiment_id int [ref: > experiment.id] resource_id int [ref:>
resource.id] sample_id int [ref: > prepared_sample.id] pretreatment_method int
[ref:> method.id] eh_method_id int [ref:> method.id] reaction_block_id int
block_position varchar temperature decimal replicate_no int analyst_id int
[ref:> contact.id] qc_pass boolean note text }

Table fermentation_record { id int [pk, increment] dataset_id int [ref: >
dataset.id] experiment_id int [ref: > experiment.id] resource_id int [ref: >
resource.id] //this is denormalized, but maybe necessary for external data
sample_id int [ref: > prepared_sample.id] strain_id int [ref:> strain.id]
pretreatement_method_id int [ref:> method.id] //decon method in gsheet
eh_method_id int [ref:> method.id] //enzymatic hydrolysis method replicate_no
int well_position varchar temperature decimal //ph decimal //Is this at the
beginning? End? agitation_rpm decimal vessel_id int [ref:> equipment.id]
analyte_detection_equipment_id int [ref:> equipment.id] analyst_id int [ref: >
contact.id] raw_data_id int [ref:> file_object_metadata.id] qc_pass boolean note
text }

Table gasification_record { id int [pk, increment] dataset_id int [ref: >
dataset.id] experiment_id int [ref: > experiment.id] resource_id int [ref: >
resource.id] //this is denormalized, but maybe necessary for external data
sample_id int [ref:> prepared_sample.id] feedstock_mass decimal bed_temperature
decimal gas_flow_rate decimal technical_replicate_no int analyst_id int [ref: >
contact.id] raw_data_id int [ref:> file_object_metadata.id] qc_pass boolean note
text }

Table autoclave_record { id int [pk, increment] dataset_id int [ref:>
dataset.id] experiment_id int [ref:> experiment.id] resource_id int [ref:>
resource.id] sample_id int [ref:> prepared_sample.id] technical_replicate_no int
analyst_id int [ref: > contact.id] raw_data_id int [ref:>
file_object_metadata.id] qc_pass boolean note text }

//=========================================================== // CHILD RECORD
TABLES – USDA DATA //===========================================================

//I want to create a base "usda_record" class that will be used for both
usda_census and usda_survey //records. I would also like to explore the class
also being applicable to usda_market type records, //although these are much
more different.

Table usda_census_record [headercolor: #ffc72f] { id int [pk, increment]
dataset_id int [ref: > dataset.id] geoid int [ref:> geography.geoid]
commodity_code int [ref: > usda_commodity.id] year int source_reference string
// this may be the same as any other source attribute note text }

Table usda_survey_record [headercolor: #ffc72f] { id int [pk, increment]
dataset_id int [ref: > dataset.id] geoid int [ref:> geography.geoid]
commodity_code int [ref: > usda_commodity.id] year int survey_program_id int
[ref: > usda_survey_program.id] survey_period string reference_month string
seasonal_flag boolean note text }

//=========================================================== // CHILD RECORD
TABLE – USDA MARKET NEWS
//===========================================================

Table usda_market_report [headercolor: #ffc72f]{ id int [pk, increment]

// IDENTIFIERS slug_id int [not null, note: "The constant MARS ID, e.g., 3667.
Defines the 'Series'."] slug_name string report_series_title string //e.g.
"Feedstuffs Report"

// FREQUENCY & ORIGIN frequency string // e.g., "Monthly", "Weekly" office_name
varchar office_city_id int [ref:> location_address.id] office_state_fips varchar
[ref:> geography.geoid] source int [ref : - data_source.id] //might be
unnecessary since data can be looked up by slug_id and data in this table

// Note: Splitting this table is NORMALIZATION. // It prevents repeating
'Monthly Feedstuffs Report' 10,000 times. }

Table usda_market_record [headercolor: #ffc72f] { id int [pk, increment]
report_id int [not null, ref: > usda_market_report.id] dataset_id int [ref:>
dataset.id] //office_name varchar //office_city_id int [ref:>
location_address.id] //office_state_fips varchar [ref:> geography.geoid]
report_begin_date datetime //This report refers to the report_end_date datetime
report_date datetime //not sure how this differs from the other dates, but it is
earlier... //published_date datetime commodity_id int [not null, ref: >
usda_commodity.id] //primary_crop_id int [not null, ref:> primary_crop.id]
//assumes we can control what USDA market data we input and import only data for
primary crops in our database. otherwise the "not null" designation may present
issue market_type_id int //[ref:> market_type.id] market_type_catagory varchar
//this could be normalized, but it is all just "summary" in the example data
//slug_id int //slug_name string //report_title string grp string
market_catagory_id int // [ref;> market_catagory.id] class string grade string
variety string protein_pct decimal application string pkg string // sale_type
string //"FOB" (Free on Board - buyer pays shipping) or "Delivered" (seller pays
shipping) price_unit_id int [ref:> unit.id] //price_min decimal //these all go
into the parameter unit observation table //price_max decimal //price_min_change
decimal //price_min_direction varchar //price_max_change decimal
//price_max_direction decimal //avg_price decimal //avg_price_year_ago decimal
freight string trans_mode string }

//=========================================================== // CHILD RECORD
TABLE – LAND IQ //===========================================================

//I think I may want to create a base "polygon" or "geometry" record type //for
geospatial records. Please log this and flag for discussion later.

Table landiq_record [headercolor: #808080] { id int [pk, increment] dataset_id
int [ref: > dataset.id] polygon_id int [ref: > polygon.id] main_crop int [ref: >
primary_crop.id] secondary_crop int [ref: > primary_crop.id] tertiary_crop int
[ref: > primary_crop.id] quaternary_crop int [ref: > primary_crop.id] confidence
int irrigated boolean acres float version string note text }

//=========================================================== // CHILD RECORD
TABLE – FACILITY/INFRASTRUCTURE DATA
//===========================================================

Table facility_record { id int [pk, increment] dataset_id int [ref: >
dataset.id] facility_name string location_id int [ref: > location_address.id]
capacity_mw decimal resource_id int [ref:> resource.id] //could have multiple
resources per facility. For example almond shells and hulls. operator string
start_year int note text }

//INFRASTRUCTURE RECORD SET PLACEHOLDER.

//These records are for now to be simply modeled as

//==================== TABLE GROUP =========================
//==================== INFRASTRUCTURE INDUSTRIAL DATASETS
=========================

Table infrastructure_biodiesel_plants [headercolor: #008B8B] { // two joined
datasets biodiesel_plant_id integer [pk] company varchar bbi_index integer //
blank for some companies city varchar state char(2) [note: "convert to state
abbreviation"] // some rows have whole names written out; reduce to
abbreviations capacity_mmg_per_y integer // should it be integer? feedstock
varchar [note: "multiselect"] // blank for some companies status varchar [note:
"select ; options listed are either 'operational' or 'idle'"] // blank for some
companies address varchar // blank for some companies coordinates varchar [note:
"currently string, convert to geometric point"] // blank for some companies
latitude decimal longitude decimal source text [note: "change to url later"] }

Table infrastructure_biosolids_facilities [headercolor: #008B8B] { // lots of
mixed all-caps and proper formatting biosolid_facility_id integer [pk]
report_submitted_date date // one row says "06-Kan-24" - correct typo and
convert to date latitude decimal longitude decimal facility varchar authority
varchar plant_type varchar [note: "multiselect"] aqmd varchar // some blank
entries. could also make multiselect if we had a unified format? e.g. "feather
river" and "feather river aqmd" is the same facility_address varchar // some
blank facility_city varchar // some blank state varchar(2) facility_zip varchar
// some blank facility_county varchar // some blank (make multiselect?)
mailing_street_1 varchar // some blank mailing_city varchar // some blank (make
multiselect?) mailing_state varchar(2) // some blank? mailing_zip varchar
biosolids_number varchar // add custom check alter - should be CALX######
biosolids_contact varchar biosolids_contact_phone varchar // convert to single
custom format biosolids_contact_email varchar // convert to single custom format
adwf decimal potw_biosolids_generated integer twtds_biosolids_treated integer //
very blank class_b_land_app integer // very blank class_b_applier varchar //
very blank class_a_compost integer // very blank class_a_heat_dried integer //
very blank class_a_other integer // very blank class_a_other_applier varchar //
very blank twtds_transfer_to_second_preparer int // very blank
twtds_second_preparer_name varchar [note: "sometimes multiple preparers are
reported along with respective amt of biosolids transferred"] adc_or_final_c
integer // very blank landfill integer landfill_name varchar // very blank
surface_disposal integer // VERY blank deepwell_injection varchar //I don't even
know what is this stored integer // has some random varchar content in there
longterm_treatment integer // very blank other integer // very blank
name_of_other varchar incineration integer Note: "probably could change to a
long format? a lot of blank fields and random columns near the bottom" }

Table infrastructure_cafo_manure_locations [headercolor: #008B8B] {
cafo_manure_id integer [pk] latitude decimal longitude decimal owner_name
varchar // very blank facility_name varchar address varchar town varchar state
varchar(2) zip varchar(5) animal varchar [note: "select"]
animal_feed_operation_type varchar [note:"select"] animal_units integer //
partially blank animal_count integer // partially blank; also some of them end
with 333, 667, or 000? are these calculations? manure_total_solids decimal
[note: "million gallons a year"] source text [note: "change to url later"]
date_accessed date }

Table infrastructure_ethanol_biorefineries [headercolor: #008B8B] {
ethanol_biorefinery_id integer [pk] name varchar city varchar state varchar(2)
address varchar type varchar [note: "multiselect"] capacity_mgy integer
production_mgy integer constr_exp integer // don't know what this is }

Table infrastructure_landfills [headercolor: #008B8B] { project_int_id integer
project_id varchar [pk] ghgrp_id varchar landfill_id integer landfill_name
varchar state varchar(2) physical_address text city varchar county varchar
zip_code varchar latitude decimal longitude decimal ownership_type varchar
[note: "select, either Public or Private"] landfill_owner_orgs varchar
landfill_opened_year date [note: "year only; should it be int or date?"]
landfill_closure_year date [note: "year only; should it be int or date?"]
landfill_status varchar [note: "select"] waste_in_place integer [note: "in
tons"] waste_in_place_year date [note: "assuming year collected?"]
lfg_system_in_place boolean [note: "currently yes/no"] lfg_collected decimal
[note: "in mmscfd"] lfg_flared decimal [note: "in mmscfd"] project_status
varchar [note: "select"] project_name varchar [note: "select?"]
project_start_date date project_shutdown_date date // very empty
project_type_category varchar [note: "select"] lfg_energy_project_type varchar
[note: "select"] rng_delivery_method varchar actual_mw_generation decimal
rated_mw_capacity decimal lfg_flow_to_project decimal [note: "mmscfd"]
direct_emission_reductions decimal [note: "MMTCO2e/yr for current year"]
avoided_emission_reductions decimal [note: "MMTCO2e/yr for current year"] }

Table infrastructure_livestock_anaerobic_digesters [headercolor: #008B8B] {
digester_id integer [pk] project_name varchar project_type varchar [note:
"select or multiselect"] city varchar state varchar(2) digester_type varchar
[note: "select or multiselect"] profile text [note: "url"] year_operational date
[note: "year only"] animal_type_class varchar [note: "select"] animal_types
varchar [note: "multiselect"] pop_feeding_digester varchar [note: "either single
integer or multiple integers separated by a semicolon"] // is this even
necessary? total_pop_feeding_digester integer cattle integer dairy integer
poultry integer swine integer codigestion varchar [note: "multiselect"]
biogas_generation_estimate integer [note: "cu/ft per day"] electricity_generated
integer [note: "kWh/yr"] biogas_end_uses varchar [note: "multiselect"]
methane_emission_reductions integer [note: "metric tons CO2e/yr"] latitude
decimal longitude decimal }

Table infrastructure_saf_and_renewable_diesel_plants [headercolor: #008B8B] {
ibcc_index integer [pk] company varchar city varchar state varchar(2) country
varchar capacity varchar [note: "mmg per yr; mostly integers with some strings
in the format '#/#' where # is a number"] feedstock varchar [note:
"multiselect"] products varchar [note: "multiselect"] status varchar [note:
"multiselect"] address text coordinates text latitude decimal longitude decimal
}

Table infrastructure_wastewater_treatment_plants [headercolor: #008B8B] {
plant_id integer [pk] name varchar state varchar(2) codigestion boolean [note:
"currently 0/1"] flow_design_adjusted decimal [note: "MGD"] flow_average decimal
[note: "MGD"] biosolids decimal [note: "BDT/yr"] excess_flow decimal [note:
"MGD"] biogas_utilized boolean [note: "currently 0/1"] flaring boolean [note:
"currently 0/1"] excess_mass_loading_rate decimal [note: "BDT/d"]
excess_mass_loading_rate_wet decimal [note: "tons per day?"] methane_production
decimal [note: "cubic ft/d"] energy_content decimal [note: "BTU/d"] electric_kw
decimal thermal_mmbtu_d decimal electric_kwh decimal thermal_annual_mmbtu_y
decimal anaerobic_digestion_facility varchar // partially blank county varchar
// partially blank dayload_bdt decimal // for ca only dayload decimal // what's
the difference between this and the prev one? for ca only equivalent_generation
decimal // for ca only facility_type varchar [note: "select"] // for ca only
feedstock varchar [note: "select"] // for ca only type varchar [note: "select"]
// for ca only city varchar latitude decimal longitude decimal zipcode varchar }

Table infrastructure_combustion_plants [headercolor: #008B8B] { combustion_fid
integer [pk] objectid integer // several object ids are 0 status varchar [note:
"select: active, retired, unknown"] // has a random 0 in there. does that mean
unknown city varchar name varchar county varchar equivalent_generation decimal
np_mw decimal // what does this mean? look up cf decimal // what does this mean?
yearload integer [note: "in bdt"] fuel varchar [note: "select WDS, MSW, AB"]
notes varchar [note: "optional field, blanks replaced by zeroes"] type varchar
[note: "all COMB_pts; is it necessary"] wkt_geom text geom point latitude
decimal longitude decimal }

Table infrastructure_district_energy_systems [headercolor: #008B8B] { des_fid
integer [pk] cbg_id integer name varchar system varchar // partially blank
object_id integer city varchar state varchar(2) primary_fuel varchar [note:
"selection of NG, E/Electric"] secondary_fuel varchar [note: "selection"] //
partially blank usetype varchar [note: "selection btwn College,
Downtown/Utility, Healthcare, Airport, Gov, Military"] cap_st decimal // what
does this mean? cap_hw decimal // what does this mean? cap_cw decimal // what
does this mean? chpcg_cap decimal // what does this mean? excess_c decimal
[note: 'all zeroes'] excess_h decimal [note: 'all zeroes'] type varchar [note:
'all DES_CBG'] wkt_geom text geom point latitude decimal longitude decimal }

Table infrastructure_food_processing_facilities [headercolor: #008B8B] {
processing_facility_id integer [pk] address varchar county varchar city varchar
company varchar join_count integer // unsure if this is necessary. could omit?
master_type varchar [note: 'select; this is the main crop'] state varchar(2)
subtype varchar [note: 'select; this is also crop/product type'] target_fid
integer // lots of zeroes processing_type varchar [note: 'select'] zip varchar
type varchar [note: 'all PROC'] // unsure if this is needed wkt_geom text geom
point latitude decimal longitude decimal }

Table infrastructure_msw_to_energy_anaerobic_digesters [headercolor: #008B8B] {
wte_id integer [pk] city varchar county varchar equivalent_generation decimal //
note: number stored as text feedstock varchar [note: 'multiselect'] dayload
decimal // note: number stored as text dayload_bdt decimal // note: number
stored as text facility_type varchar [note: 'select'] status varchar [note:
'select'] notes text source text type varchar [note: 'all W2E_pts'] // unsure if
needed wkt_geom text geom point latitude decimal longitude decimal }

//=========================================================== // CHILD RECORD
TABLE – BT23 //===========================================================

Table billion_ton_2023_record [headercolor: #EB801B] { id int [pk, increment]
subclass_id int [ref:> resource_subclass.id] resource_id int [ref:> resource.id]
geoid varchar [ref:> geography.geoid] county_square_miles float model_name
varchar //enumerated list with POLYSIS, NASS, etc. scenario_name varchar
//Enumerated list of near-term, mature-market, etc price_offered_usd decimal
production int production_unit_id int [ref:> unit.id] btu_ton int
production_energy_content int energy_content_unit_id int [ref:> unit.id]
product_density_dtpersqmi decimal land_source varchar }

///////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////// Table
usda_domain [headercolor: #ffc72f] { //domain still needs linkage! id int [pk,
increment] name string [not null, unique] description string uri string }

// Table usda_commodity [headercolor: #ffc72f] { // id int [pk, increment] //
name string [not null, unique] // description string // uri string // }

// Table usda_commodity_to_primary_crop [headercolor: #ffc72f] { //
usda_commodity_id int [ref: > usda_commodity.id] // primary_crop_id int [ref: >
primary_crop.id] // }

Table usda_statistic_category [headercolor: #ffc72f] { id int [pk, increment]
name string [not null, unique] description string uri string }

Table usda_survey_program [headercolor: #ffc72f] { id int [pk, increment] name
string [not null, unique] description string uri string }

Table dimension_type [headercolor: #A15CF5] { id int [pk, increment] name string
[not null, unique, note: "E.g., TIMEPOINT, WAVELENGTH, DEPTH"] description text
uri string }

Table analysis_type [headercolor: #A15CF5] { //we may want to be careful
difference between analysis and methods // LookupBase for enum/ontology-like
tables id int [pk, increment] name string [not null, unique, note: "X-Ray
Fluorescence analysis, Proximate analysis, Chemical Composition, Fermentation
Profile, etc"] // description string uri string // }

Table polygon [headercolor: #808080] { id int [pk] geoid string [ref: >
geography.geoid] geom geometry }

Table strain { // LookupBase for enum/ontology-like tables id int [pk,
increment] name string [not null, unique, note: "X-Ray Fluorescence analysis,
Proximate analysis, Chemical Composition, Fermentation Profile, etc"] //
parent_strain_id int [ref:> strain.id, note: "recursive"] description string uri
string //

}

# // ========================================== // USDA HIERARCHY & MAPPING //

TableGroup "Resource Ontology Mapping" [color: #5D6D7E] { usda_commodity
resource_usda_commodity_map // usda_term_map // <--- The Dictionary (Raw Text ->
Clean USDA Node)

}

Table usda_commodity { // LookupBase id int [pk, increment] name string [not
null] // e.g., "Almonds", "Tree Nuts", "Rice, Long Grain" usda_source string //
"usda_source" = Who OWNS this official definition? // - "NASS": It is a census
crop (e.g., Almonds). // - "AMS": It is a market term not tracked by NASS (e.g.,
Almond Hulls). usda_code string [note: "The official code used by USDA API"]

// The Cleanup Mechanism (Self-Referencing Hierarchy) parent_commodity_id int
[ref: > usda_commodity.id, note: "If this is 'Almonds Hulls', parent might be
'Almonds'. There might be another row where commodity code is 'Almonds', and its
parent would be 'Tree Nuts'. 'Tree Nuts' would have NULL listed for parent."]
//Gemini has promised that the USDA NASS API already has structured commodity
relations so it should be a programmable task.

description string uri string

Note: '''

# ETL INGESTION RULE

1. **Ingest NASS First:** The NASS API is the primary source of truth.
   Programmatically populate this table using NASS "Group" -> "Commodity" ->
   "Class" hierarchy.
2. **Ingest AMS Second:** The AMS API (Market Data) is messy. - When Python
   encounters a term in AMS (e.g., "Almond Hulls"), it must check this table. -
   If the term exists (from NASS), link to it. - If the term is NEW, create a
   new node here with usda_source = "AMS". - **Manual Step:** A human must
   periodically review new "AMS" nodes and link them to their NASS parent (e.g.,
   Link "Almond Hulls" -> "Almonds"). ''' }

Table usda_term_map { id int [pk, increment]

// THE INPUT (The Messy Reality) source_system string [note: " 'NASS' or 'AMS'
"] // "source_system" = Where did we FIND this specific messy text string. // We
need this so if we re-run the ingestion script, we know which rules apply (NASS
data is prioritized, AMS data is referenced and then added if not already
captured) source_context string [note: "For AMS: The Slug ID (e.g. 3667). For
NASS: The Group."] // "source_context" = The container where we found it. // -
For NASS: The Group Name (e.g., "Tree Nuts"). // - For AMS: The Slug ID (e.g.,
"3668" = "Monthly National Grain and Oilseed Processor Feedstuff Report").
raw_term string [not null, note: "The exact string from the API, e.g., 'Hulls',
'Hull/Shell Mix'"]

// THE OUTPUT (The Decision) usda_commodity_id int [ref: > usda_commodity.id]
//We review this manually.

// METADATA is_verified boolean [default: false] //Note whether we've confirmed
mapping note text }

Table resource_usda_commodity_map { id int [pk, increment]

// 1. THE INTERNAL TARGET (Who is asking?) // We allow linking to EITHER a
specific resource OR a general crop resource_id int [ref: > resource.id, null]
// Specific: "Almond Hulls" primary_crop_id int [ref: > primary_crop.id, null]
// General: "Almonds"

// 2. THE EXTERNAL SOURCE (Who has the data?) usda_commodity_id int [ref: >
usda_commodity.id, not null]

// 3. THE LOGIC (How good is the match?) match_tier string [not null, note:
"ENUM: 'DIRECT_MATCH', 'CROP_FALLBACK', 'AGGREGATE_PARENT'"]

// Metadata created_at datetime [default: `current_timestamp`] note text [note:
"Explanation of why this link was made"]

// LOGIC: A row must have EITHER a resource_id OR a primary_crop_id, but not
both null. }

///////////////////////////////////////////////////////////// ////////////
PEOPLE //////////////
////////////////////////////////////////////////////////////

Table contact { id int [pk] first_name varchar last_name varchar email varchar
[unique] affiliation varchar //maybe link to an enumerated list }

Table provider { id int [pk] codename string }
