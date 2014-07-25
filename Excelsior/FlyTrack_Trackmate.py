from ij import IJ, ImagePlus, ImageStack, measure, WindowManager
import java.io.File as File
import fiji.plugin.trackmate.Settings as Settings
import fiji.plugin.trackmate.Model as Model
import fiji.plugin.trackmate.SelectionModel as SelectionModel
import fiji.plugin.trackmate.TrackMate as TrackMate
import fiji.plugin.trackmate.Logger as Logger
import fiji.plugin.trackmate.Spot as Spot
import fiji.plugin.trackmate.gui.TrackMateGUIController as TrackMateGUIController
import fiji.plugin.trackmate.detection.DetectorKeys as DetectorKeys
import fiji.plugin.trackmate.detection.LogDetectorFactory as LogDetectorFactory
import fiji.plugin.trackmate.tracking.FastLAPTrackerFactory as FastLAPTrackerFactory
import fiji.plugin.trackmate.tracking.LAPUtils as LAPUtils
import fiji.plugin.trackmate.visualization.hyperstack.HyperStackDisplayer as HyperStackDisplayer
import fiji.plugin.trackmate.visualization.TrackMateModelView as TrackMateModelView
import fiji.plugin.trackmate.visualization.SpotColorGeneratorPerTrackFeature as SpotColorGeneratorPerTrackFeature
import fiji.plugin.trackmate.visualization.PerTrackFeatureColorGenerator as PerTrackFeatureColorGenerator
import fiji.plugin.trackmate.features.FeatureFilter as FeatureFilter
import fiji.plugin.trackmate.features.FeatureAnalyzer as FeatureAnalyzer
import fiji.plugin.trackmate.features.SpotFeatureCalculator as SpotFeatureCalculator
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
import fiji.plugin.trackmate.action.ExportStatsToIJAction as ExportStatsToIJAction
import fiji.plugin.trackmate.action.ExportTracksToXML as ExportTracksToXML
import fiji.plugin.trackmate.action.CaptureOverlayAction as CaptureOverlayAction
import fiji.plugin.trackmate.io.TmXmlReader as TmXmlReader
import fiji.plugin.trackmate.io.TmXmlWriter as TmXmlWriter
import fiji.plugin.trackmate.features.ModelFeatureUpdater as ModelFeatureUpdater
import fiji.plugin.trackmate.util.TMUtils as TMUtils


# Get currently selected image
imp = WindowManager.getCurrentImage()
#imp = IJ.openImage('http://fiji.sc/samples/FakeTracks.tif')
#imp.show()


#-------------------------
# Instantiate model object
#-------------------------

model = Model()
model.setPhysicalUnits(imp.getCalibration().getUnits(), imp.getCalibration().getTimeUnit())

# Set logger
model.setLogger(Logger.IJ_LOGGER)

#------------------------
# Prepare settings object
#------------------------

settings = Settings()
settings.setFrom(imp)

settings.tstart = 2
settings.tend = settings.tend - 5

print('min threshold: ' + str(imp.getProcessor().getMinThreshold()))

# Configure detector
settings.detectorFactory = LogDetectorFactory()
settings.detectorSettings = {
    DetectorKeys.KEY_DO_SUBPIXEL_LOCALIZATION : True,
    DetectorKeys.KEY_RADIUS : .30,
    DetectorKeys.KEY_TARGET_CHANNEL : 1,
    DetectorKeys.KEY_THRESHOLD : 50.,
    DetectorKeys.KEY_DO_MEDIAN_FILTERING : False,

}

# Configure tracker
settings.trackerFactory = FastLAPTrackerFactory()
settings.trackerSettings = LAPUtils.getDefaultLAPSettingsMap()

deltaT = settings.dt
settings.trackerSettings['LINKING_MAX_DISTANCE'] = 2.0 * deltaT
settings.trackerSettings['GAP_CLOSING_MAX_DISTANCE']=4.0 * deltaT
settings.trackerSettings['MAX_FRAME_GAP']= 2
linkingFeaturePenalties = settings.trackerSettings['LINKING_FEATURE_PENALTIES']
linkingFeaturePenalties['POSITION_X'] = 9.9999E20
linkingFeaturePenalties['QUALITY'] = 1.0
gapClosingFeaturePenalties = settings.trackerSettings['GAP_CLOSING_FEATURE_PENALTIES']
gapClosingFeaturePenalties['POSITION_X'] = 9.9999E20

