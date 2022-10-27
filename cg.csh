#!/bin/tcsh -f
# Purpose: convenient shortcut for recursively searching for a pattern in useful files.
# Usage: cg [grep options] <pattern>

# Always print out the line numbers
set opts = ( '-n' )
# Gather up all but the last argument as options to grep
while ($# > 1)
  set -l opts = ( $opts $1 )
  shift
end

# Allow the user to include wildcards in pattern by turning off glob
set noglob
set pattern = "$1"
#echo "options: $opts"
#echo "pattern: $pattern"

grep $opts -R "$pattern" \
    --exclude=*.pyc --exclude=*.dll --exclude=*.exe --exclude=*.class \
    --exclude tags --exclude *.swp --exclude-dir .git --exclude *.vcxproj #| \
        #awk 'BEGIN{FS=":"; OFS=":"}{printf("%s +%s : ", $1, $2); for (i=3; i<NF; ++i){printf("%s:", $i)} printf("%s\n", $NF)}'
unset noglob

