import os, shutil

folders = [os.path.expanduser('~/.aws/sso/cache')]#,os.path.expanduser('~/.aws/cli/cache')]

def CacheDeleted():
    for folder in folders:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
                return False
    return True

if __name__ == "__main__":
    if CacheDeleted() :
        print('Success! Cache cleared')
    else:
        print('Failure! Check the above error message and try again')
