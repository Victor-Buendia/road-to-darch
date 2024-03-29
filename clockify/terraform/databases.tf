resource "aws_db_instance" "postgres" {
  allocated_storage   = 5
  db_name             = "db01"
  engine              = "postgres"
  engine_version      = "14.7"
  instance_class      = "db.t3.micro"
  username            = var.postgres_username
  password            = var.postgres_password
  skip_final_snapshot = true
  publicly_accessible = true
}