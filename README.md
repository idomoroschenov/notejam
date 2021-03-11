# Notejam
## Decoupled Architecture

A decoupled version of Notejam project with CI/CD and IaC.

- Serverless
- Ready to deploy in any AWS region
- Cost-effective

## Prerequisites

- AWS CDK
- IAM account with HTTPS Git Credentials
- Python 3.8 or Later
- virtualenv
- AWS CLI with configured account and full access for CloudFormation and S3

## Installation

- Navigate to **notejam-cicd/**
- Activate virtual environment by running `virtualenv venv && source venv/bin/activate`
- Install python dependencies `pip install -r requirements.txt`
- Change the *notejam/variables.py* file to configure application's stage, region and account_id
- Run `cdk deploy` and approve deployment
- Navigate to **notejam-code/** and deploy code to the created repository *notejam.RepoHTTPURL* `



**Technical Overview**

![TechnicalView](https://github.com/idomoroschenov/notejam/blob/7e562e00d38668a8ff18ba6217419778f6212c36/notejam-diagrams/TechnicalView.png)


**Deployment Overview**
![DeploymenView](https://github.com/idomoroschenov/notejam/blob/23557179cb1d5486c935b7f10a4ed6b23fd20115/notejam-diagrams/DeploymentView.png)
