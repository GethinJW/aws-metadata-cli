# AWS Metadata CLI

# Requirements

You will need the following to run this program:
- Python3.11
- Pre-preppared IAM user account

# Build the program

build the program with:
```bash
make build
```

# Setup Env vars

Create an IAM user in AWS [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html).

Once you have your user, generate an access key, and secret access key, following the guide [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)

Run the command:
```bash
cp .env.copy .env
```

And the fill in the appropriate values in the newly created `.env` file.

```
AWS_ACCESS_KEY_ID="<AWS ACCESS KEY>"
AWS_SECRET_ACCESS_KEY="<AWS SECRET ACCESS KEY>"
AWS_REGION="<AWS REGION>"
```

Make sure to give the IAM user access to various services you wish for them to be able to see within AWS, see [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html)

# Run the program

run the cli with:
``` bash
make run
```

## Example Usage:
See the following example:
![example](./assets/example.png)
