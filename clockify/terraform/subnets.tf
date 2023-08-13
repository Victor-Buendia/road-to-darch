# https://terrateam.io/blog/aws-lambda-function-with-terraform

# resource "aws_subnet" "clockify_subnet" {
#   cidr_block = "10.0.1.0/24"
#   vpc_id = aws_vpc.clockify_vpc.id
#   availability_zone = "us-east-1"

#   tags = {
#     Name = "clockify_subnet"
#   }
# }