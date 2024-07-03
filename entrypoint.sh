#!/usr/bin/env sh

set -e
echo "run docker-entrypoint"
case "$1" in
    bot)
        exec python starter.py
        ;;
    web_admin)
        echo "run web_admin"
        exec python web_admin.py
        ;;
    *)  
        echo "run other command"
        exec "$@"
        ;;
esac