# Javascript LangPack

How to make a new algorithm:
docker run --rm -it -v `pwd`:/tmp/build algorithmia/langbuilder-javascript

How to run that algorithm:
docker run --rm -it -v `pwd`/algorithm.zip:/tmp/algorithm.zip -p 9999:9999 algorithmia/langserver-javascript

And to get output from the algorithm run
curl -s localhost:9999 -X POST -H 'Content-Type: text/plain' -d '<INPUT>'