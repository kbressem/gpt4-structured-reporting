import json
import os
from html import escape

from json2html import Json2Html


def json_to_html_table(json_data):
    headers = list(json_data[0].keys())
    json2html = Json2Html()
    rows = []
    for record in json_data:
        first_column = True
        for key in headers:
            if first_column:
                td_style = "white-space: word-wrap;"
                td_bg_color = "#ededed"
                first_column = False
                row = '<td bgcolor="#ababab">Free Text</td>'
            else:
                td_style = "white-space: pre-wrap; word-wrap: break-word;"
                td_bg_color = "#ffffff"
                row = '<td bgcolor="#ababab">Structured</td>'

            value = json2html.convert(record[key])
            row += f'<td style="{td_style}", bgcolor="{td_bg_color}">{value}</td>'

            rows.append(f"<tr>{row}</tr>")

    html_table = f"<table>\n<tbody>\n" + "\n".join(rows) + "\n</tbody>\n</table>"
    return html_table


html_start = """
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sample Reports</title>
  <style>
    table {
      border-collapse: collapse;
      width: 100%;
    }

    th,
    td {
      border: 1px solid black;
      padding: 8px;
      text-align: left;
    }

    th {
      background-color: #f2f2f2;
    }

    tr:nth-child(even) {
      background-color: #f2f2f2;
    }

  </style>

</head>

<body>
  <div id="table-container"></div>

"""

html_end = "</body>"

if __name__ == "__main__":
    with open(f"../reports/structured_reports.json", "r") as file:
        reports = json.load(file)

    with open("../templates/reports.html", "w+") as f:
        f.write(html_start)

    for category in reports.keys():
        json_data = reports[category]
        json_items = [item for item in json_data.values()]
        html_table = json_to_html_table(json_items)
        with open("../templates/reports.html", "a") as f:
            f.write(f'<h1>{category.replace("_", " ")}</h1>')
            f.write(html_table)
            f.write("\n")
    with open("../templates/reports.html", "a") as f:
        f.write(html_end)
    print("Successfully converted JSON to HTML")
