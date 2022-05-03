from base64 import b64encode

from codescanner_analysis import CodescannerAnalysisData
from flask import render_template_string

from storage.fsorganizer import FSOrganizer
from web_interface.components.component_base import ComponentBase
from web_interface.security.decorator import roles_accepted
from web_interface.security.privileges import PRIVILEGES


class PluginRoutes(ComponentBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fso = FSOrganizer(self._config)

    def _init_component(self):
        self._app.add_url_rule('/plugins/codescanner/byte_plot/<uid>', 'plugins/codescanner/byte_plot/<uid>', self._get_byte_plot)
        self._app.add_url_rule('/plugins/codescanner/color_map/<uid>', 'plugins/codescanner/color_map/<uid>', self._get_color_map)

    @roles_accepted(*PRIVILEGES['view_analysis'])
    def _get_byte_plot(self, uid):
        binary = CodescannerAnalysisData(self.fso.generate_path_from_uid(uid))
        return self._render_plot(binary, binary.BYTE_PLOT)

    @roles_accepted(*PRIVILEGES['view_analysis'])
    def _get_color_map(self, uid):
        binary = CodescannerAnalysisData(self.fso.generate_path_from_uid(uid))
        return self._render_plot(binary, binary.COLOR_MAP)

    @staticmethod
    def _render_plot(binary: CodescannerAnalysisData, plot_type: int) -> str:
        try:
            image = binary.plot_to_buffer(dpi=100, plot_type=plot_type)
            image_src = f'data:image/png;base64,{b64encode(image).decode()}'
            alt_text = 'color map' if plot_type == binary.COLOR_MAP else 'byte plot'
        except IOError as err:
            image_src = ''
            alt_text = f'Error: {str(err)}'
        template_str = f'<img style="max-width:100%;" src="{image_src}" width="1024px" alt="{alt_text}" />'
        return render_template_string(template_str)
