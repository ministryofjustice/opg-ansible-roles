#!/bin/bash

if [[ "${OPG_ENVIRONMENT}" =~ "production" ]]
then
    PS1="\[\033[01;31m\](${OPG_ENVIRONMENT}-${OPG_STACKNAME})\[\e[m\]\[\033[01;32m\]$PS1\[\033[00m\] "
else
    PS1="\[\e[34;40m\](${OPG_ENVIRONMENT}-${OPG_STACKNAME})\[\e[m\]\[\e[36;40m\]$PS1\\[\e[m\] "
fi
