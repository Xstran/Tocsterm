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
      // Login to Docker registry and push the Docker image
      withCredentials([usernamePassword(credentialsId: "${DOCKER_REGISTRY_CREDS}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
        sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin docker.io"
        sh "docker push ${DOCKER_BFLASK_IMAGE}"
      }

      // Pull the latest Docker image, stop and remove the existing container, and start a new container
      sh "docker pull ${DOCKER_BFLASK_IMAGE}:latest"
      sh "docker stop my-flask-app || true"  // Stop the container if it's running (ignore errors if not found)
      sh "docker rm my-flask-app || true"    // Remove the container if it exists (ignore errors if not found)
      sh "docker run -d -p 5000:5000 --name my-flask-app ${DOCKER_BFLASK_IMAGE}:latest"
    }
  }
}
}

  post {
    always {
      sh 'docker logout'
    }
  }
}
