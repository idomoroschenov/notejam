# Notejam
## Decoupled Architecture

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

## Implemented Architecture
**Technical Overview**

![TechnicalView](https://github.com/idomoroschenov/notejam/blob/44bca2da325e7048f461000f01cb5aaf8cb153e9/notejam-diagrams/TechnicalView.png)


**Deployment Overview**
![DeploymenView](https://github.com/idomoroschenov/notejam/blob/05ba46ea69567a7bdec7ff4456a67a952294fa7c/notejam-diagrams/DeploymentView.png)
