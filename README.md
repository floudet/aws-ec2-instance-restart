# Stop/Start an AWS EC2 instance for Public IP renewal

Automation script for AWS EC2:
- Stops an AWS EC2 instance and Start it again to renew its public IP

## Usage
```
usage: aws-ec2-instance-restart.py [-h] --config CONFIG --instance INSTANCE
                                   --region REGION

Restarts an AWS EC2 instance and grab its new Public IP

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        AWS credentials file
  --instance INSTANCE, -i INSTANCE
                        Name of the instance to restart
  --region REGION, -r REGION
                        AWS Region
```

## Output samples

```
./aws-ec2-instance-restart.py -c ~/.aws/credentials -i myinstance -r eu-west-3
 * InstanceId : i-0abc123d45ef6gh7i
 * InstancePublicIpAddress : 52.XX.XX.XX
 * Instance State : running
Stopping 'myinstance'................

'myinstance' has been successfully stopped
Starting instance 'myinstance'.................

'myinstance' has been successfully started
 * InstancePublicIpAddress : 52.XX.XX.XY
 ```

## License

Copyright (c) 2020 Fabien Loudet
