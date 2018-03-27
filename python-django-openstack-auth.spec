%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%if 0%{?fedora}
%global with_python3 1
%endif

%global pypi_name django_openstack_auth

Name:           python-django-openstack-auth
Version:        3.6.0
Release:        1%{?dist}
Summary:        Django authentication backend for OpenStack Keystone

License:        BSD
URL:            http://pypi.python.org/pypi/django_openstack_auth/
Source0:        https://tarballs.openstack.org/django_openstack_auth/django_openstack_auth-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  git

%description
Django OpenStack Auth is a pluggable Django authentication backend that
works with Django's ``contrib.auth`` framework to authenticate a user against
OpenStack's Keystone Identity API.

The current version is designed to work with the
Keystone V2 API.

%package -n python2-django-openstack-auth
Summary:        Django authentication backend for OpenStack Keystone

%{?python_provide:%python_provide python2-django-openstack-auth}
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-keystoneclient
BuildRequires:  python-iso8601
BuildRequires:  python-pbr >= 2.0.0
BuildRequires:  python-netaddr
BuildRequires:  python-openstackdocstheme
BuildRequires:  gettext
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-policy
BuildRequires:  python-mox3
BuildRequires:  python-mock
BuildRequires:  python-testscenarios

Requires:       python-django
BuildRequires:  python-django

Requires:       python-keystoneclient >= 1:3.8.0
Requires:       python-six >= 1.9.0
Requires:       python-oslo-config >= 2:4.0.0
Requires:       python-oslo-policy >= 1.23.0
Requires:       python-pbr >= 2.0.0
Requires:       python-keystoneauth1 >= 3.1.0

%description -n python2-django-openstack-auth
Django OpenStack Auth is a pluggable Django authentication backend that
works with Django's ``contrib.auth`` framework to authenticate a user against
OpenStack's Keystone Identity API.

The current version is designed to work with the
Keystone V2 API.


%if 0%{?with_python3}

%package -n python3-django-openstack-auth
Summary:        Django authentication backend for OpenStack Keystone

%{?python_provide:%python_provide python3-django-openstack-auth}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx
BuildRequires:  python3-keystoneclient
BuildRequires:  python3-iso8601
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  python3-netaddr
BuildRequires:  gettext
BuildRequires:  python3-oslo-config >= 2:4.0.0
BuildRequires:  python3-oslo-policy >= 1.23.0
BuildRequires:  python3-mock
BuildRequires:  python3-mox3
BuildRequires:  python3-testscenarios

Requires:       python3-django
BuildRequires:  python3-django

Requires:       python3-keystoneclient >= 1:3.8.0
Requires:       python3-six >= 1.9.0
Requires:       python3-oslo-config >= 2:4.0.0
Requires:       python3-oslo-policy >= 1.23.0
Requires:       python3-pbr >= 2.0.0
Requires:       python3-keystoneauth1 >= 3.1.0

%description -n python3-django-openstack-auth
Django OpenStack Auth is a pluggable Django authentication backend that
works with Django's ``contrib.auth`` framework to authenticate a user against
OpenStack's Keystone Identity API.

The current version is designed to work with the
Keystone V2 API.


%endif


%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git


# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -f {test-,}requirements.txt

%build
# generate translations
cd openstack_auth && django-admin compilemessages && cd ..

# remove unnecessary .po files
find . -name "django.po" -exec rm -f '{}' \;


%{__python} setup.py build

%if 0%{?with_python3}
%{__python3} setup.py build
%endif

# generate html docs
PYTHONPATH=.:$PYTHONPATH sphinx-build doc/source html

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

cp -r openstack_auth/locale %{buildroot}/%{python_sitelib}/openstack_auth

%find_lang django --all-name

# don't include tests in the RPM
rm -rf %{buildroot}/%{python2_sitelib}/openstack_auth/tests

%if 0%{?with_python3}
%{__python3} setup.py install --skip-build --root %{buildroot}
cp -r openstack_auth/locale %{buildroot}/%{python3_sitelib}/openstack_auth
cp django.lang django3.lang
sed -i 's/python%{python_version}/python%{python3_version}/' django3.lang
rm -rf %{buildroot}/%{python3_sitelib}/openstack_auth/tests
%endif


%check
export PYTHONPATH=$PYTHONPATH
%{__python} openstack_auth/tests/run_tests.py

%files -n python2-django-openstack-auth -f django.lang
%license LICENSE
%dir %{python_sitelib}/openstack_auth
%dir %{python_sitelib}/openstack_auth/locale
%dir %{python_sitelib}/openstack_auth/locale/??/
%dir %{python_sitelib}/openstack_auth/locale/??_??/
%dir %{python_sitelib}/openstack_auth/locale/??/LC_MESSAGES
%dir %{python_sitelib}/openstack_auth/locale/??_??/LC_MESSAGES
%{python_sitelib}/openstack_auth/*.py*
%{python_sitelib}/openstack_auth/plugin
%{python_sitelib}/%{pypi_name}-*.egg-info

%if 0%{?with_python3}
%files -n python3-django-openstack-auth -f django3.lang
%license LICENSE
%dir %{python3_sitelib}/openstack_auth
%dir %{python3_sitelib}/openstack_auth/locale
%dir %{python3_sitelib}/openstack_auth/locale/??/
%dir %{python3_sitelib}/openstack_auth/locale/??_??/
%dir %{python3_sitelib}/openstack_auth/locale/??/LC_MESSAGES
%dir %{python3_sitelib}/openstack_auth/locale/??_??/LC_MESSAGES
%{python3_sitelib}/openstack_auth/*.py*
%{python3_sitelib}/openstack_auth/plugin
%{python3_sitelib}/openstack_auth/__pycache__
%{python3_sitelib}/%{pypi_name}-*.egg-info
%endif

%changelog
* Tue Mar 27 2018 RDO <dev@lists.rdoproject.org> 3.6.0-1
- Update to 3.6.0

* Mon Aug 21 2017 Alfredo Moralejo <amoralej@redhat.com> 3.5.0-1
- Update to 3.5.0

