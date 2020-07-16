from PyQt5 import QtWidgets,QtCore,QtGui,Qt , Qt3DAnimation,Qt3DCore,Qt3DExtras,Qt3DInput,Qt3DLogic,Qt3DRender , QtQml
from PyQt5.QtCore import pyqtProperty, pyqtSignal # pylint: disable=no-name-in-module
import shaders

class BillboardMaterial(Qt3DRender.QMaterial):
    def __init__(self, parent = None):
        super(BillboardMaterial, self).__init__(parent)
        self.Size = Qt3DRender.QParameter( "BB_SIZE", QtCore.QSizeF(100, 100), self )
        self.WindowSize = Qt3DRender.QParameter( "WIN_SCALE", QtCore.QSizeF(800, 600), self )
        self.addParameter( self.Size )
        self.addParameter( self.WindowSize )

        self.image = Qt3DRender.QTextureImage()
        self.image.setSource(QtCore.QUrl("qrc:/shaders/success-kid.png"))

        ### Texture2D
        texture2D = Qt3DRender.QTexture2D()
        texture2D.setGenerateMipMaps(False)
        texture2D.setMagnificationFilter(Qt3DRender.QTexture2D.Linear)
        texture2D.setMinificationFilter(Qt3DRender.QTexture2D.Linear)

        texture2D.addTextureImage(self.image)

        self.Texture2D = Qt3DRender.QParameter( "tex0", texture2D, self )

        self.addParameter(self.Texture2D)

        ### Shader program
        self.shaderProgram = Qt3DRender.QShaderProgram( self )
        self.shaderProgram.setVertexShaderCode(   Qt3DRender.QShaderProgram.loadSource( QtCore.QUrl( "qrc:/shaders/billboards.vert" ) ) )
        self.shaderProgram.setFragmentShaderCode( Qt3DRender.QShaderProgram.loadSource( QtCore.QUrl( "qrc:/shaders/billboards.frag" ) ) )
        self.shaderProgram.setGeometryShaderCode( Qt3DRender.QShaderProgram.loadSource( QtCore.QUrl( "qrc:/shaders/billboards.geom" ) ) )

        ### Render Pass
        self.renderPass = Qt3DRender.QRenderPass( self )
        self.renderPass.setShaderProgram(self.shaderProgram)

        ### without self filter the default forward renderer would not render self
        self.filterKey = Qt3DRender.QFilterKey()
        self.filterKey.setName(  "renderingStyle" )
        self.filterKey.setValue( "forward" )

        ### Technique
        self.technique = Qt3DRender.QTechnique()
        self.technique.addRenderPass(self.renderPass)
        self.technique.addFilterKey(self.filterKey)
        self.technique.graphicsApiFilter().setApi( Qt3DRender.QGraphicsApiFilter.OpenGL )
        self.technique.graphicsApiFilter().setProfile( Qt3DRender.QGraphicsApiFilter.CoreProfile )
        self.technique.graphicsApiFilter().setMajorVersion( 3 )
        self.technique.graphicsApiFilter().setMinorVersion( 1 )

        ### Effect
        self.effect = Qt3DRender.QEffect( self )
        self.effect.addTechnique(self.technique)

        self.setEffect( self.effect )

    def setSize(self, size):
        self.Size.setValue(size)

    def size(self):
        return self.Size.value()

    def setWindowSize(self, size):
        self.WindowSize.setValue(size)

    def windowSize(self):
        return self.WindowSize.value()

    def setTexture2D(self, texture2D):
        self.Texture2D.setValue(texture2D)#QtCore.QVariant.fromValue(texture2D)) #TODO: Check this. fromValue seems to not exist...

    def texture2D(self):
        variant = self.Texture2D.value()
        return Qt3DRender.QTexture2D(variant) #TODO: check this

    def setTexture2DFromImagePath(self, imagePath):
        ### Texture Image
        image = Qt3DRender.QTextureImage()
        image.setSource(QtCore.QUrl( imagePath ))

        ### Texture2D
        texture2D = Qt3DRender.QTexture2D()
        texture2D.setGenerateMipMaps(False)
        texture2D.setMagnificationFilter(Qt3DRender.QTexture2D.Linear)
        texture2D.setMinificationFilter(Qt3DRender.QTexture2D.Linear)

        texture2D.addTextureImage(image)

        self.setTexture2D(texture2D)
