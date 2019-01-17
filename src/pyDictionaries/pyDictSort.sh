# arguments: argv[1]=input file; argv[2]=VRT fields which will become keys; argv[3]=VRT fields which will become values (this list is obligatory, but can be empty)
python pyDictSort.py "LKeyColumns.extend([0])" "LValueColumns.extend([2,1])" < pyDictSort_in.txt > pyDictSort_out.txt
