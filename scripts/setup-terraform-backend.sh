#!/bin/bash
# Terraform State Backend Setup Script
# This script creates S3 buckets and DynamoDB tables for Terraform state management

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="fortune-event-automation"
AWS_REGION="${AWS_REGION:-ap-northeast-1}"
ENVIRONMENTS=("dev" "stg" "prd")

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        log_error "AWS CLI is not installed. Please install it first."
        exit 1
    fi

    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        log_error "AWS credentials are not configured. Run 'aws configure' first."
        exit 1
    fi

    # Get AWS account ID
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    log_info "AWS Account ID: ${AWS_ACCOUNT_ID}"

    log_info "Prerequisites check passed ✓"
}

create_s3_bucket() {
    local env=$1
    local bucket_name="${PROJECT_NAME}-tfstate-${env}"

    log_info "Creating S3 bucket: ${bucket_name}"

    # Check if bucket already exists
    if aws s3 ls "s3://${bucket_name}" 2>&1 | grep -q 'NoSuchBucket'; then
        # Create bucket
        if [ "${AWS_REGION}" == "us-east-1" ]; then
            aws s3api create-bucket \
                --bucket "${bucket_name}" \
                --region "${AWS_REGION}"
        else
            aws s3api create-bucket \
                --bucket "${bucket_name}" \
                --region "${AWS_REGION}" \
                --create-bucket-configuration LocationConstraint="${AWS_REGION}"
        fi

        # Enable versioning
        aws s3api put-bucket-versioning \
            --bucket "${bucket_name}" \
            --versioning-configuration Status=Enabled

        # Enable encryption
        aws s3api put-bucket-encryption \
            --bucket "${bucket_name}" \
            --server-side-encryption-configuration '{
                "Rules": [{
                    "ApplyServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "AES256"
                    },
                    "BucketKeyEnabled": true
                }]
            }'

        # Block public access
        aws s3api put-public-access-block \
            --bucket "${bucket_name}" \
            --public-access-block-configuration \
                BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

        # Add lifecycle policy to delete old versions
        aws s3api put-bucket-lifecycle-configuration \
            --bucket "${bucket_name}" \
            --lifecycle-configuration '{
                "Rules": [{
                    "Id": "DeleteOldVersions",
                    "Status": "Enabled",
                    "NoncurrentVersionExpiration": {
                        "NoncurrentDays": 90
                    }
                }]
            }'

        # Add bucket tagging
        aws s3api put-bucket-tagging \
            --bucket "${bucket_name}" \
            --tagging "TagSet=[
                {Key=Project,Value=${PROJECT_NAME}},
                {Key=Environment,Value=${env}},
                {Key=ManagedBy,Value=Terraform}
            ]"

        log_info "S3 bucket created: ${bucket_name} ✓"
    else
        log_warn "S3 bucket already exists: ${bucket_name}"
    fi
}

create_dynamodb_table() {
    local env=$1
    local table_name="${PROJECT_NAME}-tflock-${env}"

    log_info "Creating DynamoDB table: ${table_name}"

    # Check if table already exists
    if ! aws dynamodb describe-table --table-name "${table_name}" &> /dev/null; then
        aws dynamodb create-table \
            --table-name "${table_name}" \
            --attribute-definitions AttributeName=LockID,AttributeType=S \
            --key-schema AttributeName=LockID,KeyType=HASH \
            --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
            --tags "Key=Project,Value=${PROJECT_NAME}" \
                   "Key=Environment,Value=${env}" \
                   "Key=ManagedBy,Value=Terraform" \
            --region "${AWS_REGION}"

        # Wait for table to be active
        log_info "Waiting for DynamoDB table to be active..."
        aws dynamodb wait table-exists --table-name "${table_name}" --region "${AWS_REGION}"

        # Enable point-in-time recovery
        aws dynamodb update-continuous-backups \
            --table-name "${table_name}" \
            --point-in-time-recovery-specification PointInTimeRecoveryEnabled=true \
            --region "${AWS_REGION}"

        log_info "DynamoDB table created: ${table_name} ✓"
    else
        log_warn "DynamoDB table already exists: ${table_name}"
    fi
}

update_terraform_backend_config() {
    local env=$1
    local bucket_name="${PROJECT_NAME}-tfstate-${env}"
    local table_name="${PROJECT_NAME}-tflock-${env}"
    local backend_file="terraform/environments/${env}/backend.tf"

    log_info "Updating backend configuration: ${backend_file}"

    # Create backend.tf if it doesn't exist
    cat > "${backend_file}" <<EOF
# Terraform Backend Configuration
# Auto-generated by setup-terraform-backend.sh

terraform {
  backend "s3" {
    bucket         = "${bucket_name}"
    key            = "terraform.tfstate"
    region         = "${AWS_REGION}"
    dynamodb_table = "${table_name}"
    encrypt        = true
  }
}
EOF

    log_info "Backend configuration updated: ${backend_file} ✓"
}

print_summary() {
    log_info "========================================="
    log_info "Terraform Backend Setup Complete"
    log_info "========================================="
    echo ""
    log_info "Created resources:"
    for env in "${ENVIRONMENTS[@]}"; do
        echo "  Environment: ${env}"
        echo "    S3 Bucket: ${PROJECT_NAME}-tfstate-${env}"
        echo "    DynamoDB Table: ${PROJECT_NAME}-tflock-${env}"
        echo ""
    done

    log_info "Next steps:"
    echo "  1. Review backend configurations in terraform/environments/*/backend.tf"
    echo "  2. Initialize Terraform: cd terraform/environments/dev && terraform init"
    echo "  3. Plan deployment: terraform plan"
    echo "  4. Apply changes: terraform apply"
    echo ""
    log_info "Documentation: docs/setup/terraform-backend.md"
}

# Main execution
main() {
    log_info "Starting Terraform Backend Setup"
    log_info "Project: ${PROJECT_NAME}"
    log_info "Region: ${AWS_REGION}"
    echo ""

    check_prerequisites

    for env in "${ENVIRONMENTS[@]}"; do
        log_info "========================================="
        log_info "Setting up environment: ${env}"
        log_info "========================================="

        create_s3_bucket "${env}"
        create_dynamodb_table "${env}"
        update_terraform_backend_config "${env}"

        echo ""
    done

    print_summary
}

# Run main function
main "$@"
