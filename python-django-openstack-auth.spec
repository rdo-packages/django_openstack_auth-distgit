%if 0%{?fedora}
# python3-keystoneclient missing
# python3-oslo-policy missing
%global with_python3 0

%endif
%global pypi_name django_openstack_auth

Name:           python-django-openstack-auth
Version:        2.0.1
Release:        2%{?dist}
Summary:        Django authentication backend for OpenStack Keystone

License:        BSD
URL:            http://pypi.python.org/pypi/django_openstack_auth/
Source0:        http://pypi.python.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch



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
BuildRequires:  python-pbr >= 1.6
BuildRequires:  python-netaddr
BuildRequires:  python-oslo-sphinx >= 2.3.0
BuildRequires:  gettext
BuildRequires:  python-oslo-config >= 2.3.0
BuildRequires:  python-oslo-policy >= 0.5.0
BuildRequires:  python-mox3
BuildRequires:  python-mock
BuildRequires:  python-testscenarios

Requires:       python-django
BuildRequires:  python-django

Requires:       python-keystoneclient >= 1:1.6.0
Requires:       python-six >= 1.9.0
Requires:       python-oslo-config >= 2.3.0
Requires:       python-oslo-policy >= 0.5.0
Requires:       python-pbr >= 1.6

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
BuildRequires:  python3-pbr >= 1.6
BuildRequires:  python3-netaddr
BuildRequires:  python3-oslo-sphinx >= 2.3.0
BuildRequires:  gettext
BuildRequires:  python3-oslo-config >= 2.3.0
BuildRequires:  python3-oslo-policy >= 0.5.0
BuildRequires:  python3-mock
BuildRequires:  python3-mox3
BuildRequires:  python3-testscenarios

Requires:       python3-django
BuildRequires:  python3-django

Requires:       python3-keystoneclient >= 1:1.6.0
Requires:       python3-six >= 1.9.0
Requires:       python3-oslo-config >= 2.3.0
Requires:       python3-oslo-policy >= 0.5.0
Requires:       python3-pbr >= 1.6

%description -n python3-django-openstack-auth
Django OpenStack Auth is a pluggable Django authentication backend that
works with Django's ``contrib.auth`` framework to authenticate a user against
OpenStack's Keystone Identity API.

The current version is designed to work with the
Keystone V2 API.


%endif



%prep
%setup -q -n %{pypi_name}-%{version}


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
%{__python} setup.py install --skip-build --root %{buildroot}

cp -r openstack_auth/locale %{buildroot}/%{python_sitelib}/openstack_auth

%find_lang django

# don't include tests in the RPM
rm -rf %{buildroot}/%{python_sitelib}/openstack_auth/tests

%if 0%{?with_python3}
%{__python3} setup.py install --skip-build --root %{buildroot}
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
%{python_sitelib}/openstack_auth/locale/openstack_auth.pot
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-django-openstack-auth -f django.lang
%license LICENSE
%dir %{python3_sitelib}/openstack_auth
%dir %{python3_sitelib}/openstack_auth/locale
%dir %{python3_sitelib}/openstack_auth/locale/??/
%dir %{python3_sitelib}/openstack_auth/locale/??_??/
%dir %{python3_sitelib}/openstack_auth/locale/??/LC_MESSAGES
%dir %{python3_sitelib}/openstack_auth/locale/??_??/LC_MESSAGES
%{python3_sitelib}/openstack_auth/*.py*
%{python3_sitelib}/openstack_auth/plugin
%{python3_sitelib}/openstack_auth/locale/openstack_auth.pot
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 15 2015 Matthias Runge <mrunge@redhat.com> - 2.0.1-1
- update to 2.0.1

* Tue Sep 22 2015 Matthias Runge <mrunge@redhat.com> - 2.0.0-1
- update to 2.0.0
- (theoretically) support python3
- really execute tests

* Fri Aug 21 2015 Matthias Runge <mrunge@redhat.com> - 1.2.0-5
- backport initialize hasher for unscoped token
- backport Extend User from AbstractBaseUser
- backport configurable token hasing
- use unscoped token for scoping the project

* Fri Jun 19 2015 Matthias Runge <mrunge@redhat.com> - 1.2.0-4
- "App 'openstack_auth' doesn't have a 'user' model." (rhbz#1232683)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 08 2015 Alan Pevec <apevec@redhat.com> - 1.2.0-2
- update Use AbstractUser instead of AnonymousUser (mrunge)
  Fixes rhbz#1218894 rhbz#1218899
- drop pbr.version removal

* Tue Apr 14 2015 Matthias Runge <mrunge@redhat.com> - 1.2.0-1
- rebase to 1.2.0
- Use AbstractUser instead of AnonymousUser

* Wed Feb 04 2015 Matthias Runge <mrunge@redhat.com> - 1.1.9-1
- rebase to 1.1.9 (rhbz#1145024)

* Thu Dec 11 2014 Matthias Runge <mrunge@redhat.com> - 1.1.7-3
- fix CVE-2014-8124 (rhbz#1170421)

* Thu Nov 13 2014 Matthias Runge <mrunge@redhat.com> - 1.1.7-2
- own locale dirs (rhbz#1163362)

* Fri Sep 26 2014 Matthias Runge <mrunge@redhat.com> - 1.1.7-1
- update to 1.1.7 (rhbz#1145024)

* Thu Sep 11 2014 Matthias Runge <mrunge@redhat.com> - 1.1.6-3
- spec cleanup

* Mon Aug 25 2014 Matthias Runge <mrunge@redhat.com> - 1.1.6-2
- bump version

* Mon Jun 23 2014 Matthias Runge <mrunge@redhat.com> - 1.1.6-1
- update to 1.1.6 (rhbz#1111877)
