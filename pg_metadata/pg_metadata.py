__copyright__ = "Copyright 2020, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"


from qgis.core import QgsApplication

from pg_metadata.locator import LocatorFilter
from pg_metadata.processing.provider import PgMetadataProvider


class PgMetadata:
    def __init__(self, iface):
        self.iface = iface
        self.provider = None
        self.locator_filter = None

    def initProcessing(self):
        if not self.provider:
            self.provider = PgMetadataProvider()
            QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

        if not self.locator_filter:
            self.locator_filter = LocatorFilter(self.iface)
            self.iface.registerLocatorFilter(self.locator_filter)

    def unload(self):
        if self.provider:
            QgsApplication.processingRegistry().removeProvider(self.provider)
        if self.locator_filter:
            self.iface.deregisterLocatorFilter(self.locator_filter)

    @staticmethod
    def run_tests(pattern='test_*.py', package=None):
        """Run the test inside QGIS."""
        try:
            from pg_metadata.qgis_plugin_tools.infrastructure.test_runner import test_package
            from pathlib import Path
            if package is None:
                package = '{}.__init__'.format(Path(__file__).parent.name)
            test_package(package, pattern)
        except (AttributeError, ModuleNotFoundError):
            message = 'Could not load tests. Are you using a production package?'
            print(message)
