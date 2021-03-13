from aws_cdk import aws_s3_assets as s3_assets

from aws_cdk import aws_iam as iam

from aws_cdk import aws_codecommit as codecommit

from aws_cdk import core as cdk

import variables

import os


class CodeCommitStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # CodeCommit Repo

        codecommit_zip = s3_assets.Asset(self, 'Code for Code Notejam', path=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'notejam-code')),
        readers=[iam.ServicePrincipal('codecommit.amazonaws.com')])


        s3_obj = codecommit.CfnRepository.S3Property(bucket=codecommit_zip.s3_bucket_name, key=codecommit_zip.s3_object_key)
        code_obj = codecommit.CfnRepository.CodeProperty(branch_name='master', s3=s3_obj)
        cfn_repository = codecommit.CfnRepository(self, 'Repository',
        repository_name=f'notejam-{variables.stage}', code=code_obj)
