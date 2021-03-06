
import datetime
import platform
WindowTitle = "Billboard-Example"
if __name__ == "__main__":
    print()
    print(datetime.datetime.now().strftime('%H:%M:%S'))
    print(WindowTitle)
    print("Loading Modules")#,end="")
    if platform.system() == 'Windows':
        try:
            import ctypes
            myAppId = u'{}{}'.format(WindowTitle , datetime.datetime.now().strftime('%H:%M:%S')) # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)
        except:
            pass

from billboardgeometry import BillboardGeometry
from billboardmaterial import BillboardMaterial
import sys
from PyQt5 import QtWidgets,QtCore,QtGui,Qt , Qt3DAnimation,Qt3DCore,Qt3DExtras,Qt3DInput,Qt3DLogic,Qt3DRender , QtQml

#include <QColor>
#include <QDebug>
#include <QObject>
#include <QPropertyAnimation>
#include <QThread>
#include <QtGui.QVector3D>

#include <Qt3DCore/QEntity>
#include <Qt3DCore/QTransform>
#include <Qt3DExtras/QCuboidMesh>
#include <Qt3DExtras/QForwardRenderer>
#include <Qt3DExtras/QOrbitCameraController>
#include <Qt3DExtras/QPhongAlphaMaterial>
#include <Qt3DExtras/QPlaneMesh>
#include <Qt3DExtras/QSphereMesh>

#include <Qt3DExtras/Qt3DWindow>
#include <Qt3DExtras/qorbitcameracontroller.h>

#include <Qt3DRender/QCamera>
#include <Qt3DRender/QGeometry>
#include <Qt3DRender/QGeometryRenderer>
#include <Qt3DRender/QMaterial>
#include <Qt3DExtras/QFirstPersonCameraController>

#include <QtGui/QScreen>

