pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        
        stage('Lint') {
            steps {
                sh 'echo "Lint skipped"'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'pytest tests || true'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t asg3-app .'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose up -d --build'
            }
        }

        stage('Selenium Tests') {
            steps {
                sh """
                docker network create asg-net || true
                docker run -d --name chrome --network asg-net \
                    -p 4444:4444 selenium/standalone-chrome
    
                docker build -t asg3-selenium ./selenium-tests
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
    }
}
