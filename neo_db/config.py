from py2neo import Graph

graph = Graph(
    "http://localhost:11008",
    username="neo4j",
    password="123456"
)  # DataStructureKG
CA_LIST = {"一级概念": 0, "二级概念": 1, "三级概念": 2, "四级概念": 3, "五级概念": 4, "函数": 5, "重要程度": 6}
