def monitor_duration = 1
def drip = 5

def checkout_self(branch) {
    dir('pipeline') {
        deleteDir()

        def git_url = 'git@gitlab.kemptechnologies.com:aconti/drip-new-rs.git'
        def git_creds = '7f29db4c-efbe-4a52-aaf4-34b0db0f6297'

        git([
            url: git_url,
            branch: branch,
            credentialsId: git_creds,
            poll: false
        ])
    }
}

node('master') {
    def status = 0

    stage("Installing dependencies") {
        deleteDir()
        checkout_self('master')
        sh "virtualenv -p python3 .venv"
        sh "./.venv/bin/pip install python-kemptech-api"
    }
    
    stage("Add RS to VS") {
        echo "Adding RS ${rs}"
        sh "./.venv/bin/python3 ./pipeline/deploy_server.py add ${rs}"
    }
    
    stage("Drip traffic to new RS") {
        echo "Dripping ${drip}% traffic to new RS"
        sh "./.venv/bin/python3 ./pipeline/deploy_server.py drip ${rs} ${drip}"
            
    }

    stage("Monitor new RS") {
        echo "Monitoring new RS for ${monitor_duration} minute"
        status = sh(
            script: "./.venv/bin/python3 ./pipeline/deploy_server.py monitor ${rs} ${monitor_duration}",
            returnStatus: true)
        echo "Status: ${status}"
    }
    
    stage("Send notification") {
        if (status == 0) {
            echo "Send notification that deploy was successful"
        } else {
            echo "Send alert notification that deploy failed"
            error("RS did not pass healthchecks during monitoring.") 
        }
    }
}
    
stage("Wait for approval") {
    input message: 'Deploy RS to full production?', ok: 'Deploy'
}

node('master') {
    stage("Deploy to production") {
        sh "./.venv/bin/python3 ./pipeline/deploy_server.py equalize"
    }
}