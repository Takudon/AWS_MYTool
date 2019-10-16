#!/bin/bash

###############################################
# Date:2019-06-10
# Abstruct:
#   lambda version check all region
# Ref:
#   It can't work normally in us-west-2...
###############################################

# REGIONS=(`aws ec2 describe-regions --query Regions[*].RegionName --output text`)
# for region in ${REGIONS[@]}
# do
#         echo "[${region}]"
#         aws lambda list-functions --region ${region}| jq -c '.Functions[] | [.FunctionName, .Runtime]'| sed -e 's/"//g' | sed -e 's/\[//g' |  sed -e 's/\]//g'
#         echo "-----------------------------------"
# done 
 
#$REGIONS = aws ec2 describe-regions --query Regions[*].RegionName

$REGIONS = aws ec2 describe-regions | ConvertFrom-Json
$Destination = "./json"

if(!(Test-Path $Destination)){
        mkdir $Destination
}

foreach($region in $REGIONS.Regions){
        $regionName = $region.RegionName
        Write-Host $regionName
        aws lambda list-functions --region $region.RegionName | Add-Content -Encoding utf8 "./$Destination/$regionName.json"
}

Write-Host "List Up Completed."