def ez_azml_pipeline(test_input):
    """Example pipeline function."""
    # pytorch_script is the name of the registered component
    test_result = pytorch_script(data_path=test_input)  # noqa F821
    return {"test_output": test_result.outputs.output_path}
