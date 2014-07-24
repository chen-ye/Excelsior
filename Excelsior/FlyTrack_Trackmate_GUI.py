import ij.IJ as IJ
import ij.ImageJ as ImageJ
import ij.ImagePlus as ImagePlus
import ij.WindowManager as WindowManager
import ij.plugin.PlugIn as PlugIn

import fiji.plugin.trackmate.gui.GuiUtils as GuiUtils
import fiji.plugin.trackmate.gui.TrackMateGUIController as TrackMateGUIController

import fiji.plugin.trackmate.TrackMate as TrackMate
import fiji.plugin.trackmate.Settings as Settings
import fiji.plugin.trackmate.Model as Model

import fiji.plugin.trackmate.Logger as Logger

import fiji.plugin.trackmate.detection.LogDetectorFactory as LogDetectorFactory
import fiji.plugin.trackmate.detection.DetectorKeys as DetectorKeys
import fiji.plugin.trackmate.tracking.LAPTrackerFactory as LAPTrackerFactory
import fiji.plugin.trackmate.tracking.LAPUtils as LAPUtils

import fiji.plugin.trackmate.features.FeatureFilter as FeatureFilter
import fiji.plugin.trackmate.features.spot.SpotContrastAndSNRAnalyzerFactory as SpotContrastAndSNRAnalyzerFactory
import fiji.plugin.trackmate.features.spot.SpotContrastAndSNRAnalyzer as SpotContrastAndSNRAnalyzer
import fiji.plugin.trackmate.features.spot.SpotIntensityAnalyzerFactory as SpotIntensityAnalyzerFactory
import fiji.plugin.trackmate.features.spot.SpotIntensityAnalyzer as SpotIntensityAnalyzer
import fiji.plugin.trackmate.features.spot.SpotRadiusEstimatorFactory as SpotRadiusEstimatorFactory
import fiji.plugin.trackmate.features.spot.SpotRadiusEstimator as SpotRadiusEstimator
import fiji.plugin.trackmate.features.spot.SpotMorphologyAnalyzerFactory as SpotMorphologyAnalyzerFactory
import fiji.plugin.trackmate.features.spot.SpotMorphologyAnalyzer as SpotMorphologyAnalyzer
import fiji.plugin.trackmate.features.edges.EdgeTargetAnalyzer as EdgeTargetAnalyzer
import fiji.plugin.trackmate.features.edges.EdgeTimeLocationAnalyzer as EdgeTimeLocationAnalyzer
import fiji.plugin.trackmate.features.edges.EdgeVelocityAnalyzer as EdgeVelocityAnalyzer
import fiji.plugin.trackmate.features.track.TrackDurationAnalyzer as TrackDurationAnalyzer
import fiji.plugin.trackmate.features.track.TrackIndexAnalyzer as TrackIndexAnalyzer
import fiji.plugin.trackmate.features.track.TrackLocationAnalyzer as TrackLocationAnalyzer
import fiji.plugin.trackmate.features.track.TrackSpeedStatisticsAnalyzer as TrackSpeedStatisticsAnalyzer
import fiji.plugin.trackmate.features.track.TrackSpotFeatureAnalyzer as TrackSpotFeatureAnalyzer



trackmate = TrackMate()
settings = Settings()
model = Model()

# Get currently selected image
imp = WindowManager.getCurrentImage()

GuiUtils.userCheckImpDimensions(imp)

#-------------------------
# Instantiate model object
#-------------------------
model.setPhysicalUnits(imp.getCalibration().getUnits(), imp.getCalibration().getTimeUnit())
  
# Set logger
model.setLogger(Logger.IJ_LOGGER)

#------------------------
# Prepare settings object
#------------------------
settings.setFrom(imp)

settings.tstart = 2
settings.tend = 26

print('min threshold: ' + str(imp.getProcessor().getMinThreshold()))

# Configure detector
settings.detectorFactory = LogDetectorFactory()
settings.detectorSettings = {
    DetectorKeys.KEY_DO_SUBPIXEL_LOCALIZATION : True,
    DetectorKeys.KEY_RADIUS : .30,
    DetectorKeys.KEY_TARGET_CHANNEL : 1,
    DetectorKeys.KEY_THRESHOLD : 50,
    DetectorKeys.KEY_DO_MEDIAN_FILTERING : False,

}
   
# Configure tracker
settings.trackerFactory = LAPTrackerFactory()
settings.trackerSettings = LAPUtils.getDefaultLAPSettingsMap()
settings.trackerSettings['LINKING_MAX_DISTANCE'] = 2.0
settings.trackerSettings['GAP_CLOSING_MAX_DISTANCE']=4.0
settings.trackerSettings['MAX_FRAME_GAP']= 2
linkingFeaturePenalties = settings.trackerSettings['LINKING_FEATURE_PENALTIES']
linkingFeaturePenalties['POSITION_X'] = 9.9999E20
linkingFeaturePenalties['QUALITY'] = 1.0
gapClosingFeaturePenalties = settings.trackerSettings['GAP_CLOSING_FEATURE_PENALTIES']
gapClosingFeaturePenalties['POSITION_X'] = 9.9999E20

# Add spot filters
settings.initialSpotFilterValue = 0
settings.addSpotFilter(FeatureFilter('QUALITY', 50.0, True))
settings.addTrackFilter(FeatureFilter('TRACK_DISPLACEMENT', 7.0, True))
settings.addTrackFilter(FeatureFilter('NUMBER_SPOTS', 5, True))

# Add the analyzers for some spot features.
# You need to configure TrackMate with analyzers that will generate 
# the data you need. 
settings.addSpotAnalyzerFactory(SpotIntensityAnalyzerFactory())
settings.addSpotAnalyzerFactory(SpotContrastAndSNRAnalyzerFactory())
settings.addSpotAnalyzerFactory(SpotRadiusEstimatorFactory())
settings.addSpotAnalyzerFactory(SpotMorphologyAnalyzerFactory())

# Add analyhzers for edges
settings.addEdgeAnalyzer(EdgeTargetAnalyzer())
settings.addEdgeAnalyzer(EdgeTimeLocationAnalyzer())
settings.addEdgeAnalyzer(EdgeVelocityAnalyzer())
  
# Add an analyzer for some track features, such as the track mean speed.
settings.addTrackAnalyzer(TrackSpeedStatisticsAnalyzer())
settings.addTrackAnalyzer(TrackDurationAnalyzer())
settings.addTrackAnalyzer(TrackIndexAnalyzer())
settings.addTrackAnalyzer(TrackLocationAnalyzer())
settings.addTrackAnalyzer(TrackSpotFeatureAnalyzer())

  
print(str(settings))

controller = TrackMateGUIController(trackmate)
GuiUtils.positionWindow(controller.getGUI(), imp.getWindow())