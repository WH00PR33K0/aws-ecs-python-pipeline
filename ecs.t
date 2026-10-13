
  container_definitions = jsonencode([
    {
      name = "cloudops-app"
      image = "://amazonaws.com"
      essential = true
      portMappings = [{ containerPort = 80, hostPort = 80 }]
    }
  ])
}
