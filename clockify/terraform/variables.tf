data "aws_caller_identity" "current" {}

variable environment {
	type = string
}

variable project_name {
	type = string
}

variable postgres_username {
	type = string
}

variable postgres_password {
	type = string
}