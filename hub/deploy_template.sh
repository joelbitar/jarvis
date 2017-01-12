# Copy this file to hub and or node root and name it deploy.sh and edit the paths
cd path_to_yarvis;
git fetch origin;
git checkout origin/_branch_;
path_to_python path_to_django manage.py migrate;
path_to_python path_to_django manage.py collectstatic --noinput;
echo "Done";

