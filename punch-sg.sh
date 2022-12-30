#!/bin/bash -e

PORT=12345
SG_ID=sg-01234567
RULE_DESCR='Example rule description'

MY_CURRENT_IP=`dig -4 TXT +short o-o.myaddr.l.google.com @ns1.google.com | awk -F'"' '{print $2}'`
MY_PREVIOUS_IP=`aws ec2 describe-security-groups --filters Name=group-id,Values=$SG_ID --query "SecurityGroups[].IpPermissions[?FromPort==\\\`$PORT\\\`].IpRanges[][?Description==\\\`$RULE_DESCR\\\`].CidrIp | [0][0]" --output text`

echo Previous IP $MY_PREVIOUS_IP
echo Current IP $MY_CURRENT_IP

if [ "$MY_PREVIOUS_IP" != "None" ]; then
  aws ec2 revoke-security-group-ingress --group-id $SG_ID --protocol udp --port $PORT --cidr $MY_PREVIOUS_IP
fi

IPRANGES="[{CidrIp=$MY_CURRENT_IP/32,Description=\"$RULE_DESCR\"}]"
echo $IPRANGES
aws ec2 authorize-security-group-ingress --group-id $SG_ID --ip-permissions "IpProtocol=udp,FromPort=$PORT,ToPort=$PORT,IpRanges=$IPRANGES"
