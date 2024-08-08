def ez_azml_fn(
    test_input: "Input(type='uri_file')",  # type: ignore  # noqa: F821
    test_output: "Output(type='uri_folder')",  # type: ignore  # noqa: F821
):
    """Test input function."""
    out_path = f"{test_output}/out_file.txt"
    with open(str(test_input)) as f_in, open(out_path, "w") as f_out:
        content = f_in.read()
        print(content)
        f_out.write(content)


def ez_azml_pipeline(test_input):
    """Test pipeline function."""
    test_result = ez_azml_fn(test_input=test_input)
    return {"test_output": test_result.outputs.test_output}
