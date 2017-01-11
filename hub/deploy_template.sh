# Copy this file to hub and or node root and name it deploy.sh and edit the paths
/path_to_python manage.py migrate;
/path_to_python manage.py collectstatic --noinput;
echo "Done";

