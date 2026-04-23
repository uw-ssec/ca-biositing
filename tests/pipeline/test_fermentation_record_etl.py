"""
Test suite for Fermentation Record ETL pipeline (Phase 3).

Tests the fermentation_record transform with new method fields:
- decon_method (pretreatment_method_id)
- eh_method (eh_method_id)
"""

import pytest
import pandas as pd
import pathlib
import inspect


class TestFermentationRecordTransform:
    """Test the transform step for fermentation records with new method fields."""

    def test_transform_module_exists(self):
        """Verify that the fermentation_record transform module can be imported."""
        from ca_biositing.pipeline.etl.transform.analysis import fermentation_record
        assert fermentation_record is not None
        assert hasattr(fermentation_record, 'transform_fermentation_record')

    def test_decon_method_in_normalize_columns(self):
        """Verify that decon_method is in the normalize_columns dictionary."""
        from ca_biositing.pipeline.etl.transform.analysis.fermentation_record import transform_fermentation_record
        source = inspect.getsource(transform_fermentation_record.fn)
        assert 'decon_method' in source
        assert "'decon_method': (Method, 'name')" in source

    def test_eh_method_in_normalize_columns(self):
        """Verify that eh_method is in the normalize_columns dictionary."""
        from ca_biositing.pipeline.etl.transform.analysis.fermentation_record import transform_fermentation_record
        source = inspect.getsource(transform_fermentation_record.fn)
        assert 'eh_method' in source
        assert "'eh_method': (Method, 'name')" in source

    def test_decon_method_rename_mapping(self):
        """Verify that decon_method_id maps to pretreatment_method_id."""
        from ca_biositing.pipeline.etl.transform.analysis.fermentation_record import transform_fermentation_record
        source = inspect.getsource(transform_fermentation_record.fn)
        # Check that the rename logic includes the mapping
        assert "'decon_method': 'pretreatment_method_id'" in source

    def test_eh_method_rename_mapping(self):
        """Verify that eh_method_id maps to eh_method_id."""
        from ca_biositing.pipeline.etl.transform.analysis.fermentation_record import transform_fermentation_record
        source = inspect.getsource(transform_fermentation_record.fn)
        # Check that the rename logic includes the mapping
        assert "'eh_method': 'eh_method_id'" in source

    def test_strain_rename_mapping(self):
        """Verify that strain_id maps to strain_id."""
        from ca_biositing.pipeline.etl.transform.analysis.fermentation_record import transform_fermentation_record
        source = inspect.getsource(transform_fermentation_record.fn)
        # Check that the rename logic includes the mapping
        assert "'strain': 'strain_id'" in source

    def test_transform_normalize_columns_structure(self):
        """Test that normalize_columns dict is properly structured for method fields."""
        from ca_biositing.pipeline.etl.transform.analysis.fermentation_record import transform_fermentation_record
        source = inspect.getsource(transform_fermentation_record.fn)
        # Verify the structure includes both Method normalizations
        assert "'decon_method': (Method, 'name')" in source
        assert "'eh_method': (Method, 'name')" in source


class TestFermentationRecordModel:
    """Test the FermentationRecord model with new method fields."""

    def test_fermentation_record_has_pretreatment_method_id(self):
        """Verify FermentationRecord model has pretreatment_method_id field."""
        from ca_biositing.datamodels.models.aim2_records.fermentation_record import FermentationRecord
        assert hasattr(FermentationRecord, 'pretreatment_method_id')

    def test_fermentation_record_has_eh_method_id(self):
        """Verify FermentationRecord model has eh_method_id field."""
        from ca_biositing.datamodels.models.aim2_records.fermentation_record import FermentationRecord
        assert hasattr(FermentationRecord, 'eh_method_id')

    def test_fermentation_record_has_strain_id(self):
        """Verify FermentationRecord model has strain_id field."""
        from ca_biositing.datamodels.models.aim2_records.fermentation_record import FermentationRecord
        assert hasattr(FermentationRecord, 'strain_id')

    def test_pretreatment_method_id_is_foreign_key(self):
        """Verify pretreatment_method_id is a foreign key to method table."""
        from ca_biositing.datamodels.models.aim2_records.fermentation_record import FermentationRecord
        # Check the field definition exists
        field_info = FermentationRecord.model_fields.get('pretreatment_method_id')
        assert field_info is not None
        assert getattr(field_info, "foreign_key", None) == "method.id"

    def test_eh_method_id_is_foreign_key(self):
        """Verify eh_method_id is a foreign key to method table."""
        from ca_biositing.datamodels.models.aim2_records.fermentation_record import FermentationRecord
        # Check the field definition exists
        field_info = FermentationRecord.model_fields.get('eh_method_id')
        assert field_info is not None
        assert getattr(field_info, "foreign_key", None) == "method.id"

    def test_strain_id_is_foreign_key(self):
        """Verify strain_id is a foreign key to strain table."""
        from ca_biositing.datamodels.models.aim2_records.fermentation_record import FermentationRecord
        # Check the field definition exists
        field_info = FermentationRecord.model_fields.get('strain_id')
        assert field_info is not None
        assert getattr(field_info, "foreign_key", None) == "strain.id"

    def test_method_model_has_duration(self):
        """Verify Method model has duration field."""
        from ca_biositing.datamodels.models.methods_parameters_units.method import Method

        assert hasattr(Method, 'duration')


