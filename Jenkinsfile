pipeline {
  agent any

  stages {
    stage('Build') {
      steps {
        sh 'docker build -t my-flask-app .'
        sh 'docker tag my-flask-app $DOCKER_BFLASK_IMAGE'
      }
    }
    stage('Test') {
      steps {
        sh 'docker run my-flask-app python -m pytest app/tests/'
      }
    }
    stage('Deploy') {
      steps {
        script {
          // Write a Docker Compose file
          writeFile file: 'docker-compose.yml', text: """
          version: '3'
          services:
            my-flask-app:
              image: ${DOCKER_BFLASK_IMAGE}:latest
              ports:
                - "5000:5000"
              container_name: my-flask-app
          """

          // Deploy the application using Docker Compose
          sh 'docker-compose -f docker-compose.yml up -d'
        }
      }
    }
  }
  post {
    always {
      script {
        // Remove the Docker Compose file
        sh 'rm docker-compose.yml'
      }
      sh 'docker logout'
    }
  }
}
