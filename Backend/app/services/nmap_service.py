import shlex
import subprocess
import tempfile
from pathlib import Path

from app.config import settings
from app.schemas.host import Host
from app.utils.xml_parser import XMLParser


class NmapService:

    def __init__(self):
        self.nmap_binary = settings.nmap_binary
        self.default_arguments = settings.default_scan_arguments

    def scan(self, target: str) -> list[Host]:

        with tempfile.NamedTemporaryFile(
            suffix=".xml",
            delete=False
        ) as temp_file:

            xml_path = Path(temp_file.name)

        command = [
            self.nmap_binary,
            *shlex.split(self.default_arguments),
            "-oX",
            str(xml_path),
            target,
        ]

        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
            )

            xml_content = xml_path.read_bytes()

            hosts = XMLParser.parse(xml_content)

            return hosts

        except subprocess.CalledProcessError as exception:
            raise RuntimeError(
                exception.stderr.strip()
            )

        finally:

            if xml_path.exists():
                xml_path.unlink()