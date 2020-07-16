from PyQt5 import QtWidgets,QtCore,QtGui,Qt , Qt3DAnimation,Qt3DCore,Qt3DExtras,Qt3DInput,Qt3DLogic,Qt3DRender , QtQml
from PyQt5.QtCore import pyqtProperty, pyqtSignal # pylint: disable=no-name-in-module
import ctypes

class BillboardGeometry(Qt3DRender.QGeometry):
    S_countChanged = pyqtSignal(int)
    def __init__(self, parent=None):
        super(BillboardGeometry, self).__init__(parent)
        self.PositionAttribute = Qt3DRender.QAttribute(self)
        self.VertexBuffer = Qt3DRender.QBuffer( Qt3DRender.QBuffer.VertexBuffer, self )
        self.PositionAttribute.setAttributeType( Qt3DRender.QAttribute.VertexAttribute )
        self.PositionAttribute.setBuffer( self.VertexBuffer )
        self.PositionAttribute.setVertexBaseType( Qt3DRender.QAttribute.Float )
        self.PositionAttribute.setVertexSize( 3 )
        self.PositionAttribute.setName( Qt3DRender.QAttribute.defaultPositionAttributeName() )
        self.addAttribute( self.PositionAttribute )

    def count(self):
        return self.VertexCount

    def setPoints(self, vertices): #TODO: complete this
        vertexBufferData = QtCore.QByteArray()
        #vertexBufferData.resize( len(vertices) * 3 * sizeof( float ) )
        #rawVertexArray = reinterpret_cast<float *>( vertexBufferData.data() )
        #idx = 0
        #for v in vertices:
        #    rawVertexArray.append(v.x())
        #    rawVertexArray.append(v.y())
        #    rawVertexArray.append(v.z())
        for v in vertices:
            vertexBufferData.append(bin(ctypes.c_uint.from_buffer(ctypes.c_float(v.x())).value).replace('0b', '').rjust(32, '0'))
            vertexBufferData.append(bin(ctypes.c_uint.from_buffer(ctypes.c_float(v.y())).value).replace('0b', '').rjust(32, '0'))
            vertexBufferData.append(bin(ctypes.c_uint.from_buffer(ctypes.c_float(v.z())).value).replace('0b', '').rjust(32, '0'))

        self.VertexCount = len(vertices)
        self.VertexBuffer.setData( vertexBufferData )

        self.S_countChanged.emit(self.VertexCount)
