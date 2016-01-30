# upgrading pip
pip install -U pip

# initializing submodules
git submodule init
git submodule update


# installing submodules and requirements
cd submodules

pip install -r requirements.txt

cd scicfg
pip uninstall scicfg -y
pip install .
cd ..

cd clusterjobs
pip uninstall clusterjobs -y
pip install .
cd ..

cd environments
pip uninstall environments -y
pip install .
cd ..

cd fastlearners
pip uninstall fastlearners -y
pip install .
cd ..

cd learners
pip uninstall learners -y
pip install .
cd ..

cd explorers
pip uninstall explorers -y
pip install .
cd ..

cd experiments
pip uninstall experiments -y
pip install .
cd ..
