import subprocess

# start the rasa server
rasa_command = f'rasa run --endpoints endpoints.yml --credentials credentials.yml -m models/prod_model.tar.gz --enable-api -p 5005 --cors "*"'


# Chama o comando rasa run a partir do script Python
subprocess.run(rasa_command, shell=True)
