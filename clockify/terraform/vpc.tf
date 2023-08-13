# https://terrateam.io/blog/aws-lambda-function-with-terraform

# resource "aws_vpc" "clockify_vpc" {
#   cidr_block = "10.0.0.0/22" # 2^10 addresses for use (1024)
#   enable_dns_hostnames = true
#   enable_dns_support = true

#   tags = {
#     Name = "clockify_vpc"
#   }
# }