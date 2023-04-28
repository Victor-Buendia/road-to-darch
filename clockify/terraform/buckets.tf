resource "aws_s3_bucket" "metadata" {
  bucket = "${var.environment}-metadata-${var.bucket_prefix}-${data.aws_caller_identity.current.account_id}"
}
