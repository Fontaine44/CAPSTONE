
# TO BE UPDATED

## Commands

must do that first:

CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE;


Empty database:

MATCH (n) DETACH DELETE n;


Reset keys and constraints:

CALL apoc.schema.assert({},{},true) YIELD label, key RETURN *


Remove Ressource label constraint:

MATCH (n:Resource) REMOVE n:Resource;
