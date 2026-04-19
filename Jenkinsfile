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
                    withEnv([
                        "DEPLOY_SERVER=161.35.28.3",
                        "REMOTE_DIR=/opt/microservices/deploy",
                        "DEPLOY_TAG=${IMAGE_TAG}"
                    ]) {
                        sh '''
                            ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$USER@$DEPLOY_SERVER" "mkdir -p $REMOTE_DIR"

                            scp -i "$SSH_KEY" -o StrictHostKeyChecking=no \
                                deploy/docker-compose.prod.yml \
                                "$USER@$DEPLOY_SERVER:$REMOTE_DIR/docker-compose.yml"

                            ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$USER@$DEPLOY_SERVER" "
                                cd $REMOTE_DIR
                                echo IMAGE_TAG=$DEPLOY_TAG > .env
                                docker compose pull
                                docker compose up -d
                            "
                        '''
                    }
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