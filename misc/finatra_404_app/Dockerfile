FROM openjdk:8-alpine

RUN apk add --update bash curl

ENV SBT_VERSION 0.13.17
ENV SBT_HOME /usr/local/sbt
ENV PATH ${PATH}:${SBT_HOME}/bin

RUN curl -L "https://github.com/sbt/sbt/releases/download/v${SBT_VERSION}/sbt-${SBT_VERSION}.tgz" | gunzip | tar -x -C /usr/local

VOLUME /code
WORKDIR /code

EXPOSE 8888

RUN sbt compile

ENTRYPOINT ["sbt", "~run"]
