#!/bin/tcsh -f
# Purpose: grep for patterns (using cg) and then prompted for match to edit. Currently hardcoded to be gvim editor.
# Usage: cge [grep options] <pattern>
#
set toolsDir = `which $0`
set toolsDir = $toolsDir:h

$toolsDir/cg "$*" | awk '{print NR, " : ", $0}'
echo -n 'Select a line number to edit (blank to skip): '
set recordNumber = $<
if ($recordNumber != '') then
  set vimArgs = `$toolsDir/cg "$*" | awk -v nr=$recordNumber 'BEGIN{FS=":"}{if (NR==nr) printf("%s +%d", $1,$2)}'`
  echo "vimArgs: $vimArgs"
  if ("$vimArgs" != '') then
    gvim $vimArgs >& /dev/null
  endif
endif
