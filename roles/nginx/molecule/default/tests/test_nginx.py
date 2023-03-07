import testinfra.utils.ansible_runner
import os

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):

    for name in (
     "/etc/nginx/sites-available/default",
     "/usr/share/nginx/html/index.html",
    ):

        f = host.file(name)
        assert f.exists


def test_nginx_is_installed(host):

    version = ['1.18.0-6ubuntu14.3']
    packages = ['nginx']

    for i, name in enumerate(packages):

        nginx = host.package(name)
        assert nginx.is_installed
        assert nginx.version.startswith(version[i])


def test_if_ngninx_is_runing(host):
   service = host.service("nginx")

   assert service.is_running
   assert service.is_enabled


def test_if_nginx_is_using_port80(host):
    cmd = host.run("lsof -i TCP:80")

    assert cmd.rc == 0


def test_if_ngninx_is_stoped(host):
    cmd = host.run("service nginx stop")
    service = host.service("nginx")

    assert cmd.rc == 0
    assert not service.is_running