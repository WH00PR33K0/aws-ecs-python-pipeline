import os

print("Assembling self-healing Infrastructure as Code blueprint...")

# Construct the script lines with dynamic data queries instead of hardcoded strings
lines = [
    'provider "aws" {',
    '  region = "us-east-1"',
    '}',
    '',
    '# Dynamically fetches your default VPC network information',
    'data "aws_vpc" "default" {',
    '  default = true',
    '}',
    '',
    '# Dynamically fetches the active subnet IDs inside your active VPC',
    'data "aws_subnets" "default" {',
    '  filter {',
    '    name   = "vpc-id"',
    '    values = [data.aws_vpc.default.id]',
    '  }',
    '}',
    '',
    'resource "aws_ecs_cluster" "app_cluster" {',
    '  name = "cloudops-apps-cluster-tf"',
    '}',
    '',
    'resource "aws_ecs_task_definition" "app_task" {',
    '  family                   = "cloudops-app-task-tf"',
    '  network_mode             = "awsvpc"',
    '  requires_compatibilities = ["FARGATE"]',
    '  cpu                      = "256"',
    '  memory                   = "512"',
    '  execution_role_arn       = "arn:aws:iam::396037508514:role/ecsTaskExecutionRole"',
    '',
    '  container_definitions = jsonencode([',
    '    {',
    '      name      = "cloudops-app"',
      f'      image     = "://amazonaws.com",'
    '      essential = true',
    '      portMappings = [',
    '        {',
    '          containerPort = 80',
    '          hostPort      = 80',
    '        }',
    '      ]',
    '    }',
    '  ])',
    '}',
    '',
    'resource "aws_ecs_service" "app_service" {',
    '  name            = "cloudops-web-service-tf"',
    '  cluster         = aws_ecs_cluster.app_cluster.id',
    '  task_definition = aws_ecs_task_definition.app_task.arn',
    '  launch_type     = "FARGATE"',
    '  desired_count   = 1',
    '',
    '  network_configuration {',
    '    subnets          = data.aws_subnets.default.ids',
    '    assign_public_ip = true',
    '  }',
    '}'
]

with open("ecs.tf", "w") as f:
    f.write("\n".join(lines) + "\n")

print("🚀 SUCCESS! ecs.tf has been built with dynamic self-healing configurations!")