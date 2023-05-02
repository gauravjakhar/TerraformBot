Jenkinsfile:
```groovy




node {
   def mvnHome
   stage('Preparation') { // for display purposes
      // Get some code from a GitHub repository
      git 'https://github.com/user/repo.git'
      // Get the Maven tool.
      // ** NOTE: This 'M3' Maven tool must be configured
      // **       in the global configuration.
      mvnHome = tool 'M3'
   }
   stage('Build') {
      // Run the maven build
      sh "${mvnHome}/bin/mvn install"
      // Archive the artifacts
      archiveArtifacts 'target/*.jar'
   }
   stage('Test') {
      // Run the maven test
      sh "${mvnHome}/bin/mvn test"
   }
   stage('Deploy') {
      // Deploy to test environment
      sh "${mvnHome}/bin/mvn deploy"
      // Deploy to production environment
      sh "${mvnHome}/bin/mvn deploy"
   }
}
```
