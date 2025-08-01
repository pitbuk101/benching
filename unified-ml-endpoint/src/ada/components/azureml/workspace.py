"""Azure ML workspace related methods and configurations."""

from typing import Dict

from azureml.core import Workspace

# from ada.utils.authorization.credentials import get_authorized_service_principle
from ada.utils.logs.logger import get_logger

log = get_logger("create_azml_environment")


def get_workspace(conf: Dict) -> Workspace:
    """Reusable method for retrieving the Azure ML workspace."""

    svc_pr = get_authorized_service_principle(conf=conf)
    workspace = Workspace(
        workspace_name=conf["global"]["workspace_name"],
        subscription_id=conf["global"]["subscription_id"],
        resource_group=conf["global"]["resource_group"],
        auth=svc_pr,
    )

    return workspace
