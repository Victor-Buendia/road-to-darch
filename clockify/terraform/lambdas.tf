# https://medium.com/akava/simple-aws-lambda-deployment-with-terraform-1f51c08c6f4

resource "aws_lambda_function" "lambda_function_instance" {
  function_name    = "${var.environment}-ingestion-lambda-${var.project_name}-${data.aws_caller_identity.current.account_id}"
  filename         = "lambda_handler.zip"
  source_code_hash = data.archive_file.function_zip.output_base64sha256
  handler          = "lambda_handler.lambda_handler"
  runtime          = "python3.8"
  role             = aws_iam_role.lambda_handler_role.arn
  layers           = [
    "arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p38-requests:12",
    "arn:aws:lambda:us-east-1:898466741470:layer:psycopg2-py38:2"
  ]
  timeout = 180
  environment {
    variables = {
        "API_KEY"       = ""
        "BASE_URL"      = "https://reports.api.clockify.me/v1/workspaces"
        "INTERVAL_DAYS" = "365"
        "WORKSPACE_ID"  = ""
        }
  }
}

# https://stackoverflow.com/questions/35895315/use-terraform-to-set-up-a-lambda-function-triggered-by-a-scheduled-event-source
resource "aws_cloudwatch_event_rule" "every_week" {
    name = "every_week"
    description = "Fires every week"
    schedule_expression = "rate(7 days)" # https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html
}

resource "aws_cloudwatch_event_target" "trigger_lambda_every_week" {
    rule = aws_cloudwatch_event_rule.every_week.name
    target_id = "every_week"
    arn = aws_lambda_function.lambda_function_instance.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda_function_instance" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.lambda_function_instance.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.every_week.arn
}

data "archive_file" "function_zip" {
  source_dir  = "${path.root}/../src/"
  type        = "zip"
  output_path = "lambda_handler.zip"
}