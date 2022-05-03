# pylint: disable=wrong-import-order
from pathlib import Path

from objects.file import FileObject
from test.unit.analysis.analysis_plugin_test_class import AnalysisPluginTest

from ..code.codescanner import AnalysisPlugin

TEST_DATA_DIR = Path(__file__).parent / 'data'


class TestAnalysisPluginCryptoHints(AnalysisPluginTest):

    PLUGIN_NAME = 'codescanner'
    PLUGIN_CLASS = AnalysisPlugin

    def test_process_object(self):
        for test_file, expected_result in [
            ('amd64.elf', 'Intel-64'),
            ('arm.elf', 'Arm-32-le'),
            ('hidden_arm.bin', 'Arm-32-le'),
        ]:
            test_fo = FileObject(file_path=str(TEST_DATA_DIR / test_file))
            processed_file = self.analysis_plugin.process_object(test_fo)
            assert self.PLUGIN_NAME in processed_file.processed_analysis
            assert processed_file.processed_analysis[self.PLUGIN_NAME]['architecture']['Full'] == expected_result
