
# Chris' assignment
This has been the first project I have done in Flask. I wanted to use the opportunity to learn another framework (and tools) as I did this assignment. I started with AWS and implemented it according to the instructoins as provided.

## Instructions on how to run
- Make sure you have docker and compose installed on your system.
- Clone this repo to your local system
- Make sure no other application is using port 3000 on your system
- Switch your working directory to the root of the application i.e `/path/to/digiusher`
- Run the following commands to build, and start the development server.
```
docker compose build
docker compose up
```
- API can be accessed at `http://localhost:3000/api/get-prices`. Without any parameters, you will get default list of items.
- To add query parametes, the URL will look like this `http://localhost:3000/api/get-prices?cloud_type=aws&location=Europe&number_of_cpus=4&memory=8`
- The data is downloaded using a cron job managed by a python package called [apscheduler](https://apscheduler.readthedocs.io/en/3.x/). However, to test the download, you can run the following commands;

`docker compose exec web /bin/bash`

That will take you to the Linux shell of the application container. From there, run the following command

`flask integrations update aws`

You should now have data in your database to use for testing the API.
- To use pagination, add `page` and `per_page` parameters to the query (GET) parameters. Default `per_page` value is 20

## What can be improved
- Adding Type hints through the codebase
- Adding Linting possibly via git hooks
- Adding tests
- Use of logging through out the application
- Use env variables for some of the settings / configs that could be sensitive
- Error checking and handling to be added

### Why download csv instead of json from AWS?
The json files are slightly bigger than the csv equivalents, but also the csv files are easier on the memory because they can be read one line at a time, whereas a JSON file will need to for example load a full list which can contain up to tens of thousands of items. I was able to figure out how to stream both, but csv would be more efficient.
