from krita import DockWidget, Krita
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtGui import QImage, QPainter
from PyQt5 import QtGui

class MirrorToolsPanel(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mirror Tools")
        main_widget = QWidget()
        layout = QHBoxLayout()

        btn = QPushButton("Mirror Right to Left")
        btn.setFixedSize(160, 60)
        btn.clicked.connect(self.mirror_right_to_left)
        layout.addWidget(btn)

        main_widget.setLayout(layout)
        self.setWidget(main_widget)

    def mirror_right_to_left(self):
        print("Mirror started")
        doc = Krita.instance().activeDocument()
        if not doc:
            print("No active document")
            return

        nodes = [doc.activeNode()]
        if not nodes:
            print("No selection, using root node")
            nodes = [doc.rootNode()]

        for node in nodes:
            print(f"Checking node: {node.name()}, type: {node.type()}")
            if node.type()!= "paintlayer":
                print(f"Node type: '{node.type()}'")
                print("Not a paint layer, skipping")
                continue

            w, h = doc.width(), doc.height()
            print(f"Document size: {w}x{h}")


            data = node.pixelData(0, 0, w, h)
            image = QImage(data, w, h, QImage.Format_RGBA8888)
            painter = QPainter(image)

            # Clear left side
            painter.setCompositionMode(QPainter.CompositionMode_Source)
            painter.fillRect(0, 0, w // 2, h, QtGui.QColor(0, 0, 0, 0))  # transparent

            # Copy right side
            right_half = image.copy(w // 2, 0, w // 2, h)
            mirrored = right_half.mirrored(True, False)

            # paste mirror on left
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            painter.drawImage(0, 0, mirrored)
            painter.end()

            print("Setting modified pixels")
            # add new layer with symmetrized image
            new_layer = doc.createNode(node.name() + "_mirrored", "paintlayer")
            doc.rootNode().addChildNode(new_layer, node)

            new_layer.setPixelData(image.bits().asstring(image.byteCount()), 0, 0, w, h)

            # empty the original and merge down the new
            doc.setActiveNode(node)
            Krita.instance().action('clear').trigger()
            new_layer.mergeDown()




        doc.waitForDone()
        doc.refreshProjection()

        print("Mirror completed")


    def canvasChanged(self, canvas):
        pass
