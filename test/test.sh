for file in $( find . -type f -name '*_test.py' );
  do 
    echo "Running test $file" 
    dir=$(dirname "$file")
    if [ $dir == "." ]; then 
      export PYTHONPATH="../reqable"
      python3 $file
    else
      cd $dir
      export PYTHONPATH="../../reqable"
      python3 $(basename "$file")
      cd ..
    fi;
  done
