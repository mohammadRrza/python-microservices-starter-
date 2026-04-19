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

        stage('Branch Info') {
            steps {
                echo "Branch: ${env.BRANCH_NAME}"
                echo "Image tag: ${env.IMAGE_TAG}"
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

        stage('Test') {
            when {
                expression {
                    env.BRANCH_NAME?.startsWith('feature/') || env.BRANCH_NAME == 'main'
                }
            }
            steps {
                echo "Running tests for ${env.BRANCH_NAME}"
                script {
                    def services = [
                        'user-service',
                        'product-service',
                        'order-service',
                        'gateway-service'
                    ]

                    for (service in services) {
                        sh "docker run --rm ${DOCKERHUB_USERNAME}/${service}:${IMAGE_TAG} pytest -v"
                    }
                }
            }
        }

        stage('Push Images') {
            when {
                expression {
                    env.BRANCH_NAME?.startsWith('bugfix/') || env.BRANCH_NAME == 'main'
                }
            }
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
                allOf {
                    branch 'main'
                    expression { params.DEPLOY }
                }
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
                        "REMOTE_DIR=/opt/microservices/${params.ENV}",
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
        success {
            echo "Pipeline succeeded on ${env.BRANCH_NAME}"
        }
        failure {
            echo "Pipeline failed on ${env.BRANCH_NAME}"
        }
        always {
            cleanWs()
        }
    }
}