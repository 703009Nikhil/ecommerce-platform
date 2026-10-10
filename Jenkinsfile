pipeline {
    agent any

    environment {
        AWS_REGION = "ap-southeast-2"
        ECR_REPO = "593964941429.dkr.ecr.ap-southeast-2.amazonaws.com/my-ecom-service"
        IMAGE_NAME = "user-service"
        CLUSTER_NAME = "my-eks-cluster"
        DEPLOYMENT_NAME = "user-deployment"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/703009Nikhil/ecommerce-platform'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:latest ./user-service"
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    sh "docker run --rm ${IMAGE_NAME}:latest pytest"
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    sh '''aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 593964941429.dkr.ecr.ap-southeast-2.amazonaws.com/my-ecom-service
'''
                }
            }
        }

        stage('Tag & Push Image') {
            steps {
                script {
                    sh "docker tag ${IMAGE_NAME}:latest ${ECR_REPO}:${IMAGE_NAME}-latest"
                    sh "docker push ${ECR_REPO}:${IMAGE_NAME}-latest"
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                script {
                    sh "aws eks update-kubeconfig --region ${AWS_REGION} --name ${CLUSTER_NAME}"
                    sh "kubectl rollout restart deployment ${DEPLOYMENT_NAME} --namespace default"
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully. Deployment updated on EKS."
        }
        failure {
            echo "Pipeline failed. Check logs for details."
        }
    }
}
