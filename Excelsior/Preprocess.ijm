//Script to pre-process all stacks in a capture series.  Stacks are seperated by folder.
//This manipulates directories, and works with UNIX systems only
//Chen Ye 2014

overwrite = false;

metaDir = getDirectory("Choose a Directory"); 
executeSubdirs(metaDir);

setBatchMode(true);

function executeSubdirs(dir)  {
	list = getFileList(dir);
	for (i=0; i<list.length; i++) {
		if (File.isDirectory(dir + list[i]))
			print("Now processing " + list[i]);
			getStack(dir, list[i]);
	}
}

function getStack(dir, stack)  {
	fileList = getFileList(dir + stack);
	stackDone = false;	
	i = 0;
	if (!overwrite) {
		if (File.exists(dir + stack + "Processed")){
			print(stack + "has already been processed!  Skipping...");
			stackDone = true;
		}
	}
	while (!stackDone) {
		if (i < fileList.length) {

			if (endsWith(fileList[i], ".jpg")) {
				print("Opening " + fileList[i]);
				processStack(dir, stack, fileList[i]);
				stackDone = true;
			}
			else {
				i++;
			}
		} else {
			print("Cannot find stack for " + stack + " !");
			stackDone = true;
		}
	}
}

function processStack(dir, stack, file) {
	run("Image Sequence...", "open=[" + dir + stack + file + "] sort");
	stackName = substring(stack, 0, lastIndexOf(stack,"/"));
	run("Rotate 90 Degrees Right");
	run("8-bit");
	run("Invert", "stack");
	run("Z Project...", "projection=Median");
	medianName = "Median_" + stackName;
	saveAs("Tiff", dir + stack + medianName);
	selectWindow(stackName);
	imageCalculator("Subtract create stack", stackName, medianName + ".tif");
	selectWindow("Result of " + stackName);
	run("Properties...", "channels=1 slices=1 frames="+ nSlices + " unit=cm pixel_width=42.700 pixel_height=42.700 voxel_depth=1.0000 frame=[1 sec]");
	File.makeDirectory(dir + stack + "Processed/")
	run("Image Sequence... ", "format=TIFF name=[Preprocessed " + stackName +"] start=0 digits=4 save=[" + dir + stack + "Processed/Preprocessed " + stackName + ".tif]");
}
