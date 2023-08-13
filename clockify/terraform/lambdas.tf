# https://medium.com/akava/simple-aws-lambda-deployment-with-terraform-1f51c08c6f4

resource "aws_lambda_function" "lambda_function_instance" {
  function_name    = "${var.environment}-ingestion-lambda-${var.project_name}-${data.aws_caller_identity.current.account_id}"
  filename         = "lambda_handler.zip"
  source_code_hash = data.archive_file.function_zip.output_base64sha256
  handler          = "lambda_handler.lambda_handler"
  runtime          = "python3.9"
  role             = aws_iam_role.lambda_handler_role.arn
#   vpc_config {
#     subnet_ids = [aws_subnet.example.id]
#     security_group_ids = [aws_security_group.example.id]
#   }
}

data "archive_file" "function_zip" {
  source_dir  = "${path.root}/../src/"
  type        = "zip"
  output_path = "lambda_handler.zip"
}