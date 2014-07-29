#/bin/bash

export x=0
export TEST=false

while getopts ":n" opt; do
    case $opt in
        n)
          TEST=true
          echo "Test run!"
          ;;
        \?)
          echo "Invalid option: -$OPTARG" >&2
          ;;
    esac
done

find . | while read -r file
do
    # replace colon with dash
    # remove exclamation points and commas
    newfile=$(echo "$file" | sed 's/:/-/g; s/[!,]//g')
    if [ "$file" != "$newfile" ]; then
        echo `basename $file` "renamed to" `basename $newfile`
        if [ "$TEST" = false ]; then
            mv "$file" "$newfile"
        fi
        ((x++))
    fi
done

echo "$x files renamed"
unset x
unset TEST
