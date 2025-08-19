from metrics_parser_0 import get_pred_segments
from metrics_0 import generate_final_report

def pretty_print_report(report):
    """
    Print the report in a readable format.
    
    :param report: The report dictionary to print.
    """
    print("Final Report:")
    for key, value in report.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")

# model inputs should be complete continuous blocks in an XML file in the dataset, here is an example
model_input1 = "<data> \
    <system_output timestamp=\"13.014325\" group=\"0\">boxtop:/home/demo# </system_output>\n \
    <user_input timestamp=\"14.015738\" group=\"1\">s</user_input>\n \
    <system_output timestamp=\"14.0159\" group=\"1\">s</system_output>\n \
    <user_input timestamp=\"14.020021\" group=\"1\">s</user_input>\n \
    <system_output timestamp=\"14.020183\" group=\"1\"s</system_output>\n \
    <user_input timestamp=\"14.027932\" group=\"1\">h</user_input>\n \
    <system_output timestamp=\"14.321538\" group=\"1\">h</system_output>\n \
    <user_input timestamp=\"14.4\" sortme=\"True\"> </user_input>\n \
    </data>"

model_input2 = "<data> \
    <system_output timestamp=\"13.014325\" group=\"0\">boxtop:/home/demo# </system_output>\n \
    <user_input timestamp=\"14.015738\" group=\"1\">s</user_input>\n \
    <system_output timestamp=\"14.0159\" group=\"1\">s</system_output>\n \
    <user_input timestamp=\"14.020021\" group=\"1\">s</user_input>\n \
    <system_output timestamp=\"14.020183\" group=\"1\"s</system_output>\n \
    <user_input timestamp=\"14.027932\" group=\"1\">h</user_input>\n \
    <system_output timestamp=\"14.321538\" group=\"1\">h</system_output>\n \
    <user_input timestamp=\"14.4\" group=\"1\"> </user_input>\n \
    <system_output timestamp=\"14.5\" sortme=\"True\"> </system_output>\n \
    </data>"

model_inputs = [model_input1, model_input2]
model_outputs = ["Answer: 1", "Answer: 1"]
score_weights = {}  # Optional

pred_segments = get_pred_segments(model_inputs, model_outputs)  # put score weights here if needed
print(f"Predicted Segments: {pred_segments}")
gt_file = "ground_truth.txt"  # just an example path, replace with actual ground truth file path
final_report = generate_final_report(pred_segments, gt_file)
pretty_print_report(final_report)  # composite score is between 0.0 and 1.0, the higher the better