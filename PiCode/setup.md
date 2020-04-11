```
model_package=arn:aws:sagemaker:us-east-1:865070037744:model-package/sassy-atermis-05-693a26662ad851a0e47bf8146e940526
aws iam list-roles --query 'Roles[?AssumeRolePolicyDocument.Statement[?Principal.Service==`sagemaker.amazonaws.com`]].{Arn:Arn,RoleName:RoleName,Principal:AssumeRolePolicyDocument.Statement[0].Principal.Service}'
aws iam get-role --query 'Role.{Arn:Arn}' --role-name <role-name>
execution_role_arn=<iam-role-arn>
instance_type=ml.p2.xlarge
supported_instance_types=(ml.p2.xlarge)






aws sagemaker create-model --model-name sample-model-51119791-78EE-457C-AA7F-679C5CE281DE-1 --execution-role-arn ${execution_role_arn} --primary-container ModelPackageName=${model_package} --enable-network-isolation --region us-east-1
aws sagemaker create-endpoint-config --endpoint-config-name sample-endpointcfg-51119791-78EE-457C-AA7F-679C5CE281DE-1 --production-variants VariantName=variant-1,ModelName=sample-model-51119791-78EE-457C-AA7F-679C5CE281DE-1,InstanceType=${instance_type},InitialInstanceCount=1 --region us-east-1
aws sagemaker create-endpoint --endpoint-name sample-endpoint-51119791-78EE-457C-AA7F-679C5CE281DE-1 --endpoint-config-name sample-endpointcfg-51119791-78EE-457C-AA7F-679C5CE281DE-1 --region us-east-1
aws sagemaker describe-endpoint --endpoint-name sample-endpoint-51119791-78EE-457C-AA7F-679C5CE281DE-1 --region us-east-1








```




```
sudo apt install python3 python3-pip
pip3 install -r requirements.txt
sudo apt-get install python-opencv
pip install opencv-contrib-python==4.1.0.25



```
# Sagemaker
```
https://aws.amazon.com/marketplace/pp/prodview-3dr4kos6pq5cq?ref_=ml_hackathon
https://aws.amazon.com/marketplace/ai/configuration?productId=9883feb9-7190-4372-8eaf-fd5a95126daa
arn:aws:sagemaker:us-east-2:057799348421:model-package/sassy-anthropos-05-28e3401e81bd6a58dd876017dfc821db

```



References

https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/

https://www.pyimagesearch.com/2019/03/25/building-a-raspberry-pi-security-camera-with-opencv/