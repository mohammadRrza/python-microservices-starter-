pipeline {
    agent any
    parameters {
        choice(
            name: 'ENV',
            choices: ['dev', 'staging', 'prod'],
            description: 'Deployment environment'
        )

        booleanParam(
            name: 'DEPLOY',
            defaultValue: false,
            description: 'Deploy after build?'
        )
    }
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

stage('Deploy') {
    when {
        expression { params.DEPLOY }
    }
    steps {
        withCredentials([
            sshUserPrivateKey(
                credentialsId: 'server-ssh-key',
                keyFileVariable: 'SSH_KEY',
                usernameVariable: 'USER'
            )
        ]) {
            sh '''
                ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$USER@161.35.28.3" '
                    mkdir -p /opt/microservices/deploy
                '

                scp -i "$SSH_KEY" -o StrictHostKeyChecking=no \
                    deploy/docker-compose.prod.yml \
                    "$USER@161.35.28.3:/opt/microservices/deploy/docker-compose.yml"

                ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$USER@161.35.28.3" "
                    cd /opt/microservices/deploy
                    echo IMAGE_TAG=${params.IMAGE_TAG} > .env
                    docker-compose pull
                    docker-compose up -d
                "
            '''
        }
    }
}
    }
    post {
        always {
            cleanWs()
        }
    }
}