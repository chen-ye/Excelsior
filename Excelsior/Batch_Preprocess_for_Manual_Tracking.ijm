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
    if (File.isDirectory(dir + list[i])) {
      print("Now processing " + list[i]);
      getStack(dir, list[i]);
    }
    //Every 5 cycles close all windows
    if (i % 5 == 0) {
      run("Close All");
    }
  }
  print("All images processed!");
}

function getStack(dir, stack)  {
  fileList = getFileList(dir + stack + "png/");
  stackDone = false;
  stackName = substring(stack, 0, lastIndexOf(stack,"/"));
  if (!overwrite) {
    if (File.exists(dir + stack + "Processed")){
      print(stack + "has already been processed!  Skipping...");
      stackDone = true;
    }
  }
  //Open the tif version if it already exists
  if (File.exists(dir + stack + stackName + ".tif") && !stackDone) {
    print("Opening .tif stack: " + stackName + ".tif");
    open(dir + stack + stackName + ".tif");
    processStack(dir, stack, stackName + ".tif");
    stackDone = true;
  }
  //Otherwise open the png sequence.
  i = 0;
  while (!stackDone) {
    if (i < fileList.length) {
      if (endsWith(fileList[i], ".png")) {
        print("Opening " + fileList[i]);
        run("Image Sequence...", "open=[" + dir + stack + "png/" + file + "] sort");
        stackName = substring(stack, 0, lastIndexOf(stack,"/"));
        saveAs("Tiff", dir + stack + stackName);
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
  stackName = substring(stack, 0, lastIndexOf(stack,"/"));
  // run("Rotate 90 Degrees Right");
  run("Properties...", "channels=1 slices=1 frames="+ nSlices + " unit=cm pixel_width=42.700 pixel_height=42.700 voxel_depth=1.0000 frame=[1 sec]");
  File.makeDirectory(dir + stack + "Manual/")
  run("Preprocess for Manual Tracking");
}
