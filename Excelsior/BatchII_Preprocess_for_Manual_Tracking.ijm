//Script to prepare a subset of frames within the video for manual review.
//Video capture series needs to be processed into frames.  This script reads .png frame sequences.
//This manipulates directories, and works with UNIX systems only
//Chen Ye 2014

overwrite = true;

metaDir = getDirectory("Choose a Directory");
setBatchMode(true);
executeSubdirs(metaDir);

function executeSubdirs(dir)  {
	list = getFileList(dir);
	for (i=0; i<list.length; i++) {
		stack = list[i];
		if (File.isDirectory(dir + stack) && startsWith(stack, "VFlylapse")) {
			stackName = substring(stack, 0, lastIndexOf(stack,"/"));
			print("Now processing " + stack);
			if (File.exists(dir + stack + "Manual") && !overwrite) {
				print(stack + " has already been tracked!  Skipping...");
			} else {
				if (File.exists(dir + stack + "Processed")) {
					batchTrack(dir, stack);
				} else {
					print(stack + " has not been processed yet!  Skipping...");
				}
			}
		}
		//Every cycle close all windows
		if (i % 1 == 0) {
			run("Close All");
			run("Collect Garbage");
		}
	}

	print("Batch Operation Complete!");
}

function batchTrack(dir, stack)  {
	stackName = substring(stack, 0, lastIndexOf(stack,"/"));
	run("Open Video Rack", "choose=" + dir + stack);
	run("Properties...", "channels=1 slices=1 frames="+ nSlices + " unit=cm pixel_width=42.700 pixel_height=42.700 voxel_depth=1.0000 frame=[1 sec]");
  	File.makeDirectory(dir + stack + "Manual/")
  	run("Preprocess for Manual Tracking");
	open(dir + stack + "Manual/Manual.tif");
	selectWindow("Manual.tif");
	run("Stack to Images");
	run("Merge Channels...", "c1=Manual-0001 c2=Manual-0002 c3=Manual-0003 c5=Manual-0004 create");
	run("RGB Color");
	run("Enhance Contrast", "saturated=0.35");
	medianName = "Median_" + stackName + ".tif";
	selectWindow(medianName);
	setMinAndMax(100, 300);
	imageCalculator("Add create", "Composite (RGB)",medianName);
	selectWindow("Result of Composite (RGB)");
	saveAs("Tiff", dir + stack + "Manual/Manual_ColorComposite_" + stackName);
}


