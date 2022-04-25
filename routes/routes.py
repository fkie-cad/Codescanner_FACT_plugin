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
        image = binary.plot_to_buffer(dpi=100, plot_type=binary.BYTE_PLOT)
        encoded_img = b64encode(image).decode()
        template_str = f'<img style="max-width:100%;" src="data:image/png;base64,{encoded_img}" width="1024px" />'
        return render_template_string(template_str)

    @roles_accepted(*PRIVILEGES['view_analysis'])
    def _get_color_map(self, uid):
        binary = CodescannerAnalysisData(self.fso.generate_path_from_uid(uid))
        image = binary.plot_to_buffer(dpi=100, plot_type=binary.COLOR_MAP)
        encoded_img = b64encode(image).decode()
        template_str = f'<img style="max-width:100%;" src="data:image/png;base64,{encoded_img}" width="1024px" />'
        return render_template_string(template_str)
