# gitlab_varedit
Edit gitlab project variables in your $EDITOR!

## Install
`
pip install git+https://github.com/trnila/gitlab_varedit
`

## Configuration
Create configuration in *~/.python-gitlab.cfg*:
```
[global]
default = work                                                                                                                                                                                                                                                                                                                 
ssl_verify = false

[dev]
url = http://gitlab-url/
private_token = my-private token
```

## Run
`gitlab_varedit project/repository`

When you save and quit your editor, changes are sent to Gitlab.