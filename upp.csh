#!/usr/bin/tcsh -f

if ( $# >= 1 ) then
  set num = $1
else
  set num = 1
endif

set upStr = "./"
@ i = $num
while ($i > 0)
  set upStr = "../$upStr"
  @ i--
end
pushd $upStr

