mkdir -p app/{agents,models,integrations,utils} \
&& touch {requirements.txt,.env} \
&& touch app/{main.py,api.py} \
&& touch app/agents/{manager_agent.py,severity_agent.py,rca_agent.py,fix_agent.py} \
&& touch app/models/schemas.py \
&& touch app/integrations/{servicenow.py,slack.py} \
&& touch app/utils/formatter.py
