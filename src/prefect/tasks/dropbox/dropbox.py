import dropbox

from prefect.client import Secret
from prefect.core import Task
from prefect.utilities.tasks import defaults_from_attrs


class DropboxDownload(Task):
    """
    Task for downloading a file from Dropbox. Note that _all_ initialization settings can be
    provided / overwritten at runtime.

    Args:
        - path (str): the path to the file to download
        - access_token_secret (str, optional): the name of the Prefect Secret containing a
            Dropbox access token; defaults to `"DROPBOX_ACCESS_TOKEN"`
        - **kwargs (optional): additional kwargs to pass to the `Task` constructor
    """

    def __init__(self, path: str, access_token_secret: str = None, **kwargs):
        self.path = path
        self.access_token_secret = access_token_secret or "DROPBOX_ACCESS_TOKEN"
        super().__init__(**kwargs)

    @defaults_from_attrs("path", "access_token_secret")
    def run(self, path: str = None, access_token_secret: str = None) -> str:
        """
        Run method for this Task.  Invoked by _calling_ this Task within a Flow context, after initialization.

        Args:
            - path (str): the path to the file to download
            - access_token_secret (str, optional): the name of the Prefect Secret containing a
                Dropbox access token; defaults to `"DROPBOX_ACCESS_TOKEN"`

        Raises:
            - ValueError: if the `path` is `None`

        Returns:
            - str: the file contents
        """
        ## check for any argument inconsistencies
        if path is None:
            raise ValueError("No path provided.")

        ## create client
        access_token = Secret(access_token_secret).get()
        dbx = dropbox.Dropbox(access_token)
        response = dbx.files_download(path)[1]
        return response.content