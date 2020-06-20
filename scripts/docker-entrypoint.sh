#!/bin/bash
set -eux

#${NEO4J_HOME}/bin/neo4j-admin set-initial-password neo4jbinder
${NEO4J_HOME}/bin/bin/neo4j start

exec "$@"