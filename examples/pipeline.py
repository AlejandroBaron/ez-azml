# def ez_azml_command_fn(
#     test_input: "Input(type='uri_file')",  # type: ignore
#     test_output: "Output(type='uri_folder')",  # type: ignore
# ):
#     """Example command function."""
#     print("This is an example!")
#     out_path = f"{test_output}/out_file.txt"
#     with open(str(test_input)) as f_in, open(out_path, "w") as f_out:
#         content = f_in.read()
#         print(content)
#         f_out.write(content)


def ez_azml_pipeline(test_input):
    """Example pipeline function."""
    test_result = pytorch(data_path=test_input)  # noqa F821
    return {"test_output": test_result.outputs.output_path}
