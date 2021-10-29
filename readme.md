Overview
===
Even thought its not required i included in this little project all the best practices and trics i learned over the years,this includes:

- A scalable django project structure suitable for large applications.
- The efficient use of DRF permissions, serializers & viewsets.
- Unit tests using pytests and some of its advanced features.
- Linters/pre-commit hooks suitable for a CI/CD envirment with multiple collaborators 


Instalation
==
- Create a virtual environement.
- Install the production requirements `requirements/prod.txt`.
- Apply the migrations `python src/manage.py migrate`.
- Run the unit tests `cd src ; pytest ./../tests` .
- Optionally, install the dev requirements if you want to edit the code.
