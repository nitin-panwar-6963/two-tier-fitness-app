pipeline{
    agent {label "nitin"}
    environment{
        NAMESPACE= "flask"
        IMAGE= "fitness-app"
    }
    stages{
        stage("cloning"){
            steps{
            echo "cloning code form the github"
            git branch: "main" , url: "https://github.com/nitin-panwar-6963/two-tier-fitness-app.git"
            echo "code clone successfull......"
            }
        }
        stage("build"){
            steps{
                echo "building docker image"
                sh "docker build -t $IMAGE ."
                echo "docker image created successfully......."
            }
        }
        stage("push to docker hub"){
            steps{
                echo "image push to dockerhub........." 
                withCredentials([usernamePassword('credentialsId':"docker", passwordVariable:"dockerHubpass" , usernameVariable: "dockerhubuser")]){
                    sh "docker login -u ${env.dockerhubuser} -p  ${env.dockerhubpass}"
                    sh "docker image tag $IMAGE:latest ${env.dockerhubuser}/$IMAGE:latest"
                    sh "docker push ${env.dockerhubuser}/$IMAGE:latest"
                echo "successfully push image to docker hub......"    
            }
            }
        }
        stage("create Namespace"){
            steps{
                echo "create namespace"
                sh "kubectl get ns $NAMESPACE || kubectl create ns $NAMESPACE"
                echo "successfully created namespace -> $NAMESPACE"
            }
        }
        stage("deployment and service"){
            steps{
                sh '''
                kubectl apply -f k8s/mysql-secret.yml -n $NAMESPACE
                kubectl apply -f k8s/mysql-service.yml -n $NAMESPACE
                kubectl apply -f k8s/mysql-deployment.yml -n $NAMESPACE
                kubectl apply -f k8s/flask-config.yml -n $NAMESPACE
                kubectl apply -f k8s/flask-deployment.yml -n $NAMESPACE
                kubectl apply -f k8s/flask-service.yml -n $NAMESPACE
                  '''
            }
        }
        stage("deploy"){
            steps{
                sh '''
                kubectl port-forward service/flask-service -n $NAMESPACE 5000:5000 --address=0.0.0.0
                '''
            }
        }
    }
}
