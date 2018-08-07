{
    "variables": {
        "aws_batch_base_ami": "{{env `AWS_BATCH_BASE_AMI`}}"
    },
    "builders": [
        {
            "type": "amazon-ebs",
            "region": "us-east-1",
            "source_ami": "{{user `aws_batch_base_ami`}}",
            "instance_type": "p3.2xlarge",
            "ssh_username": "ec2-user",
            "ami_name": "raster-foundry-batch-gpu-ami-{{timestamp}}",
            "ami_block_device_mappings": [
                {
                    "device_name": "/dev/sdb",
                    "virtual_name": "ephemeral0"
                }
            ],
            "associate_public_ip_address": true
        }
    ],
    "_comment": "Steps below are intended to reset ECS agent state.",
    "provisioners": [
        {
            "type": "shell",
            "script": "./deployment/packer/configure-gpu.sh"
        },
        {
            "type": "shell",
            "inline": [
                "sleep 5",
                "sudo stop ecs",
                "sudo rm -rf /var/lib/ecs/data/ecs_agent_data.json"
            ]
        }
    ]
}
