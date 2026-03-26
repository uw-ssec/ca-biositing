# Thermochemical Conversion ETL Transformation Planning

This document provides the necessary details for planning the transformation and
loading steps of the Thermochemical Conversion data.

## Extraction Layer

**Source File:**
`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/extract/thermochem_data.py`
**Google Sheet:** `Aim 2-Thermochem Conversion Data-BioCirV`

### Extractor Functions & Worksheet Mapping

| Function Name         | Worksheet Name           | Description                                 |
| :-------------------- | :----------------------- | :------------------------------------------ |
| `thermo_experiment`   | `01-ThermoExperiment`    | Core experiment metadata                    |
| `thermo_data`         | `02-ThermoData`          | Primary observation/result data             |
| `reaction_setup`      | `01.2-ReactionSetup`     | Detailed reaction parameters                |
| `thermo_methods`      | `03-ThermoMethods`       | Method definitions and procedures           |
| `thermo_reactors`     | `04-ThermoReactors`      | Reactor hardware information                |
| `thermo_parameters`   | `05-ThermoParameters`    | Parameter and unit definitions              |
| `aim1_material_types` | `06-Aim1-Material_Types` | Aim 1 Reference: Material characteristics   |
| `aim1_preprocessing`  | `07-Aim1-Preprocessing`  | Aim 1 Reference: Sample preparation details |

---

## Field Reference (Schema)

### 1. Core Data & Experiments

#### `01-ThermoExperiment` (Experiment Metadata)

- `Experiment_GUID`
- `Therm_exp_id`
- `Thermo_Exp_title`
- `Resource` (Likely joins to `public.resource`)
- `Prepared_sample` (Likely joins to `public.prepared_sample`)
- `Method_id` (Joins to `03-ThermoMethods`)
- `Reactor_id` (Joins to `04-ThermoReactors`)
- `Created_at`
- `Updated_at`
- `Analyst_email`
- `Note`
- `raw_data_url`
- `Other_note`

#### `02-ThermoData` (Observations)

- `Rx_UUID`
- `RxID`
- `Experiment_id` (Joins to `01-ThermoExperiment`)
- `Resource`
- `Therm_unique_id`
- `Material_Type_DELETE` (Ignore)
- `Prepared_sample`
- `Material_type`
- `Preparation_method`
- `Reactor_id`
- `Material_parameter_id_rep_no`
- `Repl_no`
- `Reaction_vial_id`
- `Parameter` (Joins to `05-ThermoParameters`)
- `Value`
- `Unit` (Joins to `public.unit` or `05-ThermoParameters`)
- `qc_result`
- `Notes`
- `Experiment_setup_url`
- `raw_data_url`
- `Analysis_type`
- `Experiment_date`
- `Analyst_email`

---

### 2. Setup & Infrastructure

#### `01.2-ReactionSetup` (Reaction Details)

- `Reaction_GUID`
- `Rxn-ID` (Note: Header in sheet includes "Next = Rxn-025")
- `Position_ID`
- `Reaction_block_ID`
- `material_types`
- `Prepro_material_name`
- `Decon_methods`
- `EH_methods`
- `Date`
- `Operator`
- `URL_to_experimental_setup`

#### `03-ThermoMethods` (Method Definitions)

- `Decon_UUID`
- `Th-ID`
- `Thermo_method_title`
- `Thermo_unique_method_name`
- `Char_length`
- `Hours`
- `Temp_profile`
- `Thermo_Procedure_description`
- `Link_to_Thermo_protocol`
- `Notes`

#### `04-ThermoReactors` (Hardware)

- `Reaction_GUID`
- `Reactor_ID`
- `Name`
- `Description`
- `Note`

#### `05-ThermoParameters` (Parameters & Units)

- `Para_UUID`
- `Par-ID`
- `Name`
- `Parameter_category`
- `Parameter_abbrev`
- `Unit`
- `Unit_safename`
- `Process`
- `Product_name`
- `Description`
- `Thermo_parameter_note`

---

### 3. Aim 1 Reference Data (Integrated)

#### `06-Aim1-Material_Types`

- Fields related to resource classification: `Resource`, `Primary_ag_product`,
  `Resource_class`, `Resource_subclass`.
- Composition typicals: `glucan`, `xylan`, `lignin`, `ash`, `moisture`,
  `fat_content`, `protein_content`.

#### `07-Aim1-Preprocessing`

- Fields related to sample preparation: `Sample_name`, `Preparation_method`,
  `Prep_temp_C`, `Drying_step`.
- Inventory tracking: `Amount_remaining_g`, `Storage_location_code`.

## Next Steps for Transformation

1.  **Normalization**: Map `Resource` and `Prepared_sample` strings to their
    respective IDs in the database using `name_id_swap.py`.
2.  **Observation Mapping**: Transform `02-ThermoData` into the
    `public.observation` format.
3.  **Entity Transformation**: Map `01-ThermoExperiment` to the relevant
    SQLModel (e.g., `ThermochemExperiment` - check if it exists or needs
    creation).
4.  **Parameter Alignment**: Ensure `05-ThermoParameters` aligns with existing
    `public.parameter` and `public.unit` tables.
