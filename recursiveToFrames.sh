#/bin/bash
# Script to convert .h264 files specified in METADIR into tiff frames
METADIR="images/"
module load 'graphicsmagick'
module load 'ffmpeg/1.2'

PARALLEL=true
TEST=false

# while getopts ":n:s" opt; do
#     case $opt in
#         n)
#           TEST=true
#           echo "Test run!"
#           ;;
#         s)
#           PARALLEL=false
#           echo "Disabling parallelization"
#         \?)
#           echo "Invalid option: -$OPTARG" >&2
#           ;;
#     esac
# done

#Parallelizable function to convert .h264 file into tiff frames
convertToTiff() {
  #path to video file
  video=$1
  echo 'Now in directory: '$video
	#directory in which $video is contained
  DIR=`dirname $video`

  echo 'Outputting frames to: '$DIR'/png'
  if [ !$TEST ]; then
	   mkdir $DIR'/png'
     ffmpeg -probesize 10M -i $video $DIR/png/img_%03d.png
	    echo 'Converting frames to tiff'
      gm mogrify -output-directory $DIR -format tiff $DIR/png/*.png
  fi
}

#find all the .h264 files in $METADIR and then run convertToTiff() on them
for video in $(find $METADIR -name '*.h264')
do
	if [ $PARALLEL ]; then
    convertToTiff $video &
  else
    convertToTiff $video
  fi
done

wait

echo "Everything's converted!"
