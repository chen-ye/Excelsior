from ij import IJ, ImagePlus, ImageStack, WindowManager

imp = WindowManager.getCurrentImage()

fileinfo = imp.getOriginalFileInfo()
filename = fileinfo.fileName
directory = fileinfo.directory

def extractFrames(imp, interval, offset, nFrames):
 """ Extract a stack containing a subset of frames from a stack """
 stack = imp.getImageStack()
 man = ImageStack(imp.width, imp.height)

 for i in range(0, nFrames):
   index = imp.getStackIndex(0, 1, i * interval + offset)
   man.addSlice(stack.getProcessor(index))
 return ImagePlus("Manual_" + filename, man)

mimp = extractFrames(imp, 45, 3, 4)

IJ.save(mimp, directory + '/Manual/Manual.tif')
