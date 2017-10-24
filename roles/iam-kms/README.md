#iam-kms

Simple role to create/update master keys and relevant aliases.

####Example meta-data and output
```yaml
opg_data:
  project: foo
  environment: bar
  
kms_data:
  - key_description: baz
  - key_description: bazbar
```

The above meta-data will create two kms managed masters keys

```yaml
output:
  - key_description: 'foo-bar-<datetime>-baz'
    key_alias: 'foo-bar-baz'
  - key_description: 'foo-bar-<datetime>-bazbar'
    key_alias: 'foo-bar-bazbar'   
```
