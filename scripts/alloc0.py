from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterVectorDestination
from qgis.core import QgsProcessingParameterFeatureSource
import processing


class Model(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource('line', '线图层（作为弧段）', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSource('point', '点图层（作为节点）', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('threshold', '阈值', type=QgsProcessingParameterNumber.Double, defaultValue=50))
        self.addParameter(QgsProcessingParameterVectorDestination('Alloction_result', '输出结果', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # v.net.alloc
        alg_params = {
            '-g': False,
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'arc_backward_column': None,
            'arc_column': None,
            'arc_type': 0,
            'center_cats': '1-100000',
            'input': parameters['line'],
            'node_column': None,
            'points': parameters['point'],
            'threshold': parameters['threshold'],
            'output': parameters['Alloction_result']
        }
        outputs['Vnetalloc'] = processing.run('grass7:v.net.alloc', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Alloction_result'] = outputs['Vnetalloc']['output']
        return results

    def name(self):
        return '子网划分'

    def displayName(self):
        return '子网划分'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model()
