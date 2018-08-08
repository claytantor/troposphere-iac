# troposphere-iac
a basic pattern for doing IAC with troposphere

## installing requirements
`pip install -r requirements.txt`

# display stack


# create stack
Create a stack with from a template sent by stdin.

The help:
```
$ python create-stack.py -h
usage: create-stack.py [-h] --name NAME --params PARAMS
    [--log LOG] [--tags TAGS]
    [--config CONFIG]

arguments:
  -h, --help            show this help message and exit
  --name NAME           the name of the stack to create.
                        the url where the stack template can be fetched.
  --params PARAMS       the key value pairs for the parameters of the stack.
  --log LOG             which log level. DEBUG, INFO, WARNING, CRITICAL
  --tags TAGS           the tags to attach to the stack.
```


# delete stack
Delete an existing stack. Includes a simple parser to allow retained resources to be excluded as comma separated string.

The help:
```
python delete-stack.py -h
usage: delete-stack.py [-h] --name NAME [--retain RETAIN] [--log LOG]
                       [--config CONFIG]
arguments:
  -h, --help       show this help message and exit
  --name NAME      the name of the stack to create.
  --retain RETAIN  the names (comma separated) of the resources to retain.
  --log LOG        which log level. DEBUG, INFO, WARNING, CRITICAL
  --config CONFIG  the config file used for the application
```

And an example:

```
python delete-stack.py --name ec2-basic-01
INFO       2018-08-07 20:56:47,714 make_cloudformation_client           50  : using default config.
INFO       2018-08-07 20:56:47,736 load                                 1032: Found credentials in shared credentials file: ~/.aws/credentials
INFO       2018-08-07 20:56:47,924 _new_conn                            735 : Starting new HTTPS connection (1): cloudformation.us-west-2.amazonaws.com
INFO       2018-08-07 20:56:48,192 main                                 56  : succeed. response: {"ResponseMetadata": {"RetryAttempts": 0, "HTTPStatusCode": 200, "RequestId": "12e52bdc-9abf-11e8-a969-95f0c7d8d06d", "HTTPHeaders": {"x-amzn-requestid": "12e52bdc-9abf-11e8-a969-95f0c7d8d06d", "date": "Wed, 08 Aug 2018 03:56:47 GMT", "content-length": "212", "content-type": "text/xml"}}}
```

# using a custom configuration file
I don’t pass configurations on the CLI, to me the args on the CLI are about runtime not config. We have a config file that has the static configs in it:

```
AWS_ACCESS_KEY_ID=[my_access_key]
AWS_SECRET_ACCESS_KEY=[my_secret_access]
AWS_REGION_NAME="us-west-2"
LOG_LEVEL="INFO"
```

Boto3 is capable of auto configuration, and it will behave like aws CLI and attempt to find configs from ~/.aws/credentials but if you want explicit configs that is available using the config option in the CLI. If you do this the debug level will default to INFO.

# gen template
`python gen-template.py --name apache --config dev`

# running a stack build
Currently building a stack is a combination of creating the template and sending the output of the template to stdio.

```
python gen-template.py --name apache --config dev | python create-stack.py --name ec2-basic-01 --params "KeyName=dronze-oregon-dev" --tags "notes=newstack01&info=made%20with%20love"
INFO       2018-08-07 20:52:04,770 make_cloudformation_client           50  : using default config.
INFO       2018-08-07 20:52:04,780 load                                 1032: Found credentials in shared credentials file: ~/.aws/credentials
INFO       2018-08-07 20:52:04,904 _new_conn                            735 : Starting new HTTPS connection (1): cloudformation.us-west-2.amazonaws.com
INFO       2018-08-07 20:52:05,097 main                                 109 : succeed. response: {"StackId": "arn:aws:cloudformation:us-west-2:705212546939:stack/ec2-basic-01/5bc91a50-9abe-11e8-9f7c-0a44a01d32f4", "ResponseMetadata": {"RetryAttempts": 0, "HTTPStatusCode": 200, "RequestId": "6a25b5fb-9abe-11e8-b4ee-0fe61e08b3ca", "HTTPHeaders": {"x-amzn-requestid": "6a25b5fb-9abe-11e8-b4ee-0fe61e08b3ca", "date": "Wed, 08 Aug 2018 03:52:04 GMT", "content-length": "382", "content-type": "text/xml"}}}
```
