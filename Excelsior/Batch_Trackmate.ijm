
overwrite = false;

metaDir = getDirectory("Choose a Directory");
executeSubdirs(metaDir);
setBatchMode(true);


function executeSubdirs(dir)  {
	list = getFileList(dir);
	for (i=0; i<list.length; i++) {
		stack = list[i];
		if (File.isDirectory(dir + stack) && startsWith(stack, "VFlylapse")) {
			stackName = substring(stack, 0, lastIndexOf(stack,"/"));
			print("Now processing " + stack);
			if (File.exists(dir + stack + "Tracked/Tracked_Batch_Preprocessed_" + stackName + ".tif.xml") && !overwrite) {
				print(stack + " has already been tracked!  Skipping...");
			} else {
				if (File.exists(dir + stack + "Processed")) {
					batchTrack(dir, stack);
				} else {
					print(stack + " has not been processed yet!  Skipping...");
				}
			}
		}
		//Every 2 cycles close all windows
		if (i % 2 == 0) {
			run("Close All");
			run("Collect Garbage");
		}
	}

	print("Batch Operation Complete!");
}

function batchTrack(dir, stack)  {
	run("Open Video Rack", "choose=" + dir + stack);
	run("FlyTrack BatchTrackmate");
}