# Add filters
settings.initialSpotFilterValue = 0
# settings.addSpotFilter(FeatureFilter('QUALITY', 50.0, True))
settings.addTrackFilter(FeatureFilter('TRACK_DISPLACEMENT', .75, True))
settings.addTrackFilter(FeatureFilter('NUMBER_SPOTS', 5, True))

# Add the analyzers for some spot features.
# You need to configure TrackMate with analyzers that will generate
# the data you need.
img = TMUtils.rawWraps(settings.imp)
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

#----------------------
# Instantiate trackmate
#----------------------

trackmate = TrackMate(model, settings)

#------------
# Execute all
#------------

trackmate.process()

#----------------
# Display results
#----------------

model.getLogger().log('Found ' + str(model.getTrackModel().nTracks(True)) + ' tracks.')

loglist = []
selectionModel = SelectionModel(model)
displayer =  HyperStackDisplayer(model, selectionModel, imp)

# Configure display settings
displayer.setDisplaySettings(TrackMateModelView.KEY_SPOT_COLORING, SpotColorGeneratorPerTrackFeature(trackmate.getModel(), Spot.QUALITY))
displayer.setDisplaySettings(TrackMateModelView.KEY_TRACK_COLORING, PerTrackFeatureColorGenerator(trackmate.getModel(), TrackIndexAnalyzer.TRACK_INDEX))
displayer.setDisplaySettings(TrackMateModelView.KEY_TRACK_DISPLAY_MODE, TrackMateModelView.TRACK_DISPLAY_MODE_LOCAL)
displayer.setDisplaySettings(TrackMateModelView.KEY_TRACK_DISPLAY_DEPTH, int(round(10/deltaT)))

# Display the displayer
displayer.render()
displayer.refresh()

# The feature model, that stores edge and track features.
fm = model.getFeatureModel()

for id in model.getTrackModel().trackIDs(True):

    # Fetch the track feature from the feature model.
    v = fm.getTrackFeature(id, 'TRACK_MEDIAN_SPEED')
    model.getLogger().log('')
    trackinfo = 'Track ' + str(id) + ': median velocity = ' + str(v) + ' ' + model.getSpaceUnits() + '/' + model.getTimeUnits()
    model.getLogger().log(trackinfo)
    loglist.append('\n' +  trackinfo)

    track = model.getTrackModel().trackSpots(id)
    for spot in track:
        sid = spot.ID()
        # Fetch spot features directly from spot.
        x=spot.getFeature('POSITION_X')
        y=spot.getFeature('POSITION_Y')
        t=spot.getFeature('FRAME')
        q=spot.getFeature('QUALITY')
        snr=spot.getFeature('SNR')
        mean=spot.getFeature('MEAN_INTENSITY')
	spotinfo = '\tspot ID = ' + str(sid) + ': x='+str(x)+', y='+str(y)+', t='+str(t)+', q='+str(q) + ', snr='+str(snr) + ', mean = ' + str(mean)
        model.getLogger().log(spotinfo)
	loglist.append('\n' +  spotinfo)

capturer = CaptureOverlayAction()
capturer.execute(trackmate)

#---------------
# Export results
#---------------

dir = File(settings.imageFolder + '/../Tracked')
dir.mkdir()

cap = WindowManager.getImage("TrackMate capture")
if not WindowManager.checkForDuplicateName:
	ij.save(cap, dir + '/Captured_' + settings.imageFileName + '.tif')
else: 
	loglist.append ('Warning: Capture not saved because there are duplicate ImagePlus names')

tracks = File(dir, 'Tracked_TracksOnly.xml')
#exporter = ExportTracksToXML(controller)
ExportTracksToXML.export(model, settings, tracks)

file = File(dir, 'Tracked.xml')

logger = model.getLogger()
writer = TmXmlWriter( file, logger )

logstring = ''.join( loglist )
writer.appendLog( logstring )
writer.appendModel( trackmate.getModel() )
writer.appendSettings( trackmate.getSettings() )
