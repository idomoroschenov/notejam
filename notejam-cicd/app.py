#!/usr/bin/env python3

from aws_cdk import core as cdk

from aws_cdk import core

from notejam.notejam_stack import NotejamStack

from notejam import variables

import datetime


env = cdk.Environment(account=variables.account_id, region=variables.region)

app = cdk.App()
NotejamStack(app, f"notejam-{variables.stage}", env=env)

app.synth()
