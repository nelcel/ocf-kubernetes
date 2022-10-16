from transpire import emit, helm

from apps.versions import versions

values = {
    "kubeProxyReplacement": "strict",
    "k8sServiceHost": "127.0.0.1",
    "k8sServicePort": "6443",
    "nativeRoutingCIDR": "10.0.0.0/8",
    "containerRuntime": {
        "integration": "crio",
    },
    "hubble": {
        "tls": {"auto": {"method": "cronJob"}},
        "listenAddress": ":4244",
        "relay": {"enabled": True},
        "ui": {"enabled": True},
    },
}

name = "cilium"
def objects() -> None:
    emit(
        helm.build_chart_from_versions(
            name="cilium",
            versions=versions,
            values=values,
        )
    )