parse-docker-files
==================

Simple role to parse Dockerfile.tmpl files into Dockerfiles, currently used to set tags 
in the `FROM` portion of the Dockerfile


####Example

Assuming you have the roles checked out into your projects `playbook_directory` under `opg-ansible`
and have a playbook similar to the following

```yaml
hosts: localhost
  pre_tasks:
    - name: Setup branch vars
      set_fact:
        docker_image_base: "{{ tag_number | default('latest') }}"
  roles:
    - { role: "parse-docker-files" }
```

```bash
 $ cd ansible
 $ ansible-playbook -i hosts playbook.yml -e tag_number=semvertag 
```