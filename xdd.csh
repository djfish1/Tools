#!/bin/tcsh -f
#Usage: xdd <dir0> <dir1> [--maxdepth <maxdepth>] [--quiet|-q] <diff flags>

set dir0 = "$1"
shift
set dir1 = "$1"
shift
set diffArgs = ""
set maxdepth = 1
@ quiet = 0
while ($# > 0)
  if ("--maxdepth" == "$1") then
    shift
    set maxdepth=$1
  else if ("--quiet" == "$1" || "-q" == "$1") then
    @ quiet = 1
  else
    set diffArgs = "$diffArgs $1"
  endif
  shift
end

set ff = ( ` find $dir0 -maxdepth $maxdepth -type f -printf '%P\n' ` )
set -f ff = ( $ff ` find $dir1 -maxdepth $maxdepth -type f -printf '%P\n' ` )

# Note: quotes are needed around stat, otherwise ? gets intepreted weirdly.
set tmpFile = `mktemp`
foreach f ($ff)
  if ( -f "$dir0/$f" ) then
    if ( -f "$dir1/$f" ) then
      # We only care if there are differences, so always pass the -q flag
      diff -q $diffArgs "$dir0/$f" "$dir1/$f" >& /dev/null
      set diffStat = $?
      if ($diffStat == 0) then
        if (! $quiet) then
          echo "IDENTICAL: $dir0/$f and $dir1/$f are the same"
        endif
      else if ($diffStat == 1) then
        echo "DIFFER: $dir0/$f and $dir1/$f are different"
        gvim --nofork -d "$dir0/$f" "$dir1/$f" >& /dev/null
      else
        echo "PROBLEM: couldn't compare $dir0/$f and $dir1/$f"
      endif
    else
      echo "MISSING: $dir1/$f does not exist"
    endif
  else
    echo "MISSING: $dir0/$f does not exist"
  endif
end
rm $tmpFile
