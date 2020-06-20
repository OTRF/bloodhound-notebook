# Author: Roberto Rodriguez (@Cyb3rWard0g)
# License: GPL-3.0

FROM cyb3rward0g/jupyter-base:0.0.5
LABEL maintainer="Roberto Rodriguez @Cyb3rWard0g"
LABEL description="BloodHound Notebook Project."

ENV DEBIAN_FRONTEND noninteractive \
  NEO4J_VERSION 4.0.6 \
  NEO4J_TARBALL neo4j-community-${NEO4J_VERSION}-unix.tar.gz \
  NEO4J_HOME /var/lib/neo4j \
  NEO4J_URI http://dist.neo4j.org/${NEO4J_TARBALL}

USER root

RUN apt-get update --fix-missing && apt-get install -y --no-install-recommends openjdk-11-jdk \
  && curl --fail --silent --show-error --location --remote-name ${NEO4J_URI} \
  && tar --extract --file ${NEO4J_TARBALL} --directory /var/lib \
  && mv /var/lib/neo4j-* "${NEO4J_HOME}" \
  && rm ${NEO4J_TARBALL} \
  && mv "${NEO4J_HOME}"/data /data \
  && mv "${NEO4J_HOME}"/logs /logs \
  && chown -R ${USER}:${USER} /data \
  && chmod -R 777 /data \
  && chown -R ${USER}:${USER} /logs \
  && chmod -R 777 /logs \
  && chown -R ${USER}:${USER} "${NEO4J_HOME}" \
  && chmod -R 777 "${NEO4J_HOME}" \
  && ln -s /data "${NEO4J_HOME}"/data \
  && ln -s /logs "${NEO4J_HOME}"/logs \
  && rm -rf /tmp/* \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get -y purge --auto-remove curl \
  && apt-get -qy clean autoremove

USER ${USER}

RUN python3 -m pip install --upgrade pip \
  && python3 -m pip install py2neo==4.3.0 plotly==4.3.0 altair==3.2.0 ipywidgets==7.5.1

ENV PATH ${NEO4J_HOME}/bin:$PATH

COPY scripts/docker-entrypoint.sh /opt/docker-entrypoint.sh

EXPOSE 7474 7473 7687

ENTRYPOINT ["/opt/docker-entrypoint.sh"]
