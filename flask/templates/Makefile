
help: 
	echo install_venv - Install Virtual Environment$("\n")
	echo create_venv - Createt my Virtual Environment$("\n")
	echo activate_venv - Activate Virtual Environment$("\n")
	echo freeze_requirements - Freeze dependencies and create requirements.txt$("\n")
	echo install_dependencies - Install dependencies from requirements.txt $("\n")
	echo deactivate_venv - quit from Virtual Environment$("\n")



install-venv:
	pip3 install virtual env

create-folder:
	mkdir VENVS

echo put-name:
	virtualenv $(ENV_NAME)

echo activate:
	source venv/bin/activate

requirements:
	pip freeze --local > requirements.txt 

deactivate:
	deactivate
  
clean:
	rm -f *.txt