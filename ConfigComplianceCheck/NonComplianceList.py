import pandas as pd 
import boto3
import json
import pprint

MODE = "TEST"

sts = boto3.client('sts')
config = boto3.client('config') 

############################################################
# Module      : get_session
# Description : 
#  Get STS session token. 
#  I must use configured profile for secret data.
#  Care for usage of credentials
############################################################
def get_session():
    MFA_TokenCode = str(input('MFA_TokenCode ->'))
    sts_res = sts.get_session_token(
        SerialNumber='arn:aws:iam::745132880338:mfa/osk-taku_tanaka', 
        TokenCode=MFA_TokenCode
    )
    credentials = sts_res['Credentials']
    session = boto3.session.Session(
        profile_name='odh', 
        aws_session_token=credentials['SessionToken']
    )
    #credentials = session.get_credentials()
    session.get_credentials()
    #return credentials

############################################################
# Module      : get_active_rules
# Description : 
#  Get active rules configured in AWS Config.
############################################################
def get_active_rules():
    # Get JSON listed 
    res = config.describe_config_rules()['ConfigRules']

    # Store each rule which state is 'Active'.
    active_rules = []
    for rule in res:
        if rule['ConfigRuleState'] == 'ACTIVE':
            active_rules.append(rule['ConfigRuleName'])
    
    return active_rules

# MAIN
if __name__ == "__main__":

    print("Module : get_session ----------------------------------")
    get_session()
    # pprint.pprint('export AWS_ACCESS_KEY_ID={}'.format(credentials.access_key))
    # pprint.pprint('export AWS_SECRET_ACCESS_KEY={}'.format(credentials.secret_key))
    # pprint.pprint('export AWS_SESSION_TOKEN={}'.format(credentials.token))
    
    print("Module : get_actove_rules -----------------------------")
    active_rules = get_active_rules()
    pprint.pprint(active_rules)

    # Paginator for get compliance details overflowed limit number.
    paginator = config.get_paginator('get_compliance_details_by_config_rule')

    for rule in active_rules:
        # compliance_details = config.get_compliance_details_by_config_rule(
        #     ConfigRuleName=rule,
        #     ComplianceTypes=['NON_COMPLIANT'],
        #     Limit=100
        # )
        compliance_details = []
        book = paginator.paginate(
            ConfigRuleName=rule,
            ComplianceTypes=['NON_COMPLIANT'],
            Limit=100
        )
        for page in book:
            compliance_details += page['EvaluationResults']


        data = []
        columns = ['ResourceId', 'ResourceType']
        for resource in compliance_details:
            data.append([
                resource['EvaluationResultIdentifier']['EvaluationResultQualifier'][columns[0]],
                resource['EvaluationResultIdentifier']['EvaluationResultQualifier'][columns[1]]
            ])
        if not data:
            continue
        
        df = pd.DataFrame(data, columns=columns)
        #df.to_csv("./csv/"+rule+".csv")
