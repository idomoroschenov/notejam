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

![TechnicalView](https://github.com/idomoroschenov/notejam/blob/44bca2da325e7048f461000f01cb5aaf8cb153e9/notejam-diagrams/TechnicalView.png)


**Deployment Overview**
![DeploymenView](https://github.com/idomoroschenov/notejam/blob/05ba46ea69567a7bdec7ff4456a67a952294fa7c/notejam-diagrams/DeploymentView.png)
