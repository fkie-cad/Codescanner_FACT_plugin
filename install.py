#!/usr/bin/env python3

import logging
from pathlib import Path

try:
    from helperFunctions.install import OperateInDirectory, is_virtualenv, run_cmd_with_logging
    from plugins.installer import AbstractPluginInstaller
except ImportError:
    import sys
    SRC_PATH = Path(__file__).absolute().parent.parent.parent.parent
    sys.path.append(str(SRC_PATH))

    from helperFunctions.install import OperateInDirectory, is_virtualenv, run_cmd_with_logging
    from plugins.installer import AbstractPluginInstaller


class CodescannerInstaller(AbstractPluginInstaller):
    base_path = Path(__file__).resolve().parent

    def build(self):
        build_dir = self.base_path / 'build'
        run_cmd_with_logging(
            f'git clone https://github.com/fkie-cad/Codescanner.git -o {build_dir}',
            shell=True, check=True
        )
        with OperateInDirectory(build_dir, remove=True):
            command = 'python3 setup.py install'
            if not is_virtualenv():
                command = f'sudo -EH {command}'
            run_cmd_with_logging(command, shell=True, check=True)


# Alias for generic use
Installer = CodescannerInstaller

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    distribution = check_distribution()
    installer = Installer(distribution)
    installer.install()
