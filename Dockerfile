FROM ubuntu:bionic

WORKDIR "/flag_submitter"
COPY . .

RUN groupadd -r mongodb \
 && useradd -r -g mongodb mongodb \
 && rm -vr /flag_submitter/db

RUN apt update \
 && apt -y install ca-certificates gnupg curl \
 && curl "https://www.mongodb.org/static/pgp/server-4.4.asc" | apt-key add - \
 && echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list \
 && apt update \
 && apt -y install python3 python3-pip mongodb \
 && echo 'Finished installing dependencies' \
 && pip3 install -r requirements.txt

RUN mkdir -p /data/db /data/configdb \
	&& chown -R mongodb:mongodb /data/db /data/configdb

VOLUME ./db /data/db
VOLUME ./configdb /data/configdb

#RUN gitlab-ctl reconfigure


EXPOSE 8000
EXPOSE 8080

#USER node

CMD ["docker-entrypoint.sh"]
