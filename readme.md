# REQUIREMENTS
You need to install postgresql

# SETUP
> ## 1 - Create a virtual environment
> Run the following command in your terminal replacing ***your path*** by the path where you will create the project

 - `Linux`
```bash
python3 -m venv "your path"
```
 - `Windows`
```shell
python -m venv "your path"
```

> ## 2 - Creating the project
> Copy the source code of this project inside the virtual environment just created

> ## 3 - Activating the virtual environment
> Open a terminal in the root folder of the project and run this command
 
 - `Linux`
```bash
Scripts/activate
```

 - `Windows`
```shell
Scripts\activate.bat
```

> ## 4 - Installing the dependencies
> Run this command on the just opened terminal, and wait to finish the installation

```bash
pip install -r requirements.txt
```

> ## 5 - Running the project
> Run this command in your opened terminal, wait for the app startup is completed and open your browser at http://localhost:8000/docs

```bash
fastapi dev main.py
```

# TESTING
> ## NOTE: Run the app is not necessary
> Run this command on your opened terminal

 - `Linux`
```bash
python3 main_tests.py
```

 - `Windows`
```shell
python main_tests.py
```