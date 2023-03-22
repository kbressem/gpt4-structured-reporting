import json
import os
import re
import time
from difflib import SequenceMatcher

import openai


def similar(a, b):
    return SequenceMatcher(None, a.upper(), b.upper()).ratio()


def find_closest_key(dct_keys, key, threshold=0.75):
    closest_key = None
    highest_similarity = 0

    for k in dct_keys:
        if key in str(k):
            return k

    for k in dct_keys:
        similarity = similar(key, k)
        if similarity > highest_similarity:
            highest_similarity = similarity
            closest_key = k

    if highest_similarity >= threshold:
        return closest_key
    else:
        return "OWN"


class GPTStructuredReporting:
    def __init__(self, api_key: str, path_to_templates: str, model: str = "gpt-4", **kwargs):
        self.set_api_key(api_key)
        self.model = model
        with open(path_to_templates, "r") as file:
            json_string = file.read()
        self.templates = json.loads(json_string)
        self.openai_kwargs = kwargs

    def __call__(self, report_text: str) -> str:
        for i in range(10):
            try:
                return self.send_request(report_text)
            except Exception as e:
                print(f"Error: {e}")
                if i < 9:  # don't wait after the last retry
                    print("Retrying after 10 seconds...")
                    time.sleep(10)  # wait for 5 seconds before retrying
                else:
                    print("Maximum retries reached.")
                    return ""

    def send_request(self, report_text) -> str:
        openai.api_key = self._api_key

        print("Sending initial request: \n\n")
        response1 = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system1()},
                {"role": "user", "content": report_text},
            ],
            **self.openai_kwargs,
        )
        main_finding, template = self.get_template_and_finding(response1)
        template = find_closest_key(self.templates.keys(), template)

        print("MAIN FINDING: ", main_finding)
        print("TEMPLATE: ", template)
        response2 = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system2(template)},
                {"role": "user", "content": report_text},
            ],
            **self.openai_kwargs,
        )

        content = response2["choices"][0]["message"]["content"]

        try:
            return json.loads(content)
        except:
            return content

    def set_api_key(self, api_key: str):
        if os.path.exists(api_key):
            with open(api_key, "r") as f:
                self._api_key = f.read().strip()
        else:
            self._api_key = api_key

    def system1(self):
        return (
            (
                "You are a chatbot that helps in converting free text radiology reports "
                "to a structured format. At first, you will analyze the text to identify "
                "the modality (CT, X-Ray, MRI, Ultrasound) as well as the main finding, "
                "then you will request the most appropriate structuring template from the user. "
                "Here are the available templates:\n"
            )
            + "".join([k + "\n" for k in self.templates.keys()])
            + (
                "Structure your answer as follows:\n"
                "MAIN FINDING: <add main finding here>\n"
                "TEMPLATE: <add requested template here>\n"
                "Structure your answer only like this. It is of utmost importance, that you list only one main finding "
                "and request only ONE template. Make sure you request the template exaclty how it is called here.\n"
                "If there is not template that could be used for this text, return 'OWN' for TEMPLATE."
                "If the text is no radiology report return '...'."
            )
        )

    def system2(self, template: dict):
        if template in self.templates.keys():
            return (
                "This is a JSON template for a structured report in radiology. "
                "The report provides a category and a default entry. "
                "You will structure radiology reports the user provides you according to this template. "
                "It is of utmost importance, that you keep all information of the report in the "
                "structured version, but use structured, standardized language. "
                "Return ONLY the report converted to JSON and return ONLY ONE filled out template"
                "If the text is not a radiology report, return '{}'."
                "Here is the template:\n"
            ) + json.dumps(self.templates[template])
        else:
            return (
                "Create a structured radiology report in JSON format. Return ONLY the report converted to JSON.\n"
                "Use this general template as guidance:\n"
                "Study Date: [Study Date]\n"
                "Study Time: [Study Time]\n"
                "\n"
                "[Study Information]\n"
                "Modality: [Modality (e.g., X-ray, MRI, CT, Ultrasound, etc.)]\n"
                "Study Type: [Study Type (e.g., Chest, Abdomen, Pelvis, Head, etc.)]\n"
                "Technique: [Detailed Technique Description]\n"
                "\n"
                "[Clinical History]\n"
                "Indication: [Brief Description of the Patient's Symptoms, History or Reason for Referral]\n"
                "\n"
                "[Findings]\n"
                "Summary: [Brief Summary of Key Findings]\n"
                "\n"
                "Detailed Findings:\n"
                "\n"
                "    [Anatomical Structure/Area]: [Description of Findings Related to the Anatomical Structure/Area]\n"
                "    [Anatomical Structure/Area]: [Description of Findings Related to the Anatomical Structure/Area]\n"
                "    [Anatomical Structure/Area]: [Description of Findings Related to the Anatomical Structure/Area]\n"
                "    [Anatomical Structure/Area]: [Description of Findings Related to the Anatomical Structure/Area]\n"
                "    (Add or remove additional lines as needed)\n"
                "\n"
                "[Impression/Conclusion]\n"
                "    [Conclusion/Diagnosis related to Finding #1]\n"
                "    [Conclusion/Diagnosis related to Finding #2]\n"
                "    [Conclusion/Diagnosis related to Finding #3]\n"
                "    [Conclusion/Diagnosis related to Finding #4]\n"
                "    (Add or remove additional lines as needed)\n"
                "\n"
                "[Recommendations]\n"
                "\n"
                "    [Recommendation or Follow-up Action Related to Conclusion/Diagnosis #1]\n"
                "    [Recommendation or Follow-up Action Related to Conclusion/Diagnosis #2]\n"
                "    [Recommendation or Follow-up Action Related to Conclusion/Diagnosis #3]\n"
                "    [Recommendation or Follow-up Action Related to Conclusion/Diagnosis #4]\n"
                "    (Add or remove additional lines as needed)\n"
                "\n"
                "[Additional Comments]\n"
                "[Any Other Relevant Information or Additional Comments]\n"
            )

    def get_template_and_finding(self, response: dict) -> tuple:
        content = response["choices"][0]["message"]["content"]

        main_finding_pattern = r"MAIN FINDING:(.*?)TEMPLATE:"
        main_finding_match = re.search(main_finding_pattern, content, re.DOTALL)

        # Extract everything after "TEMPLATE"
        template_pattern = r"TEMPLATE:(.*)"
        template_match = re.search(template_pattern, content)

        try:
            main_finding = main_finding_match.group(1).strip()
            template = template_match.group(1).strip()
        except:
            main_finding = "NA"
            template = "OWN"

        return main_finding, template
