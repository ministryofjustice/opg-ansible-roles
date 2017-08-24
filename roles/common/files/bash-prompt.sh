#!/bin/bash
STACK=$(echo "${OPG_STACKNAME}"| tr -d '[:digit:]')

if [[ "${STACK}" =~ ^production ]]
then
  PS1="\[\033[01;31m\](${OPG_STACK}) \u@${OPG_ROLE}[\033[01;31m\]"
else
  PS1="\[\033[01;34m\](${OPG_STACK}) \u@${OPG_ROLE}[\033[01;34m\]"
fi

PS1="${PS1}\[\[32;1m\](${OPG_ROLE}\[\[0m\]][\[\[33;1m\]\u@\h\[\e[0m\]][\[\e[0;33m\]\w\[\e[0m\]]: "
