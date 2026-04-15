"""Targeted tests for Stage 2 qualitative Prompt C load layer."""


class TestQualitativeLoad:
    """Basic smoke tests for qualitative load module behavior."""

    def test_load_module_exists(self):
        from ca_biositing.pipeline.etl.load.analysis import qualitative

        assert qualitative is not None
        assert hasattr(qualitative, "load_qualitative_payloads")

    def test_load_handles_empty_payload(self):
        from ca_biositing.pipeline.etl.load.analysis import qualitative

        result = qualitative.load_qualitative_payloads.fn({})

        assert isinstance(result, dict)
        assert result["data_source"] == 0
        assert result["parameter"] == 0
        assert result["use_case"] == 0
        assert result["resource_end_use_record"] == 0
        assert result["observation"] == 0

    def test_normalize_name_handles_curly_apostrophe(self):
        from ca_biositing.pipeline.etl.load.analysis.qualitative import _normalize_name

        assert _normalize_name("Beau’s Market Report") == "beau's market report"
        assert _normalize_name("  BEAU'S MARKET REPORT  ") == "beau's market report"
