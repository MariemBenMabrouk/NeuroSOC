from lxml import etree

from app.schemas.host import Host, Service


class XMLParser:

    @staticmethod
    def parse(xml_content: bytes) -> list[Host]:
        root = etree.fromstring(xml_content)

        hosts = []

        for host in root.findall("host"):

            status_element = host.find("status")
            status = (
                status_element.get("state")
                if status_element is not None
                else "unknown"
            )

            ip_address = None
            mac_address = None
            vendor = None

            for address in host.findall("address"):
                address_type = address.get("addrtype")

                if address_type == "ipv4":
                    ip_address = address.get("addr")

                elif address_type == "mac":
                    mac_address = address.get("addr")
                    vendor = address.get("vendor")

            hostname = None

            hostnames = host.find("hostnames")
            if hostnames is not None:
                hostname_element = hostnames.find("hostname")
                if hostname_element is not None:
                    hostname = hostname_element.get("name")

            operating_system = None

            os_element = host.find("os")
            if os_element is not None:
                os_match = os_element.find("osmatch")
                if os_match is not None:
                    operating_system = os_match.get("name")

            services = []

            ports = host.find("ports")

            if ports is not None:

                for port in ports.findall("port"):

                    state_element = port.find("state")
                    service_element = port.find("service")

                    services.append(
                        Service(
                            port=int(port.get("portid")),
                            protocol=port.get("protocol"),
                            state=state_element.get("state")
                            if state_element is not None
                            else "unknown",
                            service=service_element.get("name")
                            if service_element is not None
                            else "unknown",
                            product=service_element.get("product")
                            if service_element is not None
                            else None,
                            version=service_element.get("version")
                            if service_element is not None
                            else None,
                        )
                    )

            hosts.append(
                Host(
                    ip_address=ip_address,
                    hostname=hostname,
                    mac_address=mac_address,
                    vendor=vendor,
                    operating_system=operating_system,
                    status=status,
                    services=services,
                )
            )

        return hosts