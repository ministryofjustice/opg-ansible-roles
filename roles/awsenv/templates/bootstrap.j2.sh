#!/bin/bash -ex
#let's log the output
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

function download()
{
    #try downloading a file for 5 mins
    local module_path=${1}
    local retry_count_down=30
    local base_url="https://raw.githubusercontent.com/ministryofjustice/opg-bootstrap/{{ bootstrap.bootstrap_branch }}"
    while ! wget --no-verbose --retry-connrefused --random-wait -O ${module_path} "${base_url}/${module_path}" && [ ${retry_count_down} -gt 0 ] ; do
        retry_count_down=$((retry_count_down - 1))
        sleep 10
    done
}

function module()
{
    local module_path=${1}
    if [ ! -e ${module_path} ]; then
        echo ${module_path}: Downloading
        mkdir -p modules
        download ${module_path}
    fi
    echo ${bmodule_path}: Loading
    source ${module_path}
}

readonly IS_SALTMASTER={{ bootstrap.is_saltmaster | default('no') }}
readonly HAS_DATA_STORAGE={{ bootstrap.has_data_storage | default('no') }}
readonly OPG_ROLE={{ bootstrap.opg_role }}
readonly OPG_STACKNAME={{ opg_data.stack }}
readonly OPG_PROJECT={{ opg_data.project }}

readonly OPG_ENVIRONMENT={{ opg_data.environment }}
readonly OPG_SHARED_SUFFIX={{ opg_data.stack }}
readonly OPG_DOMAIN={{ opg_data.domain }}

module modules/00-start.sh
module modules/10-volumes.sh
module modules/20-docker.sh
module modules/90-salt.sh
module modules/99-end.sh
