pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = "mrtbadboy"
        DOCKERHUB_CREDENTIALS = "dockerhub-credentials"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Build Images') {
            steps {
                script {
                    def services = [
                        'user-service',
                        'product-service',
                        'order-service',
                        'gateway-service'
                    ]

                    for (service in services) {
                        docker.build(
                            "${DOCKERHUB_USERNAME}/${service}:${IMAGE_TAG}",
                            "./services/${service}"
                        )
                    }
                }
            }
        }

        stage('Push Images') {
            steps {
                script {
                    def services = [
                        'user-service',
                        'product-service',
                        'order-service',
                        'gateway-service'
                    ]

                    docker.withRegistry('', DOCKERHUB_CREDENTIALS) {
                        for (service in services) {
                            docker.image("${DOCKERHUB_USERNAME}/${service}:${IMAGE_TAG}").push()
                            docker.image("${DOCKERHUB_USERNAME}/${service}:${IMAGE_TAG}").push('latest')
                        }
                    }
                }
            }
        }
    }
}