from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterPoint
from qgis.core import QgsProcessingParameterVectorLayer
import processing


class Shortpath(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('v1', '线图层 (作为网络图层)', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterPoint('p1', '起点 (x,y)', defaultValue=''))
        self.addParameter(QgsProcessingParameterPoint('p2', '终点 (x,y)', defaultValue=''))
        self.addParameter(QgsProcessingParameterFeatureSink('Shortest_path', 'shortest_path', type=QgsProcessing.TypeVectorLine, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Shortest path (point to point)
        alg_params = {
            'DEFAULT_DIRECTION': 2,
            'DEFAULT_SPEED': 50,
            'DIRECTION_FIELD': None,
            'END_POINT': parameters['p2'],
            'INPUT': parameters['v1'],
            'SPEED_FIELD': None,
            'START_POINT': parameters['p1'],
            'STRATEGY': 0,
            'TOLERANCE': 0,
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': '',
            'OUTPUT': parameters['Shortest_path']
        }
        outputs['ShortestPathPointToPoint'] = processing.run('native:shortestpathpointtopoint', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Shortest_path'] = outputs['ShortestPathPointToPoint']['OUTPUT']
        return results

    def name(self):
        return 'shortpath'

    def displayName(self):
        return 'shortpath'

    def group(self):
        return 'network'

    def groupId(self):
        return 'network'

    def createInstance(self):
        return Shortpath()
