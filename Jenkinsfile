pipeline {
  agent any
  environment {
    PATH = "/opt/homebrew/bin:/usr/local/bin:/Applications/Docker.app/Contents/Resources/bin:${env.PATH}"
  }
  triggers { pollSCM('* * * * *') }
  stages {
    stage('Test') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install -r requirements-dev.txt
          pytest -v
        '''
      }
    }
    stage('Build image') {
      steps {
        sh 'docker build -t minishop:$(cat VERSION)-b${BUILD_NUMBER} .'
      }
    }
    stage('Deploy locally') {
      steps {
        sh '''
          docker rm -f minishop-live || true
          docker run -d --name minishop-live -p 8000:8000 minishop:$(cat VERSION)-b${BUILD_NUMBER}
          for i in $(seq 1 20); do curl -fs http://localhost:8000/health && exit 0; sleep 1; done
          docker logs minishop-live
          exit 1
        '''
      }
    }
  }
}
