resource "aws_s3_bucket" "metadata" {
  bucket = "${var.environment}-metadata-${var.bucket_prefix}-${data.aws_caller_identity.current.account_id}"
}

resource "aws_s3_bucket" "testbucket" {
  bucket = "${var.environment}-testbucket-${var.bucket_prefix}-${data.aws_caller_identity.current.account_id}"
}