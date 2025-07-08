from setuptools import setup,find_packages

def get_requirements(file_path: str) -> list:
    """
    This function will return the list of requirements
    mentioned in the requirements.txt file.
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        
        requirements = [req.replace("\n", "") for req in requirements]
    
        if '-e .' in requirements:
            requirements.remove('-e .')
    
    return requirements


setup(    name='ML-Project',
    author='Ragul',
    version='0.0.1',
    description='A simple ML project template',
    author_email="e18269@eng.pdn.ac.lk" ,
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')

    
)