__copyright__ = "Copyright 2020, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"


from qgis.core import QgsApplication
from qgis.PyQt.QtCore import QCoreApplication, Qt, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from pg_metadata.dock import PgMetadataDock
from pg_metadata.locator import LocatorFilter
from pg_metadata.processing.provider import PgMetadataProvider
from pg_metadata.qgis_plugin_tools.tools.custom_logging import setup_logger
from pg_metadata.qgis_plugin_tools.tools.i18n import setup_translation
from pg_metadata.qgis_plugin_tools.tools.resources import (
    plugin_path,
    resources_path,
)


class PgMetadata:
    def __init__(self, iface):
        self.iface = iface
        self.dock = None
        self.provider = None
        self.locator_filter = None
        self.main_action = None

        setup_logger('pg_metadata')

        locale, file_path = setup_translation(
            folder=plugin_path("i18n"), file_pattern="pgmetadata_{}.qm")
        if file_path:
            self.translator = QTranslator()
            self.translator.load(file_path)
            # noinspection PyCallByClass,PyArgumentList
            QCoreApplication.installTranslator(self.translator)

    def initProcessing(self):
        if not self.provider:
            self.provider = PgMetadataProvider()
            QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

        if not self.dock:
            self.dock = PgMetadataDock()
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock)

        if not self.locator_filter:
            self.locator_filter = LocatorFilter(self.iface)
            self.iface.registerLocatorFilter(self.locator_filter)

        icon = QIcon(resources_path('icons', 'icon.png'))
        self.main_action = QAction(icon, 'PgMetadata', self.iface.mainWindow())
        self.iface.pluginMenu().addAction(self.main_action)
        self.main_action.triggered.connect(self.open_dock)

    def open_dock(self):
        """ Open the dock. """
        self.dock.show()
        self.dock.raise_()

    def unload(self):
        if self.dock:
            self.iface.removeDockWidget(self.dock)
            self.dock.deleteLater()

        if self.provider:
            QgsApplication.processingRegistry().removeProvider(self.provider)

        if self.locator_filter:
            self.iface.deregisterLocatorFilter(self.locator_filter)

        if self.main_action:
            self.iface.pluginMenu().removeAction(self.main_action)

    @staticmethod
    def run_tests(pattern='test_*.py', package=None):
        """Run the test inside QGIS."""
        try:
            from pathlib import Path

            from pg_metadata.qgis_plugin_tools.infrastructure.test_runner import (
                test_package,
            )
            if package is None:
                package = '{}.__init__'.format(Path(__file__).parent.name)
            test_package(package, pattern)
        except (AttributeError, ModuleNotFoundError):
            message = 'Could not load tests. Are you using a production package?'
            print(message) # NOQA
