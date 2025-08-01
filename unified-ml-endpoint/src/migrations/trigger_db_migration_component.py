import os
import time

import yaml  # type: ignore # noqa
from azure.ai.ml.entities import PipelineJob, PipelineJobSettings

from ada.utils.azml.azml_utils import get_azml_client
from ada.utils.config.config_loader import (
    get_tenant_list_for_the_workspace,
    read_config,
)
from ada.utils.logs.logger import get_logger

conf = read_config("azml_deployment.yaml")
log = get_logger("azml-components")


def trigger_db_migrate_component(azml_client):
    """
    Setting up a pipeline job to trigger the db migration component in the azure ml workspace.
    """
    component_name = "db_migrate_pre_deploy"
    db_migrate_component = azml_client.components.get(component_name)

    print('Azure client secret', os.environ['AZURE_CLIENT_SECRET'])
    pipeline_job = PipelineJob(
        description="Pre deploy db migrate trigger pipeline",
        display_name="db_trigger_pipeline",
        experiment_name="pre-deploy-db-migration-pipelines",
        settings=PipelineJobSettings(
            default_compute=conf["static_deployment_conf"]["db_migrate_compute_target"],
        ),
        jobs={
            "db_migrate": db_migrate_component(
                tenant_list=",".join(get_tenant_list_for_the_workspace()),
                azure_client_secret=os.environ["AZURE_CLIENT_SECRET"],
                #TODO: Move this particular secret to AWS. Harcoded for now, need to pick from AWS secret later on.
                azure_client_secret_secondary=os.environ["AZURE_CLIENT_SECRET_SECONDARY"],
            ),
        },
    )

    run = azml_client.jobs.create_or_update(pipeline_job)
    log.info(f"Pipeline job {run.name} submitted successfully.")

    # Wait unitl the job completes
    log.info(f"Waiting for job {run.name} to complete...")
    while True:
        job_status = azml_client.jobs.get(run.name).status
        log.info(f"Current job status: {job_status}")

        if job_status in ["Completed"]:
            break

        if job_status in ["Failed", "Canceled"]:
            raise Exception(f"DB Migration job is {job_status}")

        time.sleep(30)  # Wait before checking the status again

    # Final job status
    final_job = azml_client.jobs.get(run.name)
    log.info(f"Job {final_job.name} completed with status: {final_job.status}")


if __name__ == "__main__":
    azml_client = get_azml_client()
    # Step 2: Load the Registered Component
    trigger_db_migrate_component(azml_client)
