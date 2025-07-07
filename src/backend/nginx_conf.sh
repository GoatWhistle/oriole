#!/bin/sh

if [ "$IS_DEV" = "true" ]; then
  echo "Using dev nginx config"
  cp /etc/nginx/nginx.dev.conf /etc/nginx/conf.d/default.conf
else
  echo "Using prod nginx config"
  cp /etc/nginx/nginx.prod.conf /etc/nginx/conf.d/default.conf
fi

exec "$@"
