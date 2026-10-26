# Linux access audit with SQL

This case creates three dummy regular files in a fresh temporary directory, joins
their observed Linux modes to declared policies in SQLite, applies scoped chmod
changes and checks actual access as UID/GID 65534 with no supplementary groups.
No host accounts or services are changed; the dummy script is never executed.

The complete execution requires Linux and permission to drop a child process's
UID/GID. Root alone does not guarantee those capabilities inside a restricted
container. A failed probe does not produce a successful execution report.

```sh
sudo python projects/09-linux-access-audit/audit_lab.py --output /tmp/access-report.json
sudo python -m unittest discover -s projects/09-linux-access-audit -p 'test_*.py' -v
```

Run just the SQL policy tests without privilege:

```sh
cd projects/09-linux-access-audit
python -m unittest test_audit_lab.PolicyTests -v
```

The dedicated GitHub Actions workflow records fresh kernel-access evidence and
uploads the report and stdout. Published evidence is added only after inspecting
that real run. Policies cover group/other read on the dummy secret and group/other
write on the script and public notice. ACLs, capabilities, network services and
application authorization are outside this assessment.
