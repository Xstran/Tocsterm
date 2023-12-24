pipeline {
  agent any

  stages {
    stage('Build') {
      steps {
        sh 'docker build -t my-flask-app .'

        // Tag both latest and previous for rollback
        sh "docker tag my-flask-app $DOCKER_BFLASK_IMAGE:latest"
        sh "docker tag my-flask-app $DOCKER_BFLASK_IMAGE:previous"
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
          // Login to Docker registry and push the Docker image
          withCredentials([usernamePassword(credentialsId: "${DOCKER_REGISTRY_CREDS}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
            sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin docker.io"
            sh "docker push ${DOCKER_BFLASK_IMAGE}:latest"  // Push only the latest tag
            sh "docker push ${DOCKER_BFLASK_IMAGE}:previous"  // Push the previous tag as well
          }

          // Pull the latest Docker image, stop and remove the existing container, and start a new container
          sh "docker pull ${DOCKER_BFLASK_IMAGE}:latest"
          sh "docker stop my-flask-app || true"
          sh "docker rm my-flask-app || true"
          sh "docker run -d -p 5001:80 --name my-flask-app ${DOCKER_BFLASK_IMAGE}:latest"
        }
      }
    }
  }
  post {
    failure {
      // Rollback to the previous version (using the previous tag)
      sh "docker pull ${DOCKER_BFLASK_IMAGE}:previous"
      sh "docker stop my-flask-app || true"
      sh "docker rm my-flask-app || true"
      sh "docker run -d -p 5001:80 --name my-flask-app ${DOCKER_BFLASK_IMAGE}:previous"

      // Send email notification
      emailext body: "Deployment failed! Rolling back to previous version.",
               subject: "Deployment Failure: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
               to: "ahuraira235@gmail.com"
    }
    always {
      sh 'docker logout'
    }
  }
}
