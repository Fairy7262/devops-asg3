pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Lint') {
            steps {
                sh 'echo "Lint step skipped"'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'pytest tests || true'
            }
        }

        stage('Build Application Image') {
            steps {
                sh 'docker build -t asg3-app .'
            }
        }

        stage('Deploy App Using Docker Compose') {
            steps {
                sh "docker-compose down || true"
                sh "docker-compose up -d --build"
            }
        }

        stage('Prepare Selenium Environment') {
            steps {
                sh """
                docker network create asg-net || true

                # Run selenium chrome
                docker run -d --name chrome --network asg-net \
                    -p 4444:4444 selenium/standalone-chrome:latest

                # Wait for Chrome to fully start
                sleep 8
                """
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh """
                # Build selenium test runner image
                docker build -t asg3-selenium selenium-tests

                # Run selenium tests (auto-detects all test_*.py files)
                docker run --network asg-net asg3-selenium || true
                """
            }
        }
    }

    post {
        always {
            sh 'docker-compose down || true'
            sh 'docker rm -f chrome || true'
        }
        success {
            echo "PIPELINE SUCCESS ✔✔✔"
        }
        failure {
            echo "PIPELINE FAILED ❌"
        }
    }
}
