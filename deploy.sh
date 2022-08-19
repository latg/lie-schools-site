#!/bin/sh
rm -r ./public/
hugo
rsync -rz -e ssh --progress --delete ./public/ fkn:/srv/lie-school.ru/