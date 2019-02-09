#!/bin/tcsh -f

set text = $cwd
if ($# >= 1) then
  set text = "$1"
endif
echo -n "]2;${text} "
