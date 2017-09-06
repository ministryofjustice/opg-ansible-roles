### Admins Role

Add/Remove admin users from the system

####Meta-Data
```yaml
admins:
  - name: foo
    auth_keys:
    - enc: id-rsa
      key: 1232131313121asdasdasskkkk
      comment: home pc
    - enc: id-rsa
      key: 12312312klkasdasdassdasd333
      comment: work pc
    use_vim_editing: yes #Optional to default to vim
  - name: bar
    absent: yes
```