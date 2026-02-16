from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class ExperimentAnalysis(SQLModel, table=True):
    __tablename__ = "experiment_analysis"

    id: Optional[int] = Field(default=None, primary_key=True)
    experiment_id: Optional[int] = Field(default=None, foreign_key="experiment.id")
    analysis_type_id: Optional[int] = Field(default=None, foreign_key="analysis_type.id")

    # Relationships
    experiment: Optional["Experiment"] = Relationship()
    analysis_type: Optional["AnalysisType"] = Relationship()


class ExperimentEquipment(SQLModel, table=True):
    __tablename__ = "experiment_equipment"

    id: Optional[int] = Field(default=None, primary_key=True)
    experiment_id: Optional[int] = Field(default=None, foreign_key="experiment.id")
    equipment_id: Optional[int] = Field(default=None, foreign_key="equipment.id")

    # Relationships
    experiment: Optional["Experiment"] = Relationship()
    equipment: Optional["Equipment"] = Relationship()


class ExperimentMethod(SQLModel, table=True):
    __tablename__ = "experiment_method"

    id: Optional[int] = Field(default=None, primary_key=True)
    experiment_id: Optional[int] = Field(default=None, foreign_key="experiment.id")
    method_id: Optional[int] = Field(default=None, foreign_key="method.id")

    # Relationships
    experiment: Optional["Experiment"] = Relationship()
    method: Optional["Method"] = Relationship()


class ExperimentPreparedSample(SQLModel, table=True):
    __tablename__ = "experiment_prepared_sample"

    id: Optional[int] = Field(default=None, primary_key=True)
    experiment_id: Optional[int] = Field(default=None, foreign_key="experiment.id")
    prepared_sample_id: Optional[int] = Field(default=None, foreign_key="prepared_sample.id")

    # Relationships
    experiment: Optional["Experiment"] = Relationship()
    prepared_sample: Optional["PreparedSample"] = Relationship()
