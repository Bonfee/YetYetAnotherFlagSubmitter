#! /bin/sh

[ 'run' == "$1" ] && docker run -it --rm -p 8000:8000 -p 8080:8080 -t flag_submitter /bin/bash && exit

TAG='flag_submitter'

[ ! -d ./db ] && mkdir -v db
[ ! -d ./configdb ] && mkdir -v configdb

docker build . -t "$TAG" --force-rm

[ -z "$(docker images -f "dangling=true" -q)" ] && docker rmi $(docker images -f "dangling=true" -q)

[ 'interactive' == "$1" ] && docker run -it --rm -p 127.0.0.1:8000:8000 -p 127.0.0.1:8080:8080 -t flag_submitter /bin/bash
