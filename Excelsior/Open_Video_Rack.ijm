//Open a stack in a directory and preconfigure the properties for tracking

path = getDirectory("Choose a Directory");

if (path == "") {
exit()
}

dir = File.getParent(path) + "/";
stack = File.getName(path) + "/";

print(path);
print(stack);
print(dir);

getMedian(dir, stack);
processStack(dir, stack);

function getMedian(dir, stack)  {
	fileList = getFileList(dir + stack);
	medianFound = false;
	i = 0;
	while (!medianFound) {
		if (i < fileList.length) {
			if (startsWith(fileList[i], "Median_") && !medianFound) {
				print("Opening median: " + fileList[i]);
				processMedian(dir, stack, fileList[i]);
				medianFound = true;
			}
			else {
				i++;
			}
		} else {
			print("Cannot find median for " + stack + " !");
			medianFound = true;
		}
	}
}

function processStack(dir, stack) {
	print("Path: " + dir + stack);
	run("Image Sequence...", "open=[" + dir + stack + "Processed] sort");
	stackName = substring(stack, 0, lastIndexOf(stack,"/"));
	run("Properties...", "channels=1 slices=1 frames="+ nSlices + " unit=cm pixel_width=.0282 pixel_height=.0282 voxel_depth=1.0000 frame=[.133333 sec]");
}

function processMedian(dir, stack, file) {
	print("Path: " + dir + stack + file);
	open(dir + stack + file);
}
