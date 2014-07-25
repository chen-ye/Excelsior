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
if (!processTiffStack(dir, stack)) {
	processSequenceStact(dir, stack);
}

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

function processTiffStack(dir, stack)  {
	fileList = getFileList(dir + stack);
	stackFound = false;
	i = 0;
	while (!stackFound) {
		if (i < fileList.length) {
			if (startsWith(fileList[i], "Preprocessed_") && !stackFound) {
				print("Opening tiff stack: " + fileList[i]);
				open(dir + stack + filelist[i]);
				processStack(dir, stack);
				stackFound = true;
				return true;
			}
			else {
				i++;
			}
		} else {
			print("Cannot find tiff for " + stack + ", searching for sequence stack");
			stackFound = true;
			return false;
		}
	}
}

function processSequenceStact(dir, stack) {
	print("Path: " + dir + stack);
	stackName = substring(stack, 0, lastIndexOf(stack,"/"));
	run("Image Sequence...", "open=[" + dir + stack + "Processed] sort");
	selectWindow("Processed");
	saveAs("Tiff", dir + stack + "Preprocessed_" + stackName);
	processStack(dir, stack);
}

function processStack(dir, stack) {
	stackName = substring(stack, 0, lastIndexOf(stack,"/"));
	selectWindow("Preprocessed_" + stackName + ".tif");
	run("Properties...", "channels=1 slices=1 frames="+ nSlices + " unit=cm pixel_width=.0282 pixel_height=.0282 voxel_depth=1.0000 frame=[.133333 sec]");
}

function processMedian(dir, stack, file) {
	print("Path: " + dir + stack + file);
	open(dir + stack + file);
}
