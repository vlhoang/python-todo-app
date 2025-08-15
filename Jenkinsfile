pipeline {
    agent {
        docker {
            image 'my-jenkins-python-azure'
            args '-u root:root' // so we can install extra packages if needed
        }
    }

    environment {
        AZURE_CREDENTIALS = credentials('azure-sp-credentials')
        AZURE_SUBSCRIPTION_ID = '3ccf5cb3-4402-41c5-9526-b0d0b77796f5'
        RESOURCE_GROUP = 'test-webapp-rg'
        APP_NAME = 'hvlinhtodoapp'
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/vlhoang/python-todo-app.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Azure Login') {
            steps {
                sh '''
                    echo "$AZURE_CREDENTIALS" > azure_creds.json
                    az login --service-principal \
                        --username $(jq -r .clientId azure_creds.json) \
                        --password $(jq -r .clientSecret azure_creds.json) \
                        --tenant $(jq -r .tenantId azure_creds.json)
                    az account set --subscription $AZURE_SUBSCRIPTION_ID
                '''
            }
        }

        stage('Deploy to Azure App Service') {
            steps {
                sh '''
                    az webapp up \
                      --resource-group $RESOURCE_GROUP \
                      --name $APP_NAME \
                '''
            }
        }
    }

    post {
        always {
            sh 'rm -f azure_creds.json'
        }
    }
}