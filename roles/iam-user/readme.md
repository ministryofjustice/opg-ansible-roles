To create IAMS users, pass a dictionary of users and a single group. Only a single group membership can be specified.

```
iam_user_users:
  - name: user1
    group: developer
  - name: user2
    group:
  - name: user3
    group: developer
```

A group will automatically add an inline policy when `iam_policy_[group name].json` of the same name is found in the files directory.

Secrets will be written to secrets.json in your playbook_dir or the value of `iam_user_secret_filepath`
