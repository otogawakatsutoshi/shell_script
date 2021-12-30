
import sys
import fire
from version import Version
import pexpect
import os

# 
# hotbackup coldbackup
# aws s3 upload　yyyy/mm/dd/時間.tar.gz という形で固める。
# sftp upload
# cloud bucket
# sync development

# sync development email passwordをdevelopersとかに変更する。
# private key path
# rsync -e "ssh -i ~/.ssh/id_rsa" -avz 転送元ファイル ユーザー名@転送先アドレス:転送先ディレクトリ/


class MsSQLServer(object):

    def __init__(self, Edition: int = 3) -> None:
        # Express is 3
        self.Edition = Edition
        self.root_password = os.environ['SQLSERVER_PASSWORD']
        

    def install(self) -> None:
        Edition = self.Edition
        password = self.root_password
        shell_cmd = "/opt/mssql/bin/mssql-conf setup"
        prc = pexpect.spawn('/bin/bash', ['-c', shell_cmd],timeout=1200)
        prc.expect("Enter your edition")
        prc.sendline(Edition)
        prc.expect("Do you accept the license terms")
        prc.sendline("Yes")
        prc.expect("Enter the SQL Server system administrator password")
        prc.sendline(password)
        prc.expect("Confirm the SQL Server system administrator password")
        prc.sendline(password)
        prc.expect( pexpect.EOF )

if __name__ == '__main__':
    version = Version()
    if not version.check():
        print('python version greater than {1}.{2}'.
        format(version.valid_version.major,version.valid_version.minor)
            ,file=sys.stderr
        )
        exit(1)

    fire.Fire(MsSQLServer)
    # python aaa.py add 10 20
    # python multiply 10 20
