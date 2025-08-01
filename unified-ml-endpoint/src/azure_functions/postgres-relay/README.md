### Azure Relay

This is a simple Azure Function that can be used to relay messages from an Azure Service Bus to a Postgres database.

## Configuration
Use the makefile to create a local environment file to test the function locally.  You will need to provide the following values:

To set up the environment locally:

First create a new conda environment or virtualenv (as you prefer) to maintain an environment.

```shell
conda create -n azure-relay python=3.11
conda activate azure-relay
```

Then install the requirements:

```shell
pip install -r requirements.txt
```


### Running and Deploying
**export ENV_TYPE from terminal. Ensure it is set to one of dev/production/staging otherwise it will default to dev**

To run the function locally:

````
make run
````


For now we are running the function inside the Function App `test-ml2-tbd`. The below code allows you to deploy to that Azure function app. You will need to have the Azure CLI installed and be logged in to the correct subscription.

````
make deploy FUNCTION_APP_NAME="test-ml2-tbd"
````

**During initial set up of the function app ensure AZURE_CLIENT_SECRET and ENV_TYPE are set as environment variables inside the configuration tab of the Azure function app.**