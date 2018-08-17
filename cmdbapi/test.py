from cmdb.models.Cluster import Cluster
from cmdbapi.serializers import ClusterSerializer

cluster = Cluster.objects.all()
serializer = ClusterSerializer(instance=cluster[0])
print(serializer.data)