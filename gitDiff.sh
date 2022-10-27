#!/bin/bash
# According to git documentation, script needs to have:
# GIT_EXTERNAL_DIFF is
#           called with 7 parameters:
#               path old-file old-hex old-mode new-file new-hex new-mode

pathIn=$1
shift
oldFileIn=$1
shift
oldHexIn=$1
shift
oldModeIn=$1
shift
newFileIn=$1
shift
newHexIn=$1
shift
newModeIn=$1
shift

#echo "Path: $pathIn"
#echo "oldFile: $oldFileIn"
#echo "newFile: $newFileIn"
#cd $pathIn
if [[ $oldFileIn != "/dev/null" && $newFileIn != "/dev/null" ]]; then
    gvim -d --nofork $newFileIn $oldFileIn
fi
