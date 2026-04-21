@Library('my-shared-lib') _

import com.helper.DockerHelper
import com.helper.DeployHelper

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

        stage('Checkout') {
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

                    def dockerHelper = new DockerHelper(this)

                    dockerHelper.buildImages(
                        services,
                        env.DOCKERHUB_USERNAME,
                        env.IMAGE_TAG
                    )
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

                    def dockerHelper = new DockerHelper(this)

                    dockerHelper.pushImages(
                        services,
                        env.DOCKERHUB_USERNAME,
                        env.IMAGE_TAG,
                        env.DOCKERHUB_CREDENTIALS
                    )
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
                script {
                    def deployHelper = new DeployHelper(this)

                    deployHelper.deployWithCompose(
                        credentialsId: 'server-ssh-key',
                        server: '161.35.28.3',
                        remoteDir: "/opt/microservices/${params.ENV}",
                        imageTag: env.IMAGE_TAG,
                        composeFile: 'deploy/docker-compose.prod.yml'
                    )
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline succeeded on ${env.BRANCH_NAME}"
        }
        failure {
            echo "❌ Pipeline failed on ${env.BRANCH_NAME}"
        }
        always {
            cleanWs()
        }
    }
}
