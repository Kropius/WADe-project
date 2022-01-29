# RAT WADe Project

This repo represents the implementation for [RAT WADe Project](https://profs.info.uaic.ro/~busaco/teach/courses/wade/projects/index.html) of Fall 2021 made by **Cioata Matei-Alexandru, Lipan Radu-Matei, Rezmerita Mihnea-Ioan**. More information on what are the requirements can be found in the link attached.

## [Midterm Deliverables—Design & Architecture](https://github.com/Kropius/WADe-project/tree/main/documentation)
## Tags
#project #infoiasi #wade #web

### Team Notes:
- Run a function locally: go to its folder (Below, `be/rat/src`) and run:
```
functions-framework --target apis_endpoint --debug
functions-framework --target api_endpoint --debug
```
- Deploy a function: go to its folder (Below, `be/rat/src`) and run:
```
gcloud functions deploy apisEndpoint --trigger-http --runtime python39 --region europe-west1 --entry-point apis_endpoint
gcloud functions deploy apiEndpoint --trigger-http --runtime python39 --region europe-west1 --entry-point api_endpoint
```
- Update ApiGateway config (replace `<API_DEFINITION>` with the yaml OpenApi 2.0 specification on your device and `<version>` with a unique number)
```
gcloud api-gateway api-configs create wade-rat-mihtei-rezciopan-v<version> --api=wade-rat-mihtei-rezciopan --openapi-spec=<API_DEFINITION> --project=avid-airway-337117 --backend-auth-service-account=avid-airway-337117@appspot.gserviceaccount.com

gcloud api-gateway gateways update wade-rat-mihtei-rezciopan --api=wade-rat-mihtei-rezciopan --api-config=wade-rat-mihtei-rezciopan-v<version> --location=europe-west1 --project=avid-airway-337117
```