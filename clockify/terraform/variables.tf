data "aws_caller_identity" "current" {}

variable environment {
	type = string
}

variable bucket_prefix {
	type = string
}