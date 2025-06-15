echo "Setup Started"
cd "election-runner"

python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
echo "Python setup done"


cd ../user-registerer/ur-backend
npm install
npx tsc 
echo "ur-backend setup done"

cd ../ur-frontend
npm install 
npx tsc
echo "ur-frontend setup done"

cd ../../
echo "setup done"