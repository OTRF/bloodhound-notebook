#!/bin/bash
set -e

# ********* Setting Logstash PIPELINE_WORKERS ***************
if [[ -z "$NEO4J_ADMIN_PWD" ]]; then
    NEO4J_ADMIN_PWD=wardog
fi
${NEO4J_HOME}/bin/neo4j-admin set-initial-password $NEO4J_ADMIN_PWD 2>/dev/null || true
${NEO4J_HOME}/bin/neo4j start

exec "$@"