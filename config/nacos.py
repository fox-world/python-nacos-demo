class NacosServer:

    def __init__(self, server_port, server_address):
        self.server_port = server_port
        self.server_address = server_address


class NacosService:

    def __init__(self, namespace, cluster_name, group_name, service_name, service_address):
        self.namespace = namespace
        self.cluster_name = cluster_name
        self.group_name = group_name
        self.service_name = service_name
        self.service_address = service_address
