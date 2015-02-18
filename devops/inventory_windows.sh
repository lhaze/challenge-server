#!/bin/bash
cat <<EOF
{
  "web": ["localhost"],
  "redis": ["localhost"],
  "postgres": ["localhost"],

  "_meta" : {
    "hostvars" : {
      "localhost" : {
        "ansible_connection": "local"
      }
    }
  }
}
EOF
