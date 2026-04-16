pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = "mrtbadboy"
        DOCKERHUB_CREDENTIALS = "dockerhub-credentials"
    }

    stages {

        stage('Clone Code') {
            steps {
                git 'https://github.com/YOUR_USERNAME/YOUR_REPO.git'
            }
        }

        stage('Build Images') {
            steps {
                script {
                    docker.build("${DOCKERHUB_USERNAME}/user-service:latest", "./services/user-service")
                    docker.build("${DOCKERHUB_USERNAME}/product-service:latest", "./services/product-service")
                    docker.build("${DOCKERHUB_USERNAME}/order-service:latest", "./services/order-service")
                    docker.build("${DOCKERHUB_USERNAME}/gateway-service:latest", "./services/gateway-service")
                }
            }
        }

        stage('Push Images') {
            steps {
                script {
                    docker.withRegistry('', DOCKERHUB_CREDENTIALS) {
                        docker.image("${DOCKERHUB_USERNAME}/user-service:latest").push()
                        docker.image("${DOCKERHUB_USERNAME}/product-service:latest").push()
                        docker.image("${DOCKERHUB_USERNAME}/order-service:latest").push()
                        docker.image("${DOCKERHUB_USERNAME}/gateway-service:latest").push()
                    }
                }
            }
        }
    }
}