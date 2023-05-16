import json
import csv

# Open the JSON file for reading
f = open('json.json')

data = json.load(f)

# Flatten the JSON data
def flatten_json(json_obj, delimiter='_', prefix=''):
    flattened = {}
    for k, v in json_obj.items():
        if isinstance(v, dict):
            flattened.update(flatten_json(v, delimiter, f"{prefix}{k}{delimiter}"))
        elif isinstance(v, list):
            for index, item in enumerate(v):
                if isinstance(item, dict):
                    flattened.update(flatten_json(item, delimiter, f"{prefix}{k}{delimiter}{index}{delimiter}"))
                else:
                    flattened[f"{prefix}{k}{delimiter}{index}"] = item
        else:
            flattened[f"{prefix}{k}"] = v
    return flattened

# Extract only the 'report' key from the JSON data. Can be changed to fit use case. In this case, the main object I needed is in reportResponses
reports_data = [response['report'] for item in data for response in item['body']['reportResponses']]

# Flatten the 'report' data
flattened_reports = [flatten_json(report) for report in reports_data]

# Identify the unique CSV columns
csv_columns = set().union(*(d.keys() for d in flattened_reports))

# Write the flattened 'report' data to a CSV file named 'report_output.csv'
with open('report_output.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for row in flattened_reports:
        writer.writerow(row)