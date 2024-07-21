This project serves an app that lets users explore the Earth's surface for climate change trends. This relies on climate data available from the Open-Source API here: https://open-meteo.com/. 

# Deployment 
The app is deployed whenever a change is commited to the main branch. This triggers a github action which launches an ECS Fargate task. Route 53 connects the record of this new deployment to my personal site here, climate.haydenquilty.com. 