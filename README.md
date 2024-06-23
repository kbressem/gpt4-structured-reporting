# Radiology Report Structuring with GPT-4

This repository demonstrates how radiology reports can be structured using OpenAI's GPT-4. It includes example notebooks, a demo Flask app, and sample reports. The main goal is to demonstrate how large language models can be stratecially propmpted to perform complex tasks in information extraction and structuring of complex text data.


## Repository Structure:


```bash
.
├── README.md
├── app.py                   # Flask app. Start with python app.py
├── gpt.py                   # Wrapper for GPT-4 API
├── static                   # Static files for demo app
│   ├── css
│   │   └── styles.css
│   ├── img
│   │   ├── examle.png
│   │   └── spinner.gif
│   ├── js
│   │   └── main.js
│   └── report_templates.json  # JSON templates for structured reports
├── templates
│   ├── index.html
│   └── reports.html           # Structured reports as HTML files
├── examples
│   └── structure_mimic.ipynb  # An example usecase on how GPT could structure the MIMIC dataset
├── reports                     
│   ├── structured_reports.json  # structured and structures reports
│   └── xray_reports.json      # Structured chest x-ray reports
└── scripts
    ├── json-to-html-table.py
    ├── report-structuring.py  # Convert reports to structured format with GPT-4
    └── xray-clf.py

```

## Getting Started:

To run the demo app locally, follow these steps:

Clone the repository:

```bash

git clone https://github.com/yourusername/radiology-report-structuring.git
cd radiology-report-structuring

```

install the the `openai` python package, to be able to assess the OpenAI api. 
You will need an API-Key to be able to use the OpenAI api. 


# Demo
You can access the app [here](http://kbressem.pythonanywhere.com/)

![image](https://user-images.githubusercontent.com/37253540/226769001-ddb5968d-f3ea-4e40-9d30-721e7a1a0369.png)


## Run the Flask app locally:

Given you have installed all dependecies, you can run the demo application with
```bash

export FLASK_APP=app.py
export FLASK_ENV=development
flask run

```
Alternatively the demo can also be run with Docker: 

```bash
docker build -t gpt-structured-reporting .
docker run -p 5000:5000 gpt-structured-reporting
```

Open your browser and visit http://127.0.0.1:5000 to access the demo app.

Navigate to the demo app and upload a unstructured report (use sample_reports.json for a quick start). GPT-4 will chose the most appropriate template and return a structured report as JSON. This may take a while and you need to provide your API key for this. For inspiration you can view the structured reports in the table format on the reports.html page.




