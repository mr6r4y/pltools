#!/bin/bash

# Parse Parameters #
for ARG in $*; do
  case $ARG in
    -d=*|--dir=*)
      java_src_dir=${ARG#*=}
      ;;
    *)
      echo "Usage list_methods.sh [-d=/path/to/java/srcs/dir/|--java-src-dir=/path/to/java/srcs/dir/]"
      echo "java_src_dir: $java_src_dir"
  esac
done



for i in $( ls "$java_src_dir" ); do 
    java_methods.py -f dot -j $java_src_dir/$i; 
    echo;
done