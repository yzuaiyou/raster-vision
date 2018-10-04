import os
from tempfile import TemporaryDirectory
import logging

from rastervision.runner import ExperimentRunner
from rastervision.utils.files import save_json_config

log = logging.getLogger(__name__)

class LocalExperimentRunner(ExperimentRunner):
    def __init__(self, tmp_dir=None):
        self.tmp_dir = tmp_dir

    def _run_experiment(self, command_dag):
        """Runs all commands on this machine."""

        def run_commands(tmp_dir):
            for command_config in command_dag.get_sorted_commands():
                command_root_uri = command_config.root_uri
                command_uri = os.path.join(command_root_uri,
                                           'command-config.json')
                log.info('Saving command configuration to {}...'.format(
                    command_uri))
                save_json_config(command_config.to_proto(), command_uri)

                command = command_config.create_command(tmp_dir)

                command.run(tmp_dir)

        if self.tmp_dir:
            run_commands(self.tmp_dir)
        else:
            with TemporaryDirectory() as tmp_dir:
                run_commands(tmp_dir)
