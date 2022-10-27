#!/bin/tcsh -f
# According to git documentation, script needs to have:
# GIT_EXTERNAL_DIFF is
#           called with 7 parameters:
#               path old-file old-hex old-mode new-file new-hex new-mode

set pathIn=$1
shift
set oldFileIn=$1
shift
set oldHexIn=$1
shift
set oldModeIn=$1
shift
set newFileIn=$1
shift
set newHexIn=$1
shift
set newModeIn=$1
shift

echo "Path: $pathIn"
echo "oldFile: $oldFileIn"
echo "newFile: $newFileIn"
#cd $pathIn
if ($oldFileIn != "/dev/null" && $newFileIn != "/dev/null") then
    gvim -d --nofork $newFileIn $oldFileIn
endif
