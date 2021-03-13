#!/usr/bin/env python3

from aws_cdk import core as cdk

from aws_cdk import core

from notejam.notejam_stack import NotejamStack
from notejam.codecommit_stack import CodeCommitStack


from notejam import variables


import datetime


env = cdk.Environment(account=variables.account_id, region=variables.region)

app = cdk.App()


CodeCommitStack(app, 'notejam-repository', env=env)
NotejamStack(app, f"notejam-main-{variables.stage}", env=env)

app.synth()
