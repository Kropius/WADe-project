# RAT WADe Project

This repo represents the implementation for [RAT WADe Project](https://profs.info.uaic.ro/~busaco/teach/courses/wade/projects/index.html) of Fall 2021 made by **Cioata Matei-Alexandru, Lipan Radu-Matei, Rezmerita Mihnea-Ioan**. More information on what are the requirements can be found in the link attached.

## [Midterm Deliverables—Design & Architecture](https://github.com/Kropius/WADe-project/tree/main/documentation)
## Tags
#project #infoiasi #wade #web

### Team Notes:
- Run a function locally: go to its folder (Below, `PostApiSpecifiaction`) and run:
```
functions-framework --target post_api --debug
```
- Deploy a function: go to its folder (Below, `PostApiSpecifiaction`) and run:
```
gcloud functions deploy postApi --trigger-http --runtime python39 --region europe-west1
```
