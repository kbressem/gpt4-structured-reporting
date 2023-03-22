import argparse
import json
import os
import time

import openai
import pandas as pd
from tqdm.autonotebook import tqdm

parser = argparse.ArgumentParser(description="Xray Classification with GPT-4")
parser.add_argument(
    "--xray_reports", type=str, default="/Users/keno/Projects/medbert/csv/xray/test.csv"
)
parser.add_argument("--api_key_path", type=str, default="/Users/keno/openai-apikey")
parser.add_argument("--output_dir", type=str, default="../xrays")
args = parser.parse_args()

assert os.path.exists(args.output_dir)

system = """
You are a helpful chatbot, that can accuratly classify radiology reports for the presence or absence of fingins. 
Each report, you will classify for the presence or absence of the following findings: 
Cardiac congestion, lung opacities (that includes pneumonia, atelectasis, dystelectasis and other airway processes), 
pleural effusion (this does NOT inlcude pericardial effusion), pneumothorax, presence of thoracic drains, 
presence of venous catheters, presence of gastric tubes, presence of tracheal tubes, misplacement of any devices. 
structure your answer like the template I provide you and return this template
{
    "congestion": "[0/1]",
    "opacitiy": "[0/1]",
    "effusion": "[0/1]",
    "pneumothorax": "[0/1]",
    "thoracic_drain": "[0/1]",
    "venous_catheter": "[0/1]",
    "gastric_tube": "[0/1]",
    "tracheal_tube": "[0/1]",
    "misplaced": "[0/1]",
}

"""
xray_reports = pd.read_csv(args.xray_reports)
openai.api_key_path = args.api_key_path


def classify_xray(report):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": report},
        ],
    )

    result = response["choices"][0]["message"]["content"]
    json_text = result.split("{", 1)[1].split("}", 1)[0]
    return json.loads("{" + json_text + "}")


if __name__ == "__main__":
    for i, row in tqdm(xray_reports.iterrows(), total=len(xray_reports)):
        if os.path.exists(f"{args.output_dir}/{row.id}.json"):
            continue
        for i in range(0, 3):
            try:
                report = classify_xray(row.text)
            except Exception as e:
                print(e)
                time.sleep(2)
        with open(f"{args.output_dir}/{row.id}.json", "w+") as f:
            f.write(json.dumps(report))
