import sys
import os

# Ensure dotspy is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotspy import Graph, Subgraph, Node, NodeStyle, Edge, EdgeStyle, GraphStyle

def generate_graph():
    with Graph("ResourcePoolManager_TRTLLM_2Nodes", rankdir="TB", compound="true",
              label="ResourcePoolManager: TRT-LLM Allocation\n2 Nodes, 16 GPUs Total, TP=4 (4 Replicas)",
              labelloc="t", fontsize=16, fontname="Arial Bold") as g:
    
        with NodeStyle(shape="box", style="filled", fontname="Arial"):
            
            # ResourcePoolManager
            with Subgraph("cluster_manager", label="ResourcePoolManager", color="blue", 
                          style=GraphStyle(style="filled"), fillcolor="#e3f2fd") as s_manager:
                rpm = Node("RPM", label="ResourcePoolManager\n\nresource_pool_spec:\n{'global_pool': (max_colocate_count=3,\n  [8, 8])}\n\nmapping:\n{ActorRollout: 'global_pool'}",
                           shape="box", fillcolor="#bbdefb", style="filled,rounded")
                
            # RayResourcePool
            with Subgraph(label="RayResourcePool ('global_pool')", color="darkgreen",
                          style=GraphStyle(style="filled"), fillcolor="#e8f5e9") as s_pool:
                rrp = Node("RRP", label="RayResourcePool\n\nprocess_on_nodes: [8, 8]\nmax_colocate_count: 3\nuse_gpu: True\ntotal_gpus: 16",
                           shape="box", fillcolor="#c8e6c9", style="filled,rounded")
                
            # Ray Placement Groups
            with Subgraph("cluster_placement", label="Ray Placement Groups (STRICT_PACK)", 
                          color="purple", style=GraphStyle(style="filled"), fillcolor="#f3e5f5") as s_placement:
                pg0 = Node("PG0", label="PlacementGroup 0\nNode: ray-node-1\n8 Bundles", fillcolor="#e1bee7", style="filled,rounded")
                pg1 = Node("PG1", label="PlacementGroup 1\nNode: ray-node-2\n8 Bundles", fillcolor="#e1bee7", style="filled,rounded")
                
            # Physical Node 1
            with Subgraph("cluster_node1", label="Physical Node 1 (8 GPUs)", color="black",
                          style=GraphStyle(style="filled"), fillcolor="#fff9c4") as s_node1:
                
                gpu_style = NodeStyle(fillcolor="#ffeb3b")

                with Subgraph("cluster_node1_replica0", label="Replica 0 (TP=4)", 
                                style=GraphStyle(style="dashed"), color="red") as s_n1_r0:
                    n1_gpu0 = Node("N1_GPU0", label="GPU 0\nBundle 0", nstyle=gpu_style)
                    n1_gpu1 = Node("N1_GPU1", label="GPU 1\nBundle 1", nstyle=gpu_style)
                    n1_gpu2 = Node("N1_GPU2", label="GPU 2\nBundle 2", nstyle=gpu_style)
                    n1_gpu3 = Node("N1_GPU3", label="GPU 3\nBundle 3", nstyle=gpu_style)
                        
                with Subgraph("cluster_node1_replica1", label="Replica 1 (TP=4)", 
                                style=GraphStyle(style="dashed"), color="red") as s_n1_r1:
                    n1_gpu4 = Node("N1_GPU4", label="GPU 4\nBundle 4", nstyle=gpu_style)
                    n1_gpu5 = Node("N1_GPU5", label="GPU 5\nBundle 5", nstyle=gpu_style)
                    n1_gpu6 = Node("N1_GPU6", label="GPU 6\nBundle 6", nstyle=gpu_style)
                    n1_gpu7 = Node("N1_GPU7", label="GPU 7\nBundle 7", nstyle=gpu_style)
                    
            # Physical Node 2
            with Subgraph("cluster_node2", label="Physical Node 2 (8 GPUs)", color="black",
                          style=GraphStyle(style="filled"), fillcolor="#e8f4f8") as s_node2:
                
                with Subgraph("cluster_node2_replica2", label="Replica 2 (TP=4)", 
                              style=GraphStyle(style="dashed"), color="red") as s_n2_r2:
                    n2_gpu0 = Node("N2_GPU0", label="GPU 8\nBundle 0", fillcolor="#b3e5fc")
                    n2_gpu1 = Node("N2_GPU1", label="GPU 9\nBundle 1", fillcolor="#b3e5fc")
                    n2_gpu2 = Node("N2_GPU2", label="GPU 10\nBundle 2", fillcolor="#b3e5fc")
                    n2_gpu3 = Node("N2_GPU3", label="GPU 11\nBundle 3", fillcolor="#b3e5fc")
                    
                with Subgraph("cluster_node2_replica3", label="Replica 3 (TP=4)", 
                              style=GraphStyle(style="dashed"), color="red") as s_n2_r3:
                    n2_gpu4 = Node("N2_GPU4", label="GPU 12\nBundle 4", fillcolor="#b3e5fc")
                    n2_gpu5 = Node("N2_GPU5", label="GPU 13\nBundle 5", fillcolor="#b3e5fc")
                    n2_gpu6 = Node("N2_GPU6", label="GPU 14\nBundle 6", fillcolor="#b3e5fc")
                    n2_gpu7 = Node("N2_GPU7", label="GPU 15\nBundle 7", fillcolor="#b3e5fc")
                    
            # Workers & Servers Node 1
            with Subgraph("cluster_workers_node1", label="Node 1: Workers & TRT-LLM Servers",
                          color="darkblue", style=GraphStyle(style="filled"), fillcolor="#e1f5fe") as s_workers_n1:
                n1_workers = Node("N1_Workers", label="ActorRolloutRefWorkers\nRank 0-7\n(8 Training Engines)",
                                  fillcolor="#81d4fa", shape="component")
                n1_server0 = Node("N1_Server0", label="TRTLLMHttpServer\nReplica 0\n(Bundles 0-3)",
                                  fillcolor="#4fc3f7", shape="box3d")
                n1_server1 = Node("N1_Server1", label="TRTLLMHttpServer\nReplica 1\n(Bundles 4-7)",
                                  fillcolor="#4fc3f7", shape="box3d")
                n1_adapter = Node("N1_Adapter", label="TRTLLMAsyncRollout\nClients (Rank 0-7)",
                                  fillcolor="#ffe0b2", shape="note")
                
            # Workers & Servers Node 2
            with Subgraph("cluster_workers_node2", label="Node 2: Workers & TRT-LLM Servers",
                          color="darkblue", style=GraphStyle(style="filled"), fillcolor="#f1f8e9") as s_workers_n2:
                n2_workers = Node("N2_Workers", label="ActorRolloutRefWorkers\nRank 8-15\n(8 Training Engines)",
                                  fillcolor="#aed581", shape="component")
                n2_server2 = Node("N2_Server2", label="TRTLLMHttpServer\nReplica 2\n(Bundles 0-3)",
                                  fillcolor="#9ccc65", shape="box3d")
                n2_server3 = Node("N2_Server3", label="TRTLLMHttpServer\nReplica 3\n(Bundles 4-7)",
                                  fillcolor="#9ccc65", shape="box3d")
                n2_adapter = Node("N2_Adapter", label="TRTLLMAsyncRollout\nClients (Rank 8-15)",
                                  fillcolor="#ffe0b2", shape="note")
                
            # Inter-node Communication
            nccl = Node("NCCL", label="NCCL All-Reduce\n(Cross-node gradient sync)", shape="cylinder", fillcolor="#fff59d", style="filled")
            
            # Connections - Management Flow
            rpm >> rrp | {"label": "creates", "color": "blue", "penwidth": 2}
            rrp >> pg0 | {"label": "creates PG", "color": "darkgreen", "penwidth": 2}
            rrp >> pg1 | {"label": "creates PG", "color": "darkgreen", "penwidth": 2}
            
            # Placement Group to Nodes
            Edge(pg0, n1_gpu0, label="binds", color="purple", style=EdgeStyle(style="dashed"), lhead="cluster_node1")
            Edge(pg1, n2_gpu0, label="binds", color="purple", style=EdgeStyle(style="dashed"), lhead="cluster_node2")
            
            # Workers to GPUs (Node 1)
            Edge(n1_gpu0, n1_workers, label="schedules", color="black", style=EdgeStyle(style="dotted"), ltail="cluster_node1")
            Edge(n1_gpu0, n1_server0, label="uses", color="red", style=EdgeStyle(style="bold"), penwidth=2, ltail="cluster_node1_replica0")
            Edge(n1_gpu4, n1_server1, label="uses", color="red", style=EdgeStyle(style="bold"), penwidth=2, ltail="cluster_node1_replica1")
            
            # Workers to GPUs (Node 2)
            Edge(n2_gpu0, n2_workers, label="schedules", color="black", style=EdgeStyle(style="dotted"), ltail="cluster_node2")
            Edge(n2_gpu0, n2_server2, label="uses", color="red", style=EdgeStyle(style="bold"), penwidth=2, ltail="cluster_node2_replica2")
            Edge(n2_gpu4, n2_server3, label="uses", color="red", style=EdgeStyle(style="bold"), penwidth=2, ltail="cluster_node2_replica3")
            
            # Communication flows
            n1_workers >> n1_adapter | {"label": "embeds", "color": "darkgreen", "dir": "none", "penwidth": 2}
            n2_workers >> n2_adapter | {"label": "embeds", "color": "darkgreen", "dir": "none", "penwidth": 2}
            
            n1_adapter >> n1_server0 | {"label": "HTTP", "color": "orange", "penwidth": 2}
            n1_adapter >> n1_server1 | {"label": "HTTP", "color": "orange", "penwidth": 2}
            n2_adapter >> n2_server2 | {"label": "HTTP", "color": "orange", "penwidth": 2}
            n2_adapter >> n2_server3 | {"label": "HTTP", "color": "orange", "penwidth": 2}
            
            # Weight sync
            Edge(n1_workers, n1_server0, label="CUDA IPC\nWeight Sync", color="green", penwidth=2, style=EdgeStyle(style="dashed"))
            Edge(n1_workers, n1_server1, label="CUDA IPC\nWeight Sync", color="green", penwidth=2, style=EdgeStyle(style="dashed"))
            Edge(n2_workers, n2_server2, label="CUDA IPC\nWeight Sync", color="green", penwidth=2, style=EdgeStyle(style="dashed"))
            Edge(n2_workers, n2_server3, label="CUDA IPC\nWeight Sync", color="green", penwidth=2, style=EdgeStyle(style="dashed"))
            
            # Cross-node communication
            Edge(n1_workers, nccl, color="brown", penwidth=2, style=EdgeStyle(style="bold"))
            Edge(n2_workers, nccl, color="brown", penwidth=2, style=EdgeStyle(style="bold"))
            
            # Legend
            with Subgraph("cluster_legend", label="Legend", color="gray", 
                          style=GraphStyle(style="filled"), fillcolor="white") as s_legend:
                l1 = Node("L1", label="Blue: Resource Management", fillcolor="#e3f2fd", shape="box")
                l2 = Node("L2", label="Red: TP Group (4 GPUs)", fillcolor="white", shape="box", style="dashed", color="red")
                l3 = Node("L3", label="Orange: HTTP Requests", fillcolor="white", shape="box")
                l4 = Node("L4", label="Green: Weight Sync (CUDA IPC)", fillcolor="white", shape="box")
                l5 = Node("L5", label="Brown: NCCL Cross-Node", fillcolor="white", shape="box")
                
                l1 >> l2 >> l3 >> l4 >> l5 | EdgeStyle(style="invis")
                
            # Layout hints
            with Subgraph(rank="same", cluster=False):
                Node("PG0"); Node("PG1")
                
            with Subgraph(rank="same", cluster=False):
                Node("N1_Server0"); Node("N1_Server1"); Node("N2_Server2"); Node("N2_Server3")
            
    return g

if __name__ == "__main__":
    g = generate_graph()
    g.render("resource_pool_trtllm_2nodes.png")
