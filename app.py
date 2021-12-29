#!/usr/bin/env python3

import aws_cdk as cdk

from dynamodb_migrate_test.dynamodb_migrate_test_stack import DynamodbMigrateTestStack


app = cdk.App()
DynamodbMigrateTestStack(app, "dynamodb-migrate-test")

app.synth()
