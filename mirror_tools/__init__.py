from krita import DockWidgetFactory, DockWidgetFactoryBase, Krita
from .mirror_tools import MirrorToolsPanel  # your dock widget class file

DOCKER_ID = 'mirror_tools_docker'
instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockRight,
                                        MirrorToolsPanel)
instance.addDockWidgetFactory(dock_widget_factory)
