{
    "variables": {
        "raster_vision_gpu_version": "",
        "aws_region": "",
        "aws_gpu_ami": "",
        "branch": ""
    },
    "builders": [
        {
            "name": "raster-vision-gpu",
            "type": "amazon-ebs",
            "region": "{{user `aws_region`}}",
            "source_ami": "{{user `aws_gpu_ami`}}",
            "instance_type": "p3.2xlarge",
            "ssh_username": "ec2-user",
            "ami_name": "raster-vision-gpu-{{timestamp}}-{{user `branch`}}",
            "run_tags": {
                "PackerBuilder": "amazon-ebs"
            },
            "ami_block_device_mappings": [
                 {
                     "delete_on_termination": true,
                     "device_name": "/dev/xvda",
                     "volume_size": 120,
                     "volume_type": "gp2"
                 }
            ],
            "tags": {
                "Name": "raster-vision-gpu",
                "Version": "{{user `raster_vision_gpu_version`}}",
                "Created": "{{ isotime }}"
            },
            "associate_public_ip_address": true
        }
    ],
    "_comment": "Steps below are intended to reset ECS agent state.",
    "provisioners": [
        {
            "type": "shell",
            "script": "./packer/configure-gpu.sh"
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
