SHELL := /usr/bin/env bash

# http://stackoverflow.com/a/16844327
normal := \033[0m
green := \033[0;32m

on_aws := $(shell curl --retry 0 -m 1 http://169.254.169.254/latest/meta-data/mac >/dev/null 2>&1 && echo yes )
eth0mac := $(shell test -z "${on_aws}" || curl --retry 0 -m 1 http://169.254.169.254/latest/meta-data/mac 2>/dev/null)
jenkins_vpc_id := $(shell test -z "${on_aws}" || curl --retry 0 -m 1 http://169.254.169.254/latest/meta-data/network/interfaces/macs/$(eth0mac)/vpc-id 2>/dev/null)
jenkins_subnet_id := $(shell test -z "${on_aws}" || curl --retry 0 -m 1 http://169.254.169.254/latest/meta-data/network/interfaces/macs/$(eth0mac)/subnet-id 2>/dev/null)
jenkins_ami_serial := $(shell date +'%s')
jenkins_pubkey_filename := $(shell echo $(PWD)/id_rsa.pub)
jenkins_aws_region := $(shell test -z "${on_aws}" || curl --retry 0 -m 1 -s http://169.254.169.254/latest/dynamic/instance-identity/document 2>/dev/null | \
	python -c "import json,sys; print json.loads(sys.stdin.read())['region']" 2>/dev/null)
jenkins_ubuntu1404_base_ami := $(shell test -z "${on_aws}" || curl --retry 0 -m 1 -s  "https://cloud-images.ubuntu.com/locator/ec2/releasesTable?_=`date +%s`" 2>/dev/null | \
	grep $(jenkins_aws_region) 2>/dev/null | \
	grep trusty 2>/dev/null | \
	grep 'hvm:ebs-ssd' 2>/dev/null | \
	cut -f 7 -d ","  2>/dev/null | \
	cut -f 2 -d ">" 2>/dev/null | \
	cut -f 1 -d "<" 2>/dev/null )
jenkins_ubuntu1604_base_ami := $(shell test -z "${on_aws}" || curl --retry 0 -m 1 -s  "https://cloud-images.ubuntu.com/locator/ec2/releasesTable?_=`date +%s`" 2>/dev/null | \
	grep $(jenkins_aws_region) 2>/dev/null | \
	grep xenial  2>/dev/null | \
	grep 'hvm:ebs-ssd' 2>/dev/null | \
	cut -f 7 -d "," 2>/dev/null | \
	cut -f 2 -d ">"  2>/dev/null | \
	cut -f 1 -d "<" 2>/dev/null )

check_vars:
	echo; echo -e "$(green)Checking required variables... $(normal)"; echo
	 if [ ! -n "$$KEY_NAME" ]; then echo "KEY_NAME is not set"; exit 1; fi
	 if [ ! -n "$$VPC_ID" ]; then echo "VPC_ID is not set"; exit 1; fi
	 if [ ! -n "$$VPC_SUBNET_ID" ]; then echo "VPC_SUBNET_ID is not set"; exit 1; fi
	 if [ ! -n "$$AMI_SERIAL" ]; then echo "AMI_SERIAL is not set"; exit 1; fi
	 if [ ! -n "$$PUBKEY_FILENAME" ]; then echo "PUBKEY_FILENAME is not set"; exit 1; fi


test: check_vars roles ssh_pub_key venv lint
	echo; echo -e "$(green)Running make test... $(normal)"; echo
	ansible-playbook -i ansible/ec2.py \
		-e KEY_NAME=$$KEY_NAME \
		-e VPC_ID=$$VPC_ID \
		-e VPC_SUBNET_ID=$$VPC_SUBNET_ID \
		-e AMI_SERIAL=$$AMI_SERIAL \
		-e PUBKEY_FILENAME=$$PUBKEY_FILENAME \
		$$EXTRA_ANSIBLE_OPTIONS site.yml

roles:
	echo; echo -e "$(green)Prepare our WORKSPACE to consume our role $(normal)"; echo
	mkdir -p roles
	rm -f roles/opg-ansible-ec2-ami-base
	ln -s .. roles/opg-ansible-ec2-ami-base

ssh_pub_key:
	echo; echo -e "$(green)generate our public.key from our existing private key in this slave $(normal)"; echo
	ssh-keygen -y -f ~/.ssh/id_rsa |tee id_rsa.pub

venv:
	echo; echo -e "$(green)set our virtualenv $(normal)"; echo
	virtualenv venv
	venv/bin/pip install -q --upgrade -r requirements.txt

lint: roles venv
	echo; echo -e "$(green)lint all the things $(normal)"; echo
	source venv/bin/activate && ansible-lint --force-color site.yml

make jenkins: roles ssh_pub_key venv lint
	echo; echo -e "$(green)running ansible... $(normal)"; echo
	# Make sure we consume the local public key
	# then use timestamp as our serial id
	# and grab our VPC and other bobs from our own VM
	# we assume our AMI will be available across AWS accounts...
	bash -c "export AWS_REGION=$(jenkins_aws_region) && \
		export ANSIBLE_FORCE_COLOR=true && \
		source venv/bin/activate &&  \
		ansible-playbook -i ansible/ec2.py \
			-e KEY_NAME="bake-ami-keypair" \
			-e VPC_ID=$(jenkins_vpc_id) \
			-e VPC_SUBNET_ID=$(jenkins_subnet_id) \
			-e AMI_SERIAL=$(jenkins_ami_serial) \
			-e PUBKEY_FILENAME=$(jenkins_pubkey_filename) \
			-e UBUNTU_1404_BASE_AMI=$(jenkins_ubuntu1404_base_ami) \
			-e UBUNTU_1604_BASE_AMI=$(jenkins_ubuntu1604_base_ami) \
			$$EXTRA_ANSIBLE_OPTIONS site.yml "