import sys
import os

# Ensure dotspy is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotspy import Graph, Subgraph, Node, NodeStyle, Edge, EdgeStyle, GraphStyle

def generate_graph():
    with Graph("RolloutLogic", rankdir="TB") as g:
    
        with NodeStyle(shape="box", style="filled", fillcolor="white", fontname="Helvetica"):
            
            # cluster_vllm
            with Subgraph("cluster_vllm", label="vLLM Rollout (In-Process / Coupled)", 
                          style=GraphStyle(style="filled"), fillcolor="#e3f2fd") as s_vllm:
                
                v_rayworker = Node("V_RayWorker", label="Ray Worker Process\n(Hybrid Engine)", fillcolor="#bbdefb")
                
                with Subgraph("cluster_vllm_proc", label="Worker Process Memory", 
                              style=GraphStyle(style="dashed"), color="#1565c0") as s_vllm_proc:
                    
                    v_engine = Node("V_Engine", label="vLLM Engine\n(WorkerWrapperBase)", fillcolor="#90caf9")
                    v_weights = Node("V_Weights", label="Model Weights\n(Shared GPU Mem)", shape="cylinder", fillcolor="#ffe0b2")
                    
                Edge(v_rayworker, v_engine, label="ZMQ (IPC/TCP)\nRequests", dir="both")
                Edge(v_engine, v_weights, label="Direct Access")
                
            # cluster_trtllm
            with Subgraph("cluster_trtllm", label="TRT-LLM Rollout (Client-Server)", 
                          style=GraphStyle(style="filled"), fillcolor="#f3e5f5") as s_trt:
                
                t_rayworker = Node("T_RayWorker", label="Ray Worker Process\n(Client)", fillcolor="#e1bee7")
                
                with Subgraph("cluster_trt_server", label="TRT-LLM Server Process\n(Separate Actor)", 
                              style=GraphStyle(style="dashed"), color="#7b1fa2", fillcolor="#f3e5f5") as s_trt_server:
                    
                    t_server = Node("T_Server", label="HTTP Server\n(OpenAIServer)", fillcolor="#ce93d8")
                    t_weights = Node("T_Weights", label="Engine Weights", shape="cylinder", fillcolor="#ffe0b2")
                    
                Edge(t_rayworker, t_server, label="HTTP (aiohttp)\nRequests", dir="both")
                Edge(t_rayworker, t_weights, label="CUDA IPC\n(Weight Refit)", style=EdgeStyle(style="dotted"), color="red")
                Edge(t_server, t_weights, label="Inference")
            
    return g

if __name__ == "__main__":
    g = generate_graph()
    output_path = os.path.join(os.path.dirname(__file__), "rollout_logic_generated.dot")
    with open(output_path, "w") as f:
        f.write(g.to_dot())
    print(f"Generated {output_path}")
