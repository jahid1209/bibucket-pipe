import os
from bitbucket_pipes_toolkit import Pipe, get_logger
import yaml
from download_synopsys_binaries import download_bridge, print_directory_files
from install_synopsys_bridge import extract_bridge
from prepare_bridge_input import prepare_blackduck_input_json, print_json
from run_scan import invoke_synopsys_bridge
from upload_artifacts import upload_sarif, upload_diagnostics


logger = get_logger()

schema = {
  'PRODUCT': {'type': 'string', 'required': True},
  'BLACKDUCK_URL': {'type': 'string', 'required': False},
  'BLACKDUCK_TOKEN': {'type': 'string', 'required': False},
  'BLACKDUCK_DOWNLOAD_URL': {'type': 'string', 'required': False, 'default':'https://sig-repo.synopsys.com/artifactory/bds-integrations-release/com/synopsys/integration/synopsys-bridge/latest/synopsys-bridge-linux64.zip'},
  'BITBUCKET_USERNAME': {'type': 'string', 'required': False},
  'BITBUCKET_APP_PASSWORD': {'type': 'string', 'required': False},
}


class BitbucketPipe(Pipe):
    def __init__(self, pipe_metadata=None, schema=None, env=None, check_for_newer_version=False):
        super().__init__(
            pipe_metadata=pipe_metadata,
            schema=schema,
            env=env,
            check_for_newer_version=check_for_newer_version
        )
        self.product = self.get_variable('PRODUCT')
        self.blackduck_url = self.get_variable('BLACKDUCK_URL')
        self.blackduck_token = self.get_variable('BLACKDUCK_TOKEN')
        self.blackduck_download_url = self.get_variable('BLACKDUCK_DOWNLOAD_URL')
        self.user_name = self.get_variable('BITBUCKET_USERNAME')
        self.bitbucket_app_password = self.get_variable('BITBUCKET_APP_PASSWORD')
        self.owner_name = os.getenv('BITBUCKET_REPO_OWNER')
        self.repository_name = os.getenv('BITBUCKET_REPO_SLUG')
        
    
    def run(self):
        logger.info('Executing the pipe...')
        
        logger.info(f"Product: {self.product}")
        logger.info(f"username: { self.user_name}")
        logger.info(f"owner name: {self.owner_name}")
        logger.info(f"repo_name: {self.repository_name}")

        # download bridge binary
        # comment me while developing and local testing as it is time consuming
        # uncomment me before docker deployment 
        logger.info("Downloading bridge....")
        downloaded_bridge_path = download_bridge(self.blackduck_download_url)
        logger.info(f"Downloaded_bridge_path {downloaded_bridge_path}")
        
        # for local testing only
        # comment me before docker deployment
        # uncomment me while developing and local testing to speed up the
        # downloaded_bridge_path = '/home/jahid/bridge.zip'

        extracted_directory = extract_bridge(downloaded_bridge_path)
        logger.info(f"Bridge extracted to: {extracted_directory}")

        input_json_path = prepare_blackduck_input_json(self.blackduck_url, self.blackduck_token)
        logger.info(f"Input Json Path: {input_json_path}")

        # invoke binary
        result = invoke_synopsys_bridge(extracted_directory, input_json_path)
        logger.info(f"Bridge returned: {result}")

        upload_sarif(self)
        upload_diagnostics(self)

        # print status
        self.success(message="Success!")


if __name__ == '__main__':
    # pipe = BitbucketPipe(pipe_metadata='/pipe.yml', schema=schema)

    # remove '/' from  /pipe.yml to run locally
    # add /pipe.yml before docker deployment
    with open('/pipe.yml', 'r') as metadata_file:
        metadata = yaml.safe_load(metadata_file.read())
    
    pipe = BitbucketPipe(schema=schema, pipe_metadata=metadata, check_for_newer_version=True)
    pipe.run()
