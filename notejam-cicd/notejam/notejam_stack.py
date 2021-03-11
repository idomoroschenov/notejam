from aws_cdk import core as cdk
from aws_cdk import core
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codecommit as codecommit
from aws_cdk import aws_codebuild as codebuild
from aws_cdk import aws_logs as logs
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_rds as rds
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_elasticloadbalancingv2 as lb
from aws_cdk import aws_codepipeline_actions as codepipeline_actions
import variables
import random
import string
import json


def create_img_def():
    with open('../notejam/imagedefinitions.json', 'w') as file:
        img = [{
            'name': variables.ecr_repo_name,
            'imageUri': f'{variables.account_id}.dkr.ecr.{variables.region}.amazonaws.com/{variables.ecr_repo_name}'
        }]
        json.dump(img, file)
create_img_def()


def generate_secret():
    secret = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(12))
    return secret
password = generate_secret()


class NotejamStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # CodeCommit Repo
        repository = codecommit.Repository(self, "Repository}", repository_name=f"Notejam-{variables.stage}",
                                           description="Git repository for Notejam project")
        # core.Tags.of(repository).add("Test_Key", "Test_Value")
        repository_http_url = core.CfnOutput(self, "Repo HTTP URL", value=repository.repository_clone_url_http,
                                             export_name="CodeCommit-HTTP-URL")


        #CodeBuild Project
        build_spec = codebuild.BuildSpec.from_object(dict(
            version="0.2",
            phases=dict(
                pre_build=dict(
                    commands=[
                        "echo Logging into AWS ECR",
                        "aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com"
                        ""
                    ]
                ),
                build=dict(
                    commands=[
                        "echo Build started on `date`",
                        "echo Building Docker image",
                        "docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .",
                        "docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG"
                    ]
                ),
                post_build=dict(
                    commands=[
                        "echo Build complete on `date`",
                        "echo Pushing the Docker image",
                        "docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG",
                        f"aws ecs update-service --cluster notejam-{variables.stage} --service notejam-{variables.stage} --desired-count 1"
                        "echo Done"
                    ]
                )
            ),
            artifacts={
                "files": [
                    "imagedefinitions.json"
                ]
            }
        ))

        build_log_group = logs.LogGroup(self, "CodeBuild logs", log_group_name=f"notejam-{variables.stage}-codebuild",
                                        removal_policy=core.RemovalPolicy.DESTROY)
        codebuild_project = codebuild.PipelineProject(self, "CodeBuild Project", project_name=f"Notejam-{variables.stage}",
                                                      description="CodeBuild project to build Notejam images",
                                                      build_spec=build_spec, check_secrets_in_plain_text_env_variables=False,
                                                      environment_variables=variables.buildspec_vars,
                                                      environment=codebuild.BuildEnvironment(privileged=True,
                                                                                             build_image=codebuild.LinuxBuildImage.STANDARD_5_0)
                                                                                             ,
                                                      logging=codebuild.LoggingOptions(
                                                      cloud_watch=codebuild.CloudWatchLoggingOptions(enabled=True,
                                                      log_group=build_log_group
                                                      )))

        codebuild_project.add_to_role_policy(iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                             resources=['*'], actions=['ecr:*']))


        # ECR Repository
        ecr_repository = ecr.Repository(self, 'ECR Repository',
                                        repository_name=variables.ecr_repo_name)

        # Networking
        vpc = ec2.Vpc(self, "VPC")
        psql_sec_group = ec2.SecurityGroup(self, 'PSQL Security Group', vpc=vpc)
        container_sec_group = ec2.SecurityGroup(self, 'Container Security Group', vpc=vpc)
        alb_sec_group = ec2.SecurityGroup(self, 'ALB Security Group', vpc=vpc)
        psql_sec_group.add_ingress_rule(peer=container_sec_group, connection=ec2.Port.tcp(5432))
        container_sec_group.add_ingress_rule(peer=alb_sec_group, connection=ec2.Port.tcp(5000))
        alb_sec_group.add_ingress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(80))

        private_subnets = [i.subnet_id for i in vpc.private_subnets]
        public_subnets = [i.subnet_id for i in vpc.public_subnets]


        # Aurora Cluster
        # psql_subnet_group = rds.SubnetGroup(
        #     self,
        #     'PostgreSQL Subnet Group',
        #     description='Created for Notejam project',
        #     vpc=vpc,
        #     subnet_group_name='notejam' + variables.stage
        # )

        psql_subnet_group = rds.CfnDBSubnetGroup(
            self,
            'DB Subnet Group',
            db_subnet_group_description='test',
            subnet_ids=private_subnets,
            db_subnet_group_name='notejamdev'
        )
        psql_cluster = rds.CfnDBCluster(
            self,
            'PostgreSQL Cluster',
            database_name='notejam',
            db_cluster_parameter_group_name='default.aurora-postgresql10',
            db_cluster_identifier=f'notejam-{variables.stage}',
            engine='aurora-postgresql',
            engine_mode='serverless',
            master_username=variables.user,
            master_user_password=password,
            port=5432,
            db_subnet_group_name='notejamdev',
            vpc_security_group_ids=[psql_sec_group.security_group_id]
            )
        cluster_endpoint = core.CfnOutput(self, 'Aurora Cluster Endpoint',
                                          value=psql_cluster.attr_endpoint_address,
                                          export_name='postgresql-cluster-endpoint'
                                          )

        psql_cluster.add_depends_on(psql_subnet_group)


        # IAM Resources
        dev_policy = iam.ManagedPolicy(self, 'Dev Policy',
                                       statements=[iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                       resources=['*'], actions=['codecommit:*'
                                       , 'codebuild:*', 'codepipeline:*'])])

        dev_group = iam.Group(self, 'Dev Group', group_name='Developers',
                              managed_policies=[dev_policy])


        # ECS Cluster
        cluster = ecs.Cluster(self, 'MyCluster', vpc=vpc, cluster_name=f'notejam-{variables.stage}')

        task_definition_1 = ecs.TaskDefinition(self, 'Task Definition',
                compatibility=ecs.Compatibility('FARGATE'), cpu='256',
                memory_mib='512')
        container = task_definition_1.add_container(f'{variables.ecr_repo_name}'
                , image=ecs.ContainerImage.from_ecr_repository(ecr_repository),
                environment={'ENVIRONMENT': 'production',
                'SQLALCHEMY_DATABASE_URI': f'postgresql://{variables.user}:{password}@{psql_cluster.attr_endpoint_address}/notejam'
                },
                logging=ecs.LogDriver.aws_logs(stream_prefix='notejamcontainer'
                ))

        container.add_port_mappings(ecs.PortMapping(container_port=5000,
                                    host_port=5000))

        service = ecs.FargateService(
            self,
            'Service',
            cluster=cluster,
            desired_count=0,
            service_name=f'notejam-{variables.stage}',
            task_definition=task_definition_1,
            assign_public_ip=True,
            security_groups=[container_sec_group]
            )

        alb = lb.ApplicationLoadBalancer(self, 'Notejam ALB',
                                         internet_facing=True,
                                         load_balancer_name='notejam', vpc=vpc,
                                         security_group=alb_sec_group)
        alb.name = core.CfnOutput(self, 'DNS',
                                  value=alb.load_balancer_dns_name,
                                  export_name='alb-dns-name')

        http_listener = alb.add_listener('HTTP Listener', open=True, port=80)

        http_listener.add_targets('ECS', port=80,
                                  targets=[service.load_balancer_target(container_name='notejamdev'
                                  , container_port=5000)],
                                  health_check=lb.HealthCheck(healthy_http_codes='200,302'
                                  ))




        # CodePipeline
        pipeline = codepipeline.Pipeline(self, 'Pipeline',
                                         stages=[codepipeline.StageProps(stage_name='Source'
                                         ,
                                         actions=[codepipeline_actions.CodeCommitSourceAction(action_name='Source'
                                         , branch='master',
                                         repository=repository,
                                         output=codepipeline.Artifact(artifact_name='SourceArtifact'
                                         ))]),
                                         codepipeline.StageProps(stage_name='Build'
                                         ,
                                         actions=[codepipeline_actions.CodeBuildAction(action_name='Build'
                                         , project=codebuild_project,
                                         input=codepipeline.Artifact(artifact_name='SourceArtifact'
                                         ),
                                         outputs=[codepipeline.Artifact(artifact_name='BuildArtifact'
                                         )])]),
                                         codepipeline.StageProps(stage_name='Deploy'
                                         ,
                                         actions=[codepipeline_actions.EcsDeployAction(service=service,
                                         input=codepipeline.Artifact(artifact_name='BuildArtifact'
                                         ), action_name='Deploy')])])
