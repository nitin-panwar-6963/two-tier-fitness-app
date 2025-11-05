pipeline{
    agent any
    stages{
        stage("code"){
            steps{
                echo "clonning the code from github..."
                sh "sleep 2s"
                git branch: 'main',url: 'https://github.com/nitin-panwar-6963/two-tier-fitness-app.git'
                echo "cloning code is successfull...."
            }
        }
        stage("build"){
            steps{
                echo "build your docker images for docker hub......"
                sh "sleep 5s"
                sh "docker build -t fitness-app ."
                echo "your docke images id create successfully...."
                sh "docker build -t fitness-app ."
            }
        }
        stage("deploy"){
            steps{
                echo "your code is read for execute..."
                sh "docker compose up -d "
                echo "your app is ready for local host"
            }
        }
    }
}
