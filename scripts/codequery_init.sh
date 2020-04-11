#!/bin/bash

# Parse Parameters #
for ARG in $*; do
  case $ARG in
    -d=*|--dir=*)
      project_dir=${ARG#*=}
      ;;
    *)
      echo "Usage c_codequery_init.sh [-d=/path/to/project/|--dir=/path/to/project/]"
      echo "project_dir: $project_dir"
  esac
done

project_name="$(basename $(pwd))"

cd $project_dir

find . -iname "*.c"    > ./cscope.files
find . -iname "*.cpp" >> ./cscope.files
find . -iname "*.cxx" >> ./cscope.files
find . -iname "*.cc " >> ./cscope.files
find . -iname "*.h"   >> ./cscope.files
find . -iname "*.hpp" >> ./cscope.files
find . -iname "*.hxx" >> ./cscope.files
find . -iname "*.hh " >> ./cscope.files

cscope -cb
ctags --fields=+i -n -R -L ./cscope.files
cqmakedb -s "./$project_name.db" -c "./cscope.out" -t "./tags" -p

cd -
