pipeline {
    agent any

    environment {
        ENVIRONMENT = 'PROD'
        PROD_BASE_URL=https: '//restful-booker.herokuapp.com'
    }

    stages {
        stage('Setup Python Environment') {
            steps {
                // ВСЕ команды в одном sh блоке
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    echo "Python environment setup completed"
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python3 -m pytest --alluredir allure-results
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                // Активация не нужна для allure команды
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }

    post {
        always {
            // Сохранение отчетов о тестировании
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            echo 'The build finished!'
        }
        failure {
            echo 'The build failed!'
        }
    }
}