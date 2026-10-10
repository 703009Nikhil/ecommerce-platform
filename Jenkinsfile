pipeline {
    agent any

    environment {
        AWS_REGION = "ap-southeast-2"
        ECR_REPO = "593964941429.dkr.ecr.ap-southeast-2.amazonaws.com/my-ecom-service"
        IMAGE_NAME = "user-service"
        CLUSTER_NAME = "my-eks-cluster"
        DEPLOYMENT_NAME = "user-deployment"

        AWS_CREDS = credentials('aws-creds')
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

        stage('Set AWS Env') {
            steps {
                script {
                    env.AWS_ACCESS_KEY_ID = env.AWS_CREDS_USR
                    env.AWS_SECRET_ACCESS_KEY = env.AWS_CREDS_PSW
                }
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region ${AWS_REGION} | \
                docker login --username AWS --password-stdin ${ECR_REPO}
                '''
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
