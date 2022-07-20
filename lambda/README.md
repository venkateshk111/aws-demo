1. Create IAM Policy ***ec2-stop-start-iam-policy.json***  
2. Create IAM Role and attach policy ***ec2-stop-start-iam-policy.json***  to IAM Role
3. Change Below details in the files ***startec2.py*** and ***stopec2.py*** according to your AWS region and your instance id
      ```
      region = 'us-west-1'
      instances = ['i-12345abcde4f78g9h', 'i-08sf9b2f7csef6d52']
      ```
