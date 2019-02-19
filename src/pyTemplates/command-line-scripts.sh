# add extension recursively
find . -type f -exec mv '{}' '{}'.jpg \;


# recursive download with Curl
curl --remote-name-all https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2621{/PDT3.5.tgz}

# rsync 
rsync -avz rpmpkgs/ root@192.168.0.101:/home/
rsync -avh smlbb@corpus:/data/bogdan/corpus/medical/nohup.out .
rsync -avh ./PDT3.5-xml.zip smlbb@corpus:/data/bogdan/corpus/prague-dependencies


