from constructs import Construct
from aws_cdk import (
    Duration,
    RemovalPolicy,
    RemovalPolicyOptions,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_dynamodb as dynamodb
)


class DynamodbMigrateTestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self, "DynamodbMigrateTestQueue",
            visibility_timeout=Duration.seconds(300),
        )

        topic = sns.Topic(
            self, "DynamodbMigrateTestTopic"
        )

        topic.add_subscription(subs.SqsSubscription(queue))

        p = RemovalPolicy(RemovalPolicy.RETAIN)
        table = dynamodb.Table(self, "markotestsecond",
            partition_key=dynamodb.Attribute(name="name", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="age", type=dynamodb.AttributeType.STRING),
            removal_policy=p,
            stream=dynamodb.StreamViewType(dynamodb.StreamViewType.NEW_IMAGE)
        )


        # global_secondary_index_props = dynamodb.GlobalSecondaryIndexProps(
        #     index_name="hellp",
        #     partition_key=dynamodb.Attribute(
        #         name="id111",
        #         type=dynamodb.AttributeType.BINARY
        #     ),

        #     # the properties below are optional
        #     non_key_attributes=["nonKeyAttributes"],
        #     projection_type=dynamodb.ProjectionType.KEYS_ONLY,
        #     read_capacity=1,
        #     sort_key=dynamodb.Attribute(
        #         name="id222",
        #         type=dynamodb.AttributeType.BINARY
        #     ),
        #     write_capacity=1
        # )


        table.add_global_secondary_index(index_name="name-index",
            partition_key=dynamodb.Attribute(
                name="name",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1)
        # "CDKMetadata": {
        # "Type": "AWS::CDK::Metadata",
        # "Properties": {
        #     "Analytics": "v2:deflate64:H4sIAAAAAAAA/1WNQQ6CMBBFz8K+HVE27rkAgnsDpcYR7GCnjSFN7y4tiYmb+f+/vGROUEFZ9B+WapzkjAOEzvVqEhu6BX4zhIvXXov6bvaSb0MzqvUH9xkFm83v/MDK4uKQTDL+9pUWVInmEmOqrWbyVuUfNZkRkxlFs7oHmUMFZziWxZMRpfXG4UtDu+cXpUJN470AAAA="
        # },
        # "Metadata": {
        #     "aws:cdk:path": "dynamodb-migrate-test/CDKMetadata/Default"
        # },
        # "Condition": "CDKMetadataAvailable"
        # }
