# Notejam

A decoupled version of Notejam project with CI/CD and IaC.

- Serverless
- Ready to deploy in any AWS region
- Cost-effective

## Prerequisites

- AWS CDK
- Python 3.8 or Later
- virtualenv
- AWS CLI with configured account and full access for CloudFormation and S3

## Installation

- Navigate to **notejam-cicd/**
- Activate virtual environment by running `virtualenv venv && source venv/bin/activate`
- Install python dependencies `pip install -r requirements.txt`
- Change the *notejam/variables.py* file to configure application's stage, region and account_id
- Run `cdk bootstrap` to provision deployment infrastructure. Specify your account id and region where deployment should take place.
- Run `cdk deploy --all` to deploy the application
- When finished, cdk will output app URL

## Initial requirements

![Requirements](https://github.com/idomoroschenov/notejam/blob/b182142215affd5f538006e24e135181839faa60/notejam-diagrams/notejam.png)

- Application is ready to scale dynamically based on the traffic load which is implemented via ECS scaling policy for the web layer and via Aurora Serverless scaling for the data layer.
- Regular snapshots of the database are taken and are availalbe for S3 export. They will be kept for 3 years in a warm state and archived after that period.
- Both container fleet and the database span across multiple availability zones thus making service resillient to the outages
- All infrastructure is described in Python code and is ready to be deployed in any available region with respective variables
- A development CI/CD pipeline is created for the developers and the Dev group is provisioned in the account allowing developers to work with the required resources
- Application can be deployed in several modes that would run independently. It is possible to include per-stage rollout of the service in the development pipeline
- All logs are exported to the CloudWatch log groups and are available for the analysis

## Design Assumptions

![DesignAssumptions](https://github.com/idomoroschenov/notejam/blob/d6c100d6ea74abc7d91dffc617f7eee70d0f368a/notejam-diagrams/Architectural%20Decisions.png)

## Implemented Architecture

**Technical Overview**

![TechnicalView](https://github.com/idomoroschenov/notejam/blob/44bca2da325e7048f461000f01cb5aaf8cb153e9/notejam-diagrams/TechnicalView.png)

The architecture above is the first iteration which covers all business requirements.

**Deployment Overview**
![DeploymenView](https://github.com/idomoroschenov/notejam/blob/05ba46ea69567a7bdec7ff4456a67a952294fa7c/notejam-diagrams/DeploymentView.png)


## Further recommendations
