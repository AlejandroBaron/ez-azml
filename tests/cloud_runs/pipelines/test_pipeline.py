from azure.ai.ml.entities import PipelineJob
from ez_azml.cloud_runs import PipelineRun


def test_e2e_register(pipeline: PipelineRun):
    """Tests e2e mock register."""
    component = pipeline.register()
    assert isinstance(component, PipelineJob)
