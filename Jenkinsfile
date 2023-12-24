pipeline {
    agent any

    environment {
        DOCKER_REGISTRY_CREDS = 'dockerhub'
        EMAIL_NOTIFICATION = 'ahuraira235@gmail.com'
    }

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
                    try {
                        // Login to Docker registry and push the Docker image
                        withCredentials([usernamePassword(credentialsId: "${DOCKER_REGISTRY_CREDS}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                            sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin docker.io"
                            sh "docker push ${DOCKER_BFLASK_IMAGE}"
                        }

                        // Pull the latest Docker image, stop and remove the existing container, and start a new container
                        sh "docker pull ${DOCKER_BFLASK_IMAGE}:latest"
                        sh "docker stop my-flask-app || true"  // Stop the container if it's running (ignore errors if not found)
                        sh "docker rm my-flask-app || true"    // Remove the container if it exists (ignore errors if not found)
                        sh "docker run -d -p 5001:5000 --name my-flask-app ${DOCKER_BFLASK_IMAGE}:latest"
                    } catch (Exception deployException) {
                        // Deployment failed
                        currentBuild.result = 'FAILURE'

                        // Rollback to the previous version (adjust as needed)
                        // ...

                        // Send email notification
                        emailext(
                            subject: "Deployment Failure - ${env.JOB_NAME} ${env.BUILD_NUMBER}",
                            body: "The deployment of ${env.JOB_NAME} ${env.BUILD_NUMBER} has failed. Please investigate.",
                            to: "${EMAIL_NOTIFICATION}",
                            mimeType: 'text/plain'
                        )

                        // Rethrow the exception to mark the build as failed
                        throw deployException
                    }
                }
            }
        }
    }
    post {
        always {
            // Your existing code for cleanup, e.g., docker logout
            sh 'docker logout'
        }
    }
}
