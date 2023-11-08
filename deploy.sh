#!/bin/sh
rm -r ./public/
hugo
rsync -rzp --chmod=Du=rwx,Dg=rwx,Do=rwx,Fu=rw,Fg=rw,Fo=rw -e ssh --progress --delete ./deploy/ lieschool:/opt/

rsync -rzp --chmod=Du=rwx,Dg=rwx,Do=rwx,Fu=rw,Fg=rw,Fo=rw -e ssh --progress --delete ./public/ lieschool:/srv/lie-school.ru/