class TestMvBiomassFermentationView:
    """Test the mv_biomass_fermentation view with new method fields."""

    def test_view_module_exists(self):
        """Verify that the view module can be imported."""
        from ca_biositing.datamodels.data_portal_views import mv_biomass_fermentation
        assert mv_biomass_fermentation is not None

    def test_view_source_file_references_pretreatment_method_id(self):
        """Verify that mv_biomass_fermentation.py source file contains pretreatment_method_id."""
        view_file = pathlib.Path(__file__).parent.parent.parent / "src/ca_biositing/datamodels/ca_biositing/datamodels/data_portal_views/mv_biomass_fermentation.py"
        source = view_file.read_text()
        # The view should join on pretreatment_method_id
        assert 'pretreatment_method_id' in source

    def test_view_source_file_references_eh_method_id(self):
        """Verify that mv_biomass_fermentation.py source file contains eh_method_id."""
        view_file = pathlib.Path(__file__).parent.parent.parent / "src/ca_biositing/datamodels/ca_biositing/datamodels/data_portal_views/mv_biomass_fermentation.py"
        source = view_file.read_text()
        # The view should join on eh_method_id
        assert 'eh_method_id' in source

    def test_view_source_file_has_aliases(self):
        """Verify that mv_biomass_fermentation.py uses PM and EM aliases for Method table."""
        view_file = pathlib.Path(__file__).parent.parent.parent / "src/ca_biositing/datamodels/ca_biositing/datamodels/data_portal_views/mv_biomass_fermentation.py"
        source = view_file.read_text()
        # Should have PM (pretreatment method) and EM (enzyme method) aliases
        assert 'PM = aliased(Method' in source
        assert 'EM = aliased(Method' in source

    def test_view_source_file_labels_pretreatment_method(self):
        """Verify that mv_biomass_fermentation.py labels pretreatment_method correctly."""
        view_file = pathlib.Path(__file__).parent.parent.parent / "src/ca_biositing/datamodels/ca_biositing/datamodels/data_portal_views/mv_biomass_fermentation.py"
        source = view_file.read_text()
        # Should label PM.name as pretreatment_method
        assert 'PM.name.label("pretreatment_method")' in source

    def test_view_source_file_labels_enzyme_method(self):
        """Verify that mv_biomass_fermentation.py labels enzyme_name correctly."""
        view_file = pathlib.Path(__file__).parent.parent.parent / "src/ca_biositing/datamodels/ca_biositing/datamodels/data_portal_views/mv_biomass_fermentation.py"
        source = view_file.read_text()
        # Should label EM.name as enzyme_name
        assert 'EM.name.label("enzyme_name")' in source

    def test_view_source_file_labels_elapsed_time(self):
        """Verify that mv_biomass_fermentation.py projects elapsed_time from methods."""
        view_file = pathlib.Path(__file__).parent.parent.parent / "src/ca_biositing/datamodels/ca_biositing/datamodels/data_portal_views/mv_biomass_fermentation.py"
        source = view_file.read_text()

        assert 'ELAPSED_TIME = func.coalesce(PM.duration, EM.duration)' in source
        assert 'ELAPSED_TIME.label("elapsed_time")' in source


class TestAim2BioconversionFlow:
    """Test the Aim 2 flow startup ordering for fermentation extraction."""

    def test_methods_extract_runs_before_fermentation_extract(self):
        flow_file = pathlib.Path(__file__).parent.parent.parent / "src/ca_biositing/pipeline/ca_biositing/pipeline/flows/aim2_bioconversion.py"
        source = flow_file.read_text()

        methods_call = "bioconversion_methods.extract()"
        fermentation_call = "bioconversion_data.extract()"

        assert methods_call in source
        assert fermentation_call in source
        assert source.index(methods_call) < source.index(fermentation_call)

    def test_methods_are_loaded_before_fermentation_extract(self):
        flow_file = pathlib.Path(__file__).parent.parent.parent / "src/ca_biositing/pipeline/ca_biositing/pipeline/flows/aim2_bioconversion.py"
        source = flow_file.read_text()

        load_call = "load_method(method_load_df)"
        fermentation_call = "fermentation_raw = bioconversion_data.extract()"

        assert load_call in source
        assert fermentation_call in source
        assert source.index(load_call) < source.index(fermentation_call)

    def test_method_id_column_maps_to_method_name(self):
        flow_file = pathlib.Path(__file__).parent.parent.parent / "src/ca_biositing/pipeline/ca_biositing/pipeline/flows/aim2_bioconversion.py"
        source = flow_file.read_text()

        assert "method_id_col" in source
        assert "col.lower().strip() == 'method_id'" in source
        assert "pd.DataFrame({'name': methods_df[method_id_col]})" in source

    def test_time_h_column_maps_to_duration(self):
        flow_file = pathlib.Path(__file__).parent.parent.parent / "src/ca_biositing/pipeline/ca_biositing/pipeline/flows/aim2_bioconversion.py"
        source = flow_file.read_text()

        assert "col.lower().strip() == 'time_h'" in source
        assert "method_load_df['duration'] = methods_df[time_col]" in source


class TestMethodLoadTask:
    """Test the method metadata loader task surface."""

    def test_method_load_task_module_exists(self):
        from ca_biositing.pipeline.etl.load.analysis import method

        assert method is not None
        assert hasattr(method, 'load_method')
