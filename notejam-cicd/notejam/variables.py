from aws_cdk.aws_codebuild import BuildEnvironmentVariable as build_var

stage = 'DEV'
account_id = '617023782104'
region = 'eu-west-1'
ecr_repo_name = 'notejam' + stage.lower()
tags = {
    'stage': stage,
    'project': 'Notejam'
}
user = 'postgres'

buildspec_vars = {
    'AWS_DEFAULT_REGION': build_var(value=region),
    'AWS_ACCOUNT_ID': build_var(value=account_id),
    'IMAGE_TAG': build_var(value='latest'),
    'IMAGE_REPO_NAME': build_var(value=ecr_repo_name)
}
