import os
import sys
import datetime
import shlex

from elastalert import elastalert
from elastalert import create_index

class TmpSysArgv(object):

    def __enter__(self):
        self.orig_argv = sys.argv

    def __exit__(self, *args, **kwargs):
        sys.argv = self.orig_argv

def handler(event, context):
    print("Starting up ElastAlert")
    args = shlex.split(event.get('ARGS', os.getenv('ARGS', '')))

    if '--end' not in args:
        args.extend([
            '--end',
            datetime.datetime.utcnow().isoformat(),
        ])

    if '--config' not in args:
        args.extend(['--config', 'config.yaml'])

    print("Using arguments: `%s`" % args)

    if "EA_CREATE_INDEX" in os.environ:

        if "EA_CREATE_INDEX_ARGS" in os.environ:
            ci_args = ["elastalert-create-index"] + shlex.split(
                os.getenv("EA_CREATE_INDEX_ARGS"))
        else:
            config_index = args.index("--config")
            ci_args = [
                "elastalert-create-index",
                args[config_index],
                args[config_index + 1]
            ]

        print("Creating index for elastalert with args: %s" % (ci_args, ))
        with TmpSysArgv():
            sys.argv = ci_args
            create_index.main()

    try:
        elastalert.main(args)
    except SystemExit as exc:
        if exc.args[0] == 0:
            print("ElastAlert run successfully!")
            return
        raise


if __name__ == "__main__":
    """
    Purely for local testing
    """
    import json
    import sys
    import select
    event = {}
    if select.select([sys.stdin,], [], [], 0.0)[0]:
        event = json.loads(sys.stdin.read())
    handler(event, None)
