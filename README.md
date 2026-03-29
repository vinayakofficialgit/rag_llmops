
setup:
1. create DB + logs table
2. update .env
3. pip install -r requirements.txt
4. uvicorn main:app --reload



<!-- ##to check connection for langfuse -->
<!-- ##curl --ssl-no-revoke -u "pk-lf-5e829818-5f2d-4079-90bb-245b8cd  24315:sk-lf-c2700576-cca1-40ef-8c59-176b70724e75"               https://us.cloud.langfuse.com/api/public/projects
{"data":[{"id":"cmn7is9s8000jad07b9hpv7yh","name":"my-llmops-monitoring-projects","organization":{"id":"cmn7iq9di065pad076pjmcgjl","name":"LLMOPS-ORG-vin"},"metadata":{}}]}(.venv)  -->