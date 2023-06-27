
## Build Server Image
docker build ./Server/ -t nimble-server
echo "\n Building Server Image Complete"
echo "example run 'docker run --network host nimble-server'\n\n"


## Build Client Image
docker build ./Client/ -t nimble-client
echo "\n Building Client Image Complete"
echo "example run 'docker run --network host -e Display=\"0\" nimble-client'\n\n"