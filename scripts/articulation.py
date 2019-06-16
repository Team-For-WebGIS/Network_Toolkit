from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterVectorDestination
from qgis.core import QgsProcessingParameterFeatureSource
import processing


class Ariticulation(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource('inputline', '线图层（网络图层）', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSource('inputnode', '节点图层', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('threshhold', '点到网络的距离容差', type=QgsProcessingParameterNumber.Double, defaultValue=50))
        self.addParameter(QgsProcessingParameterVectorDestination('Result', '输出结果', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # articulation
        alg_params = {
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'arc_backward_column': None,
            'arc_column': None,
            'input': parameters['inputline'],
            'method': 1,
            'node_column': None,
            'points': parameters['inputnode'],
            'threshold': parameters['threshhold'],
            'output': parameters['Result']
        }
        outputs['Articulation'] = processing.run('grass7:v.net.bridge', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return '计算网络中的重要节点'

    def displayName(self):
        return '计算网络中的重要节点'

    def group(self):
        return 'network'

    def groupId(self):
        return 'network'

    def createInstance(self):
        return Ariticulation()
