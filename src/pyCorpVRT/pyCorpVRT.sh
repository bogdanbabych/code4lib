# python pyCorpVRT.py "LKeyColumns.extend([2,1])" "LValueColumns.extend([1])" < pyCorpVRT_in.txt > pyCorpVRT_out.txt
# python pyCorpVRT.py "LKeyColumns.extend([2,1])" "LValueColumns.extend([1])" < pyCorpVRT_in.txt > pyCorpVRT_out.txt

# python pyCorpVRT.py "LKeyColumns.extend([0])" "LValueColumns.extend([2,1])" "LFlags.extend(['fileVRT2dict','dict2dstr'])" < pyCorpVRT_in_BNC1994-10k.vrt > pyCorpVRT_out_BNC1994-10k.txt
# python pyCorpVRT.py "LKeyColumns.extend([0])" "LValueColumns.extend([2,1])" "LFlags.extend(['fileVRT2dict','dict2dstr'])" < pyCorpVRT_in_canada2018.vrt > pyCorpVRT_out_canada2018.txt


# python pyCorpVRT.py "LKeyColumns.extend([2,1])" "LValueColumns.extend([1])" "LIndexColumns.extend([2,1])" "LFlags.extend(['fileVRT2posTemplates','templates2dtoponly'])" < pyCorpVRT_in_BNC1994-10k.vrt > pyCorpVRT_out_BNC1994-10k.txt
# python pyCorpVRT.py "LKeyColumns.extend([2,1])" "LValueColumns.extend([1])" "LIndexColumns.extend([2,1])" "LFlags.extend(['fileVRT2posTemplates','templates2dtoponly'])" < pyCorpVRT_in_canada2018.vrt > pyCorpVRT_out_canada2018.txt

# python pyCorpVRT.py "LKeyColumns.extend([0])" "LValueColumns.extend([1])" "LIndexColumns.extend([2,1])" "LFlags.extend(['fileVRT2posTemplates','templates2dtoponly'])" < pyCorpVRT_in_BNC1994-10k.vrt > pyCorpVRT_out_BNC1994-10k.txt
# python pyCorpVRT.py "LKeyColumns.extend([0])" "LValueColumns.extend([1])" "LIndexColumns.extend([2,1])" "LFlags.extend(['fileVRT2posTemplates','templates2dtoponly'])" < pyCorpVRT_in_canada2018.vrt > pyCorpVRT_out_canada2018.txt


# python pyCorpVRT.py "LKeyColumns.extend([0])" "LValueColumns.extend([1])" "LIndexColumns.extend([2,1])" "LFlags.extend(['fileVRT2posTemplates','templates2dtoponly'])" < pyCorpVRT_in_bnc1994-1mw.vrt > pyCorpVRT_out_bnc1994-1mw.tsv
python pyCorpVRT.py "LKeyColumns.extend([0])" "LValueColumns.extend([1])" "LIndexColumns.extend([2,1])" "LFlags.extend(['fileVRT2posTemplates','templates2dtoponly'])" < pyCorpVRT_in_canada2018.vrt > pyCorpVRT_out_canada2018.tsv
python pyCorpVRT.py "LKeyColumns.extend([0])" "LValueColumns.extend([1])" "LIndexColumns.extend([2,1])" "LFlags.extend(['fileVRT2posTemplates','templates2dtoponly'])" < pyCorpVRT_in_bnc1994.vrt > pyCorpVRT_out_bnc1994.tsv
