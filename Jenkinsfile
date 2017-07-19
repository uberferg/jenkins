#!/usr/bin/env groovy
//Declarative Jenkins Pipeline
//2017-07-19

import java.time.*

pipeline {
   agent any
   stages {
      stage('Checkout') {
         steps {
              sh "echo woudl checkout here"
 //           checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'e5589e10-b755-49b0-8f64-b06df6ade600', url: 'https://github.com/Aqueti/acos.git']]])
         }
      }
      stage('Build') {
         steps {
            sh "mkdir -p build/acos"
            dir('build/acos') {
               sh "cmake ../.. -DBUILD_API:BOOL=ON -DBUILD_AGT:BOOL=ON -DBUILD_APPLICATIONS:BOOL=ON -DBUILD_TESTS:BOOL=ON -DBUILD_DEB_PACKAGE:BOOL=ON -DDOXYGEN_DIR:BOOL=~/Documentation"
               sh "make -j"
               
               dir('applications-prefix/src/applications-build/') {
                  sh "make package"
                  sh 'scp *.deb 192.168.0.1:"/storage/Web/software"'
               }
               dir('agt-prefix/src/agt-build/') {
                  sh "make package"
                  sh 'scp *.deb 192.168.0.1:"/storage/Web/software"'
               }
            }
         }
      }
      stage('Deploy') {
         steps {
            sh "echo deploying..."
            sh 'scp build/acos/INSTALL/deb/* 192.168.0.1:"/storage/Web/software"'
         }
      }
   }

   post {
      // Always runs. And it runs before any of the other post conditions.
//      always {
//         // Let's wipe out the workspace before we finish!
//         deleteDir()
//      }
    
      success {
         sh "Sending success e-mail"
         mail(
             to: "sfeller@aqueti.com", 
             subject: "Jenkins build passed.",
             body: "Nothing to see here"
         )
      }

      failure {
         sh "Sending failure e-mail"
         mail(
           to: "steve@example.com", 
           subject: "Jenkins build failed!", 
           body: "Nothing to see here"
        )
    }
  }
}

