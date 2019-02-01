# elastalert-lambda

Lambda handler for running [elastalert](https://github.com/Yelp/elastalert) serverless.


## Usage

* Clone this repository and jump into it:

```
$ git clone https://github.com/beezz/elastalert-lambda.git && cd elastalert-lambda
```

* Update configuration in `config.yaml`

* Put your rules into `rules` directory (remove example rules)

* Build deployment package `dist/lambda.zip` using command:

```
$ make lambda
```

* Deploy to AWS and schedule
  * Deployment package / code `dist/lambda.zip`
  * Handler name `elastalert_lambda.handler`
  * Runtime Python 2.7
  * Timeout and memory depends on the amount of data in your rules queries as on complexity of the queries
  * Schedule and event to trigger the function (as defined in configuration `run_every`)


## How it works

Lambda handler for elastalert works by executing the main entry point of
elastalert with predefined arguments

* `--config` pointing to `config.yaml`
* `--end` set to current timestamp (`datetime.datetime.utcnow()`)

You can override those defaults and also add additional arguments using
environmental variable `ARGS` or as part of sent event, also with `ARGS` key.

Automatic creation of indexes and mappings (``elastalert-create-index``) add
``EA_CREATE_INDEX`` environmental variable to the lambda function. You can
control the argument supplied to the index creation using the
``EA_CREATE_INDEX_ARGS`` environmental variable. If you omit that one, the
elastalert ``config.yaml`` is supplied via the ``--config`` flag.

Example of create index args setting ``EA_CREATE_INDEX="--host localhost --user user --password pass"``.


**Check all supported arguments `elastalert --help`**


## Testing locally

Simply by executing:

```
$ python elastalert_lambda.py
```

Passing arguments using environment:

```
$ ARGS="--debug --patience seconds=5 --es_debug" python elastalert_lambda.py
```

Passing arguments using event:

```
$ echo '{"ARGS": "--debug --patience seconds=5 --es_debug"}' | python elastalert_lambda.py
```
