[![build](https://github.com/SoftmedTanzania/tanzania-openhim-hdr/workflows/build/badge.svg)](https://github.com/SoftmedTanzania/tanzania-openhim-hdr/actions?query=workflow%3Abuild)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/e7ad2143ece9446192877e233a7b2ffd)](https://www.codacy.com/gh/SoftmedTanzania/tanzania-openhim-hdr/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SoftmedTanzania/tanzania-openhim-hdr&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/SoftmedTanzania/tanzania-openhim-hdr/badge.svg?branch=development)](https://coveralls.io/github/SoftmedTanzania/tanzania-openhim-hdr?branch=development)
# Tanzania Health Data Repository
A Health Data Repository for data visualization for received from EMR systems through [OpenHIM](http://openhim.org/) mediators.



# Installation Instructions
1. Download and Install Python from <code>https://www.python.org/</code> depending on your operating system.
2. Download and Install PostgreSQL from <code>https://www.postgresql.org/</code> depending on your operating system.
3. Download and Install Git in your machine from <code>https://git-scm.com/</code> depending on your operating system.
4. Clone the Tanzania Health Data Repository project from GitHub by running the command <code>git clone git@github.com:SoftmedTanzania/tanzania-openhim-hdr.git </code>
5. Install any text editor or IDE of your choice which runs terminal/bash on it i.e VS Code, Vim, PyCharm IDE.
6. After Python is successfully installed, open your terminal/bash then run <code>pip3 install pipenv</code>.
7. Then, upgrade pip by running the command <code>python -m pip3 install –upgrade pip3</code>
8. Navigate to the project folder then run the command <code>pipenv shell</code> to create and activate the Project Environment if does not exist.
9. After successful activation of the environment, run <code>pipenv install</code> to install all the packages needed for the project.
10. Run this command to run the development server <code>python manage.py runserver</code> or <code>./manage.py runserver</code>
11. Press CTRL+C for Linux and Windows or CMD+C for Mac to quit the running server.
12. Run <code>./manage.py migrate</code> to migrate the authentication tables to the database which is the SQLite database by default.
13. Run <code>./manage.py createsuperuser</code> to create the first admin user to the sysem.
14. Run the command <code>python manage.py runserver</code> or <code>./manage.py runserver</code> to re-run the development server.
15. DONE!!