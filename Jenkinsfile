pipeline {
    agent any

    parameters {
      gitParameter(
         type: 'PT_TAG',
         name: 'BUILD_TAG',
         defaultValue: 'opentyrian-2.1-17.20221123g50ba362',
         description: 'Which tag to build',
         selectedValue: 'TOP',
         sortMode: 'DESCENDING_SMART'
        )
    }

    options {
        disableConcurrentBuilds abortPrevious: true
        timestamps()
        timeout(10)
    }

    triggers {
        pollSCM '''TZ=Europe/Prague
            H/5 * * * *'''
    }

    environment {
        COPR_CONFIG_FILE = credentials('copr-auth')
        REGISTRY = 'nostovo.arnostdudek.cz:32769'
        IMAGE_NAME = 'copr-builder'
        IMAGE_TAG = "${REGISTRY}/${IMAGE_NAME}"
        UPSTREAM_REPO = 'git@github.com:dudekaa/opentyrian-spec.git'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(
                    branches: [[name: params.BUILD_TAG]],
                    browser: github('https://github.com/dudekaa/opentyrian-spec'),
                    extensions: [],
                    userRemoteConfigs: [
                        [
                            credentialsId: 'jenkins',
                            url: 'git@[nostovo.arnostdudek.cz:2244]:opentyrian-spec.git'
                        ]
                    ]
                )
            }
        }

        stage('Lint') {
            agent {
                docker {
                    alwaysPull true
                    image "${IMAGE_TAG}"
                    registryCredentialsId 'nexus-jenkins'
                    registryUrl "https://${REGISTRY}"
                }
            }
            steps {
                sh 'rpmlint opentyrian.spec'
            }
        }

        stage('Push to upstream') {
            // push to github to make sure there are no commits missing in upstream
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'jenkins', keyFileVariable: 'SSH_KEY')]) {
                    sh '''
                        export GIT_SSH_COMMAND="ssh -i $SSH_KEY -o StrictHostKeyChecking=no"
                        git remote add upstream "$UPSTREAM_REPO" || true
                        git push upstream "$BUILD_TAG"
                    '''
                }
            }
        }

        stage('Build') {
            agent {
                docker {
                    alwaysPull true
                    image "${IMAGE_TAG}"
                    registryCredentialsId 'nexus-jenkins'
                    registryUrl "https://${REGISTRY}"
                }
            }
            // trigger build in COPR infrastructure
            steps {
                sh 'copr-cli --config ' + env.COPR_CONFIG_FILE + ' buildscm opentyrian --clone-url "https://' + env.UPSTREAM_REPO + '" --spec opentyrian.spec --commit ' + params.BUILD_TAG
            }
        }
    }
}