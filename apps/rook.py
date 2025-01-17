from transpire import helm

from apps.versions import versions

values = {"image": {"tag": "v1.5.1"}}

name = "rook"
ceph_yaml = {
    "apiVersion": "ceph.rook.io/v1",
    "kind": "CephCluster",
    "metadata": {
        "name": "ceph",
        "namespace": "rook",
        "annotations": {"argocd.argoproj.io/compare-options": "IgnoreExtraneous"},
    },
    "spec": {
        "cephVersion": {"image": "ceph/ceph:v15.2.6"},
        "dataDirHostPath": "/var/lib/rook",
        "mon": {"count": 3, "allowMultiplePerNode": False},
        "dashboard": {
            "enabled": True,
        },
        "storage": {
            "useAllNodes": False,
            "useAllDevices": False,
            "nodes": [
                {
                    "name": "jaws",
                    "devices": [
                        {
                            "name": "/dev/disk/by-id/ata-Samsung_SSD_860_EVO_1TB_S3Z8NB0K932843P",
                            "config": {},
                        },
                        {
                            "name": "/dev/disk/by-id/ata-Samsung_SSD_860_EVO_1TB_S3Z8NB0K933151M",
                            "config": {},
                        },
                        {
                            "name": "/dev/disk/by-id/ata-Samsung_SSD_860_EVO_1TB_S3Z8NB0K934154M",
                            "config": {},
                        },
                        {
                            "name": "/dev/disk/by-id/ata-Samsung_SSD_860_EVO_1TB_S3Z8NB0K934284J",
                            "config": {},
                        },
                        {
                            "name": "/dev/disk/by-id/ata-Samsung_SSD_860_EVO_1TB_S3Z8NB0K934288X",
                            "config": {},
                        },
                        {
                            "name": "/dev/disk/by-id/ata-Samsung_SSD_860_EVO_1TB_S3Z8NB0K937582P",
                            "config": {},
                        },
                        {
                            "name": "/dev/disk/by-id/ata-Samsung_SSD_860_EVO_1TB_S3Z8NB0K943700W",
                            "config": {},
                        },
                        {
                            "name": "/dev/disk/by-id/ata-Samsung_SSD_860_EVO_1TB_S3Z8NB0K944017K",
                            "config": {},
                        },
                    ],
                },
            ],
        },
    },
}
storageclass_yaml = [
    {
        "apiVersion": "ceph.rook.io/v1",
        "kind": "CephBlockPool",
        "metadata": {"name": "replicapool", "namespace": "rook"},
        "spec": {
            "failureDomain": "host",
            "replicated": {"size": 2, "requireSafeReplicaSize": True},
        },
    },
    {
        "apiVersion": "storage.k8s.io/v1",
        "kind": "StorageClass",
        "metadata": {
            "name": "rook-ceph-block",
            "annotations": {"storageclass.kubernetes.io/is-default-class": "true"},
        },
        "provisioner": "rook.rbd.csi.ceph.com",
        "parameters": {
            "clusterID": "rook",
            "pool": "replicapool",
            "imageFormat": "2",
            "imageFeatures": "layering",
            "csi.storage.k8s.io/provisioner-secret-name": "rook-csi-rbd-provisioner",
            "csi.storage.k8s.io/provisioner-secret-namespace": "rook",
            "csi.storage.k8s.io/controller-expand-secret-name": "rook-csi-rbd-provisioner",
            "csi.storage.k8s.io/controller-expand-secret-namespace": "rook",
            "csi.storage.k8s.io/node-stage-secret-name": "rook-csi-rbd-node",
            "csi.storage.k8s.io/node-stage-secret-namespace": "rook",
            "csi.storage.k8s.io/fstype": "ext4",
        },
        "allowVolumeExpansion": True,
        "reclaimPolicy": "Delete",
    },
]


def objects():
    yield from (
        helm.build_chart_from_versions(
            name="rook",
            versions=versions,
            values=values,
        )
        + [ceph_yaml]
        + storageclass_yaml
    )
