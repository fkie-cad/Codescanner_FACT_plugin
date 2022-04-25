from codescanner_analysis import CodescannerAnalysisData

from analysis.PluginBase import AnalysisBasePlugin
from objects.file import FileObject
from plugins.mime_blacklists import MIME_BLACKLIST_COMPRESSED, MIME_BLACKLIST_NON_EXECUTABLE


class AnalysisPlugin(AnalysisBasePlugin):

    NAME = 'codescanner'
    DESCRIPTION = 'scan unknown binaries for executable code'
    VERSION = '1.0.0'
    DEPENDENCIES = ['file_type']
    MIME_BLACKLIST = MIME_BLACKLIST_NON_EXECUTABLE + MIME_BLACKLIST_COMPRESSED
    FILE = __file__

    def process_object(self, file_object: FileObject) -> FileObject:
        binary = CodescannerAnalysisData(file_object.file_path)
        result = {}

        for key in ['Full', 'ISA', 'Bitness', 'Endianess']:
            result.setdefault('architecture', {}).update({key: binary.architecture.get(key)})

        result['file_size'] = binary.sizes.get('FileSize')

        for key in ['Code', 'Ascii', 'Data', 'HighEntropy']:
            result.setdefault('sections', {}).update({
                key: {
                    'size': binary.sizes.get(key),
                    'regions': binary.regions.get(key),
                }
            })

        if result['architecture']['Full'] is not None:
            result['summary'] = [result['architecture']['Full']]
        file_object.processed_analysis[self.NAME] = result
        return file_object