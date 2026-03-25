#!/bin/sh
set -e

doas sh -c 'grep -q "^/home/user/packages/projects" /etc/apk/repositories || echo "/home/user/packages/projects" >> /etc/apk/repositories'
doas apk update
doas apk add jaraco-starter
