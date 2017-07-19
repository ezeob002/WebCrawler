from urllib.parse import urlparse
import os


class General:
    # Get the domain name for a url (example.com)
    @staticmethod
    def get_domain_name(url):
        try:
            results = General.get_sub_domain_name(url).split('.')
            return results[-2] + '.' + results[-1]
        except Exception as error:
            return ''

    # Get the sub domain name (name.example.com)
    @staticmethod
    def get_sub_domain_name(url):
        try:
            return urlparse(url).netloc
        except Exception as error:
            print('Cannot retrieve the information')
            return ''

    # Create a folder
    @staticmethod
    def create_project_dir(directory):
        if not os.path.exists(directory):
            print('Creating directory ' + directory)
            os.makedirs(directory)

    @staticmethod
    def create_data_files(project_name):
        results = os.path.join(project_name, 'result.txt')
        # Always create a new file
        General.write_file(results, ' ')

    # Create a new file
    @staticmethod
    def write_file(path, data):
        with open(path, 'w') as file:
            file.write(data)

    @staticmethod
    def append_to_file(path, data):
        with open(path, 'a') as file:
            file.write(data + '\n')
