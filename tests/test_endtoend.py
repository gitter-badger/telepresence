"""
End-to-end tests.
"""

from unittest import TestCase
from pathlib import Path
from subprocess import check_output, Popen, STDOUT
import time

DIRECTORY = Path(__file__).absolute().parent


class EndToEndTests(TestCase):
    """
    End-to-end tests.

    Only reason I'm using this is that I can't figure equivalent of addCleanup
    in py.test.
    """

    def test_tocluster(self):
        """
        Tests of communication to the cluster.

        Python script is run using telepresence --docker-run, and output is
        checked for the string "SUCCESS!" indicating the checks passed. The
        script shouldn't use code py.test would detect as a test.
        """
        result = str(
            check_output([
                "telepresence",
                "--new-deployment",
                "tests",
                "--docker-run",
                "-v",
                "{}:/code".format(DIRECTORY),
                "--rm",
                "python:3.5-slim",
                "python",
                "/code/tocluster.py",
            ]), "utf-8")
        assert "SUCCESS!" in result

    def test_fromcluster(self):
        """
        Tests of communication from the cluster.

        Start webserver that serves files from this directory. Run HTTP query
        against it on the Kubernetes cluster, compare to real file.
        """
        # XXX leaking docker processes, try to figure out why
        p = Popen(
            [
                "telepresence", "--new-deployment", "fromclustertests",
                "--expose", "8080", "--docker-run", "-v",
                "{}:/code".format(DIRECTORY), "--rm", "-w", "/code",
                "python:3.5-slim", "python3", "-m", "http.server", "8080"
            ], )

        def cleanup():
            p.terminate()
            p.wait()

        self.addCleanup(cleanup)
        time.sleep(30)
        result = check_output([
            'kubectl', 'run', '--attach', 'testing123', '--generator=job/v1',
            "--quiet", '--rm', '--image=alpine', '--restart', 'Never',
            '--command', '--', '/bin/sh', '-c',
            "apk add --no-cache --quiet curl && " +
            "curl http://fromclustertests:8080/test_endtoend.py"
        ])
        assert result == (DIRECTORY / "test_endtoend.py").read_bytes()

    def test_existingdeployment(self):
        """
        Tests of communicating with existing Deployment.
        """
        name = "testing-{}".format(time.time()).replace(".", "-")
        version = str(
            check_output(["telepresence", "--version"], stderr=STDOUT),
            "utf-8").strip()
        check_output([
            "kubectl",
            "run",
            "--generator",
            "deployment/v1beta1",
            name,
            "--image=datawire/telepresence-k8s:" + version,
            '--env="MYENV=hello"',
        ])
        self.addCleanup(check_output,
                        ["kubectl", "delete", "deployment", name])
        result = str(
            check_output([
                "telepresence",
                "--deployment",
                name,
                "--docker-run",
                "-v",
                "{}:/code".format(DIRECTORY),
                "--rm",
                "python:3.5-slim",
                "python",
                "/code/tocluster.py",
                "MYENV=hello",
            ]), "utf-8")
        assert "SUCCESS!" in result
