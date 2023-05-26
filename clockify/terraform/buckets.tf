resource "aws_s3_bucket" "metadata" {
  bucket = "${var.environment}-metadata-${var.project_name}-${data.aws_caller_identity.current.account_id}"
}
