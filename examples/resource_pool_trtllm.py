import sys
import os

# Ensure dotspy is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotspy import Graph, Subgraph, Node, NodeStyle, Edge, EdgeStyle, GraphStyle

def generate_graph():
    with Graph("ResourcePoolManager_TRTLLM", rankdir="TB", compound="true",
              label="ResourcePoolManager: TRT-LLM Allocation\n1 Node, 8 GPUs, TP=4 (2 Replicas)",
              labelloc="t", fontsize=16, fontname="Arial Bold") as g:
    
        with NodeStyle(shape="box", style="filled", fontname="Arial"):
            
            # cluster_manager
            with Subgraph("cluster_manager", label="ResourcePoolManager", color="blue", 
                          style=GraphStyle(style="filled"), fillcolor="#e3f2fd") as s_manager:
                rpm = Node("RPM", label="ResourcePoolManager\n\nresource_pool_spec:\n{'global_pool': (max_colocate_count=3,\n  [8])}\n\nmapping:\n{ActorRollout: 'global_pool'\n Critic: 'global_pool'}",
                           shape="box", fillcolor="#bbdefb", style="filled,rounded")
                
            # cluster_pool
            with Subgraph("cluster_pool", label="RayResourcePool ('global_pool')", color="darkgreen",
                          style=GraphStyle(style="filled"), fillcolor="#e8f5e9") as s_pool:
                rrp = Node("RRP", label="RayResourcePool\n\nprocess_on_nodes: [8]\nmax_colocate_count: 3\nuse_gpu: True",
                           shape="box", fillcolor="#c8e6c9", style="filled,rounded")
                
            # cluster_pg
            with Subgraph("cluster_pg", label="Ray Placement Group (STRICT_PACK)\nNode: ray-node-1",
                          color="purple", style=GraphStyle(style="filled"), fillcolor="#f3e5f5") as s_pg:
                pg = Node("PG", label="PlacementGroup\n\nBundles (8 total):\nEach: {CPU: 3, GPU: 1}\n\nStrategy: STRICT_PACK",
                          shape="box", fillcolor="#e1bee7", style="filled,rounded")
                
            # cluster_gpus
            with Subgraph("cluster_gpus", label="Physical Node (8 GPUs)", color="black",
                          style=GraphStyle(style="filled"), fillcolor="#fff9c4") as s_gpus:
                
                # cluster_replica0
                with Subgraph("cluster_replica0", label="Replica 0 (TP=4)", style=GraphStyle(style="dashed"), color="red") as s_rep0:
                    gpu0 = Node("GPU0", label="GPU 0\nBundle 0", fillcolor="#ffeb3b")
                    gpu1 = Node("GPU1", label="GPU 1\nBundle 1", fillcolor="#ffeb3b")
                    gpu2 = Node("GPU2", label="GPU 2\nBundle 2", fillcolor="#ffeb3b")
                    gpu3 = Node("GPU3", label="GPU 3\nBundle 3", fillcolor="#ffeb3b")
                    
                # cluster_replica1
                with Subgraph("cluster_replica1", label="Replica 1 (TP=4)", style=GraphStyle(style="dashed"), color="red") as s_rep1:
                    gpu4 = Node("GPU4", label="GPU 4\nBundle 4", fillcolor="#ffeb3b")
                    gpu5 = Node("GPU5", label="GPU 5\nBundle 5", fillcolor="#ffeb3b")
                    gpu6 = Node("GPU6", label="GPU 6\nBundle 6", fillcolor="#ffeb3b")
                    gpu7 = Node("GPU7", label="GPU 7\nBundle 7", fillcolor="#ffeb3b")
                    
            # Worker Allocation - Replica 0
            with Subgraph("cluster_workers_r0", label="Worker Group & TRT-LLM Server - Replica 0",
                          color="darkblue", style=GraphStyle(style="filled"), fillcolor="#e1f5fe") as s_work_r0:
                
                with Subgraph("cluster_hybrid_r0", label="HybridEngine Workers (Colocate Slot 0)",
                              style=GraphStyle(style="dashed"), color="green") as s_hybrid_r0:
                    aw0 = Node("AW0", label="ActorRolloutRefWorker\nRank 0\n(Training Engine)", fillcolor="#b3e5fc", shape="component")
                    aw1 = Node("AW1", label="ActorRolloutRefWorker\nRank 1\n(Training Engine)", fillcolor="#b3e5fc", shape="component")
                    aw2 = Node("AW2", label="ActorRolloutRefWorker\nRank 2\n(Training Engine)", fillcolor="#b3e5fc", shape="component")
                    aw3 = Node("AW3", label="ActorRolloutRefWorker\nRank 3\n(Training Engine)", fillcolor="#b3e5fc", shape="component")
                    
                trtllm0 = Node("TRTLLM0", label="TRTLLMHttpServer\n(Ray Actor)\nReplica 0\n\nTP=4 via TRT-LLM's\ninternal orchestration",
                               fillcolor="#4fc3f7", shape="box3d", style="filled")
                
            # Worker Allocation - Replica 1
            with Subgraph("cluster_workers_r1", label="Worker Group & TRT-LLM Server - Replica 1",
                          color="darkblue", style=GraphStyle(style="filled"), fillcolor="#e1f5fe") as s_work_r1:
                
                with Subgraph("cluster_hybrid_r1", label="HybridEngine Workers (Colocate Slot 0)",
                              style=GraphStyle(style="dashed"), color="green") as s_hybrid_r1:
                    aw4 = Node("AW4", label="ActorRolloutRefWorker\nRank 4\n(Training Engine)", fillcolor="#b3e5fc", shape="component")
                    aw5 = Node("AW5", label="ActorRolloutRefWorker\nRank 5\n(Training Engine)", fillcolor="#b3e5fc", shape="component")
                    aw6 = Node("AW6", label="ActorRolloutRefWorker\nRank 6\n(Training Engine)", fillcolor="#b3e5fc", shape="component")
                    aw7 = Node("AW7", label="ActorRolloutRefWorker\nRank 7\n(Training Engine)", fillcolor="#b3e5fc", shape="component")
                    
                trtllm1 = Node("TRTLLM1", label="TRTLLMHttpServer\n(Ray Actor)\nReplica 1\n\nTP=4 via TRT-LLM's\ninternal orchestration",
                               fillcolor="#4fc3f7", shape="box3d", style="filled")
                
            # Client Adapters
            with Subgraph("cluster_adapters", label="TRT-LLM Client Adapters (in each worker)",
                          color="orange", style=GraphStyle(style="filled"), fillcolor="#fff3e0") as s_adapters:
                adapter0 = Node("ADAPTER0", label="TRTLLMAsyncRollout\n(HTTP Client)\nReplica 0", fillcolor="#ffe0b2", shape="note")
                adapter1 = Node("ADAPTER1", label="TRTLLMAsyncRollout\n(HTTP Client)\nReplica 1", fillcolor="#ffe0b2", shape="note")
                
            # Define styles
            invis_style = EdgeStyle(style="invis")
            dotted_style = EdgeStyle(style="dotted", color="black", label="schedules")
            bold_red_style = EdgeStyle(style="bold", color="red", penwidth=2)
            http_style = EdgeStyle(style="bold", color="orange", penwidth=2, label="HTTP\nRequests")
            weight_sync_style = EdgeStyle(style="dashed", color="green", penwidth=2, label="CUDA IPC\nWeight Sync", constraint="false")
            embed_style = EdgeStyle(color="darkgreen", dir="none", penwidth=2, label="embeds")
            
            # Connections - Management Flow
            rpm >> rrp | {"label": "creates", "color": "blue", "penwidth": 2}
            rrp >> pg | {"label": "creates\nPlacement Group", "color": "darkgreen", "penwidth": 2}
            pg >> gpu0 | {"label": "binds", "color": "purple", "style": "dashed", "lhead": "cluster_gpus"}
            
            # Connections - GPU Assignment Replica 0
            gpu0 >> aw0 | dotted_style
            gpu1 >> aw1 | dotted_style
            gpu2 >> aw2 | dotted_style
            gpu3 >> aw3 | dotted_style
            
            gpu0 >> trtllm0 | bold_red_style | {"label": "uses Bundle 0-3"}
            gpu1 >> trtllm0 | invis_style
            gpu2 >> trtllm0 | invis_style
            gpu3 >> trtllm0 | invis_style
            
            # Connections - GPU Assignment Replica 1
            gpu4 >> aw4 | dotted_style
            gpu5 >> aw5 | dotted_style
            gpu6 >> aw6 | dotted_style
            gpu7 >> aw7 | dotted_style
            
            gpu4 >> trtllm1 | bold_red_style | {"label": "uses Bundle 4-7"}
            gpu5 >> trtllm1 | invis_style
            gpu6 >> trtllm1 | invis_style
            gpu7 >> trtllm1 | invis_style
            
            # Connections - Communication
            aw0 >> adapter0 | embed_style
            aw1 >> adapter0 | invis_style
            aw2 >> adapter0 | invis_style
            aw3 >> adapter0 | invis_style
            
            aw4 >> adapter1 | embed_style
            aw5 >> adapter1 | invis_style
            aw6 >> adapter1 | invis_style
            aw7 >> adapter1 | invis_style
            
            adapter0 >> trtllm0 | http_style
            adapter1 >> trtllm1 | http_style
            
            # Weight Sync
            aw0 >> trtllm0 | weight_sync_style
            aw4 >> trtllm1 | weight_sync_style
            
            # Legend
            with Subgraph("cluster_legend", label="Legend", color="gray", 
                          style=GraphStyle(style="filled"), fillcolor="white") as s_legend:
                l1 = Node("L1", label="Blue: Resource Management", fillcolor="#e3f2fd", shape="box")
                l2 = Node("L2", label="Red: TP Group Boundaries", fillcolor="white", shape="box", style="dashed", color="red")
                l3 = Node("L3", label="Orange: HTTP Communication", fillcolor="white", shape="box")
                l4 = Node("L4", label="Green: Weight Sync (CUDA IPC)", fillcolor="white", shape="box")
                
                l1 >> l2 >> l3 >> l4 | invis_style
                
            # Layout hints
            with Subgraph(rank="same", cluster=False):
                Node("GPU0"); Node("GPU1"); Node("GPU2"); Node("GPU3"); Node("GPU4"); Node("GPU5"); Node("GPU6"); Node("GPU7")
                
            with Subgraph(rank="same", cluster=False):
                Node("TRTLLM0"); Node("TRTLLM1")
                
            with Subgraph(rank="same", cluster=False):
                Node("ADAPTER0"); Node("ADAPTER1")
            
    return g

if __name__ == "__main__":
    g = generate_graph()
    output_path = os.path.join(os.path.dirname(__file__), "resource_pool_trtllm_generated.dot")
    with open(output_path, "w") as f:
        f.write(g.to_dot())
    print(f"Generated {output_path}")