#include <QtWidgets/QApplication>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>
#include <QCommandLinkButton>
#include <QPushButton>

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Custom Shader for Billboard")
        self.setWindowIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon))
        self.Display = Qt3DExtras.Qt3DWindow()
        self.DisplayContainer = QtWidgets.QWidget.createWindowContainer(self.Display)

        ### Root entity
        self.rootEntity = Qt3DCore.QEntity()
        
        self.screenSize = self.Display.screen().size()
        self.DisplayContainer.setMinimumSize(QtCore.QSize(400, 300))
        self.DisplayContainer.setMaximumSize(self.screenSize)
        
        self.central_widget = QtWidgets.QWidget(self)
        self.controlWidget = QtWidgets.QWidget(self)
        self.hLayout = QtWidgets.QHBoxLayout(self.central_widget)
        self.vLayout = QtWidgets.QVBoxLayout()
        self.controlLayout = QtWidgets.QGridLayout(self.controlWidget)
        self.vLayout.setAlignment(QtCore.Qt.AlignTop)
        self.hLayout.addWidget(self.DisplayContainer, 1)
        self.hLayout.addLayout(self.vLayout)
        self.vLayout.addWidget(self.controlWidget)
        self.setCentralWidget(self.central_widget)

        ### Create control widget
        self.info = QtWidgets.QCommandLinkButton()
        self.info.setText("Qt3D Billboard")
        self.info.setIconSize(QtCore.QSize(0,0))

        ### Random size
        self.randomSizeButton = QtWidgets.QPushButton(self.controlWidget)
        self.randomSizeButton.setText("Random Size")
        self.randomSizeButton.setToolTip("Random Size")

        ### Bigger billboard size
        self.biggerSizeButton = QtWidgets.QPushButton(self.controlWidget)
        self.biggerSizeButton.setText("Make Bigger")
        self.biggerSizeButton.setToolTip("Make the size of billboard bigger")

        ### Smaller billboard size
        self.smallerSizeButton = QtWidgets.QPushButton(self.controlWidget)
        self.smallerSizeButton.setText("Make Smaller")
        self.smallerSizeButton.setToolTip("Make the size of billboard smaller")

        ### Switch image
        self.successKidButton = QtWidgets.QPushButton(self.controlWidget)
        self.successKidButton.setText("Success Kid")
        self.successKidButton.setToolTip("Swith the image of the billboards to success kid")

        self.qgisIDButton = QtWidgets.QPushButton(self.controlWidget)
        self.qgisIDButton.setText("QGIS ID")
        self.qgisIDButton.setToolTip("Swith the image of the billboards to QGIS ID logo")

        ### Put to layout
        self.controlLayout.addWidget(self.info)
        self.controlLayout.addWidget(self.randomSizeButton)
        self.controlLayout.addWidget(self.biggerSizeButton)
        self.controlLayout.addWidget(self.smallerSizeButton)
        self.controlLayout.addWidget(self.successKidButton)
        self.controlLayout.addWidget(self.qgisIDButton)


        ### Camera
        self.camera = self.Display.camera()
        self.camera.lens().setPerspectiveProjection(45.0, 16.0/9.0, 0.1, 100.0)
        originalPosition = QtGui.QVector3D(0, 10.0, 20.0)
        self.camera.setPosition(originalPosition)
        originalViewCenter = QtGui.QVector3D(0, 0, 0)
        self.camera.setViewCenter(originalViewCenter)
        upVector = QtGui.QVector3D(0, 1.0, 0)
        self.camera.setUpVector(upVector)

        ### Camera control
        self.camController = Qt3DExtras.QFirstPersonCameraController(self.rootEntity)
        self.camController.setCamera(self.camera)

        ### Cuboid mesh data
        self.cuboid = Qt3DExtras.QCuboidMesh()
        self.cuboid.setXExtent(2)
        self.cuboid.setYExtent(2)
        self.cuboid.setZExtent(2)

        ### Cuboid mesh transform
        self.cuboidTransform = Qt3DCore.QTransform()
        self.cuboidTransform.setScale(3.0)
        self.cuboidTransform.setTranslation(QtGui.QVector3D(15.0, 0.0, 0.0))

        ### Cuboid material
        self.cuboidMaterial = Qt3DExtras.QPhongAlphaMaterial(self.rootEntity)
        self.cuboidMaterial.setDiffuse(QtGui.QColor(255, 0, 0, 255))
        self.cuboidMaterial.setAmbient(QtGui.QColor(255, 0, 0, 255))
        self.cuboidMaterial.setSpecular(QtGui.QColor(255, 0, 0, 255))
        self.cuboidMaterial.setAlpha(0.5)
        self.cuboidMaterial.setShininess(1.0)

        ### Cuboid entity
        self.cuboidEntity = Qt3DCore.QEntity(self.rootEntity)
        self.cuboidEntity.addComponent(self.cuboid)
        self.cuboidEntity.addComponent(self.cuboidTransform)
        self.cuboidEntity.addComponent(self.cuboidMaterial)
        self.cuboidEntity.setEnabled(True)

        ### Blue Plane mesh
        self.planeMesh = Qt3DExtras.QPlaneMesh()
        self.planeMesh.setWidth(20)
        self.planeMesh.setHeight(20)

        self.planeMaterial = Qt3DExtras.QPhongAlphaMaterial(self.rootEntity)
        self.planeMaterial.setAmbient(QtGui.QColor(0, 0, 255, 255))

        self.planeEntity = Qt3DCore.QEntity(self.rootEntity)
        self.planeEntity.addComponent(self.planeMesh)
        self.planeEntity.addComponent(self.planeMaterial)
        self.planeEntity.setEnabled(True)

        ### Green Sphere
        self.sphereMesh = Qt3DExtras.QSphereMesh()
        self.greenMaterial = Qt3DExtras.QPhongAlphaMaterial(self.rootEntity)
        self.greenMaterial.setAmbient(QtGui.QColor(0, 255, 0, 255))
        self.sphereTransform = Qt3DCore.QTransform()
        self.sphereTransform.setTranslation(QtGui.QVector3D(0.0, 5.0, 0.0))

        self.sphereEntity = Qt3DCore.QEntity(self.rootEntity)
        self.sphereEntity.addComponent(self.sphereMesh)
        self.sphereEntity.addComponent(self.greenMaterial)
        self.sphereEntity.addComponent(self.sphereTransform)
        self.sphereEntity.setEnabled(True)


        ### Billboard
        ### Points
        pos = [QtGui.QVector3D(1, 1, 0), QtGui.QVector3D(-1, 2, 8), QtGui.QVector3D(1, 1, 7), QtGui.QVector3D(0, 0, 4)]
        
        ### Billboard Geometry
        self.billboardGeometry = BillboardGeometry()
        self.billboardGeometry.setPoints(pos)
        
        ### Billboard Geometry Renderer
        self.billboardGeometryRenderer = Qt3DRender.QGeometryRenderer()
        self.billboardGeometryRenderer.setPrimitiveType( Qt3DRender.QGeometryRenderer.Points )
        self.billboardGeometryRenderer.setGeometry( self.billboardGeometry )
        self.billboardGeometryRenderer.setVertexCount( self.billboardGeometry.count() )
        
        ### Billboard Material
        self.billboardMaterial = BillboardMaterial()
        
        ### Billboard Transform
        self.billboardTransform = Qt3DCore.QTransform()
        self.billboardTransform.setTranslation(QtGui.QVector3D(0.0, 1.5, 0.0))
        
        ### Billboard Entity
        self.billboardEntity = Qt3DCore.QEntity(self.rootEntity)
        self.billboardEntity.addComponent(self.billboardMaterial)
        self.billboardEntity.addComponent(self.billboardGeometryRenderer)
        self.billboardEntity.addComponent(self.billboardTransform)
        self.billboardEntity.setEnabled(True)
        
        
        ### Signal and slot for widgets
        self.randomSizeButton.pressed.connect(self.rs)
        
        self.biggerSizeButton.pressed.connect(self.bs)
        
        self.smallerSizeButton.pressed.connect(self.ss)
        
        self.successKidButton.pressed.connect(self.sk)
        
        self.qgisIDButton.pressed.connect(self.qg)

        self.Display.setRootEntity(self.rootEntity)

        ###
        self.Display.heightChanged.connect(self.correctCameraRatio)
        self.Display.widthChanged.connect(self.correctCameraRatio)

    def correctCameraRatio(self):
        self.camera.setAspectRatio(self.Display.width()/self.Display.height())

    def rs(self):
        randomNumber = (QtCore.qrand() % 20) * 10 + 10 ### Random number multiple of 10 between 0 to 200, mull
        self.billboardMaterial.setSize(QtCore.QSizeF(randomNumber, randomNumber))

    def bs(self):
        self.billboardMaterial.setSize(self.billboardMaterial.size() + QtCore.QSizeF(10, 10))

    def ss(self):
        ### Minus size -. reverse the orientation of the image
        self.billboardMaterial.setSize(self.billboardMaterial.size() - QtCore.QSizeF(10, 10))

    def sk(self):
        self.billboardMaterial.setTexture2DFromImagePath( "qrc:/shaders/success-kid.png")

    def qg(self):
        self.billboardMaterial.setTexture2DFromImagePath( "qrc:/shaders/QGIS-ID.png")

if __name__ == "__main__":
    print("Billboard-Example Window Startup")
    app = QtWidgets.QApplication([])
    app.setApplicationName(WindowTitle)
    window = MainWindow()
    print(datetime.datetime.now().strftime('%H:%M:%S:'),"Billboard-Example Window Started\n")
    window.show()
    window.resize(906, 634)
    sys.exit(app.exec())
