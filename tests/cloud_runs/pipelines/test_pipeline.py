from ez_azml.cloud_runs.pipelines import Pipeline


def test_pipeline_register_components(pipeline: Pipeline):
    """Tests that the components are properly decorated."""
    pipeline.commands = pipeline._register_components(pipeline.commands)


def test_pipeline_setup_dec_kwargs(pipeline: Pipeline):
    """Tests that the pipeline decorator kwargs are properly postprocessed."""
    pipeline.dec_kwargs = pipeline._setup_dec_kwargs(pipeline.dec_kwargs)


def test_build_pipeline(pipeline: Pipeline):
    """Tests that the pipeline is properly decorated."""
    pipeline.pipeline = pipeline._build_pipeline(pipeline.pipeline, pipeline.dec_kwargs)
