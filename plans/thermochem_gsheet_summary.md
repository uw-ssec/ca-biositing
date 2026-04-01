# GSheet Inventory: Aim 2-Thermochem Conversion Data-BioCirV

## 01-Summaries

- **Rows**: 0
- **Columns**:

## 00-Aim2-readme

- **Rows**: 46
- **Columns**: This file provides a data collection location for conversion
  analysis via the platforms identified by the BioCirV proposal or thereafter.,

## 00-Aim2-SheetImprovements

- **Rows**: 9
- **Columns**: item_no, Improvement, location, status, who, description

## 01-ThermoExperiment

- **Rows**: 15
- **Columns**: Experiment_GUID, Therm_exp_id, Thermo_Exp_title, Resource,
  Prepared_sample, Method_id, Reactor_id, Created_at, Updated_at, Analyst_email,
  Note, raw_data_url, Other_note

## 02-ThermoData

- **Rows**: 542
- **Columns**: Rx_UUID, RxID, Experiment_id, Resource, Therm_unique_id,
  Material_Type_DELETE, Prepared_sample, Material_type, Preparation_method,
  Reactor_id, Material_parameter_id_rep_no, Repl_no, Reaction_vial_id,
  Parameter, Value, Unit, qc_result, Notes, Experiment_setup_url, raw_data_url,
  Analysis_type, Experiment_date, Analyst_email

## 01.2-ReactionSetup

- **Rows**: 24
- **Columns**: Reaction_GUID, Rxn-ID Next = Rxn-025, Position_ID,
  Reaction_block_ID, material_types, Prepro_material_name, Decon_methods,
  EH_methods, Date, Operator, URL_to_experimental_setup

## Pivot Table 1

- **Rows**: 1
- **Columns**: , Columns

## 03-ThermoMethods

- **Rows**: 3
- **Columns**: Decon_UUID, Th-ID, Thermo_method_title,
  Thermo_unique_method_name, Char_length, Hours, Temp_profile,
  Thermo_Procedure_description, Link_to_Thermo_protocol, Notes

## 04-ThermoReactors

- **Rows**: 6
- **Columns**: Reaction_GUID, Reactor_ID, Name, Description, Note

## 01.2-Thermochem

- **Rows**: 0
- **Columns**:

## 01.3-Autoclave

- **Rows**: 0
- **Columns**:

## 01.4-Compost

- **Rows**: 0
- **Columns**:

## 05-ThermoParameters

- **Rows**: 23
- **Columns**: Para_UUID, Par-ID, Name, Parameter_category, Parameter_abbrev,
  Unit, Unit_safename, Process, Product_name, Description, Thermo_parameter_note

## 06-Aim1-Material_Types

- **Rows**: 97
- **Columns**: Resources*UUID_072, Material_name_no, mat_number, Resource,
  Description, Resource_inits, Resource_code, Primary_ag_product,
  Resource_class, Resource_subclass, Resource_description, Count_of_collections,
  Material_priority, Resource_annual_BDT_NSJV, %\_of_all_NSJV_byproduct_biomass,
  Logistical_maturity*(1-5), Relationship*score*(1-5), %_water_range_"lo*-\_hi",
  %\_ash_range*"lo\_-_hi", Moisture,\_Ash,\_Other_gross_charx_of_composition?,
  Resource_target_biochem, Resource_target_thermochem,
  Resource_target_autoclave, Resource_target_compost,
  Resource_glucan_typical_ranges, Resource_xylan_typical_ranges,
  Resource_glucose_typical_ranges, Resource_xylose_typical_ranges,
  Resource_lignin_typical_ranges, Resource_ash_typical_ranges,
  Resource_moisture_typical_ranges, Resource_pectins_typical_ranges,
  Resource_fat_content, Resource_protein_content

## 07-Aim1-Preprocessing

- **Rows**: 492
- **Columns**: UUID, Record_ID, Resource, Sample_name, Source_codename,
  Preparation_method, Prepared_sample, Storage_cond, Prep_temp_C,
  Amount_before_drying_g, Drying_step, Amount_after_drying_g, Preparation_date,
  Storage_location_code, Amount_remaining_g, Amount_as_of_date, Analyst_email,
  Note, Analyze_status, Prox_prepro_count, XRF_prepro_count, Cmp_prepro_count,
  XRD_prepro_count, ICP_prepro_count, Cal_prepro_count, Ult_prepro_count,
  FTNIR_prepro_count, RGB_prepro_count
