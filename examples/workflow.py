import sys
import os

# Ensure dotspy is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotspy import Graph, Subgraph, Node, NodeStyle, Edge, GraphStyle

def generate_graph():
    # Create the main graph context
    with Graph("Workflow", rankdir="TD") as g:
        
        # Global node style
        with NodeStyle(shape="rect", style="filled", fillcolor="white", fontname="Helvetica"):
            
            # Start node
            start = Node("start", label="Start Epoch", shape="oval", fillcolor="#c8e6c9")
            
            # Phase 1: Rollout & Data Collection
            with Subgraph("cluster_rollout", label="Phase 1: Rollout & Data Collection", 
                        styles=GraphStyle(style="filled"), fillcolor="#fff9c4") as s1:
                gen = Node("gen", label="Generate Sequences\n(ActorRolloutWG.generate_sequences)", fillcolor="#fff59d")
                compute_log_probs = Node("compute_log_probs", label="Compute Old Log Probs\n(ActorWG)", fillcolor="#fff59d")
                compute_ref = Node("compute_ref", label="Compute Ref Log Probs\n(RefPolicyWG)", fillcolor="#fff59d")
                compute_values = Node("compute_values", label="Compute Values\n(CriticWG)", fillcolor="#fff59d")
                compute_rewards = Node("compute_rewards", label="Compute Rewards\n(RewardModelWG / Fn)", fillcolor="#fff59d")
                
                Edge(gen, compute_log_probs)
                Edge(gen, compute_ref)
                Edge(gen, compute_values)
                Edge(gen, compute_rewards)
                
            # Phase 2: Driver Calculation
            with Subgraph("cluster_driver_calc", label="Phase 2: Driver Calculation", 
                        styles=GraphStyle(style="filled"), fillcolor="#e1f5fe") as s2:
                calc_adv = Node("calc_adv", label="Compute Advantages (GAE)\n(Driver)", fillcolor="#b3e5fc")
                make_batch = Node("make_batch", label="Construct Training Batch\n(Driver)", fillcolor="#b3e5fc")
                
            # Phase 3: Model Updates
            with Subgraph("cluster_update", label="Phase 3: Model Updates", 
                        styles=GraphStyle(style="filled"), fillcolor="#ffccbc") as s3:
                update_actor = Node("update_actor", label="Update Actor\n(ActorWG.update_actor)", fillcolor="#ffab91")
                update_critic = Node("update_critic", label="Update Critic\n(CriticWG.update_critic)", fillcolor="#ffab91")
                
            # End node
            end = Node("end", label="Next Step / Finish", shape="oval", fillcolor="#c8e6c9")
            
            # Connect the phases
            Edge(start, gen)
            
            Edge(compute_log_probs, calc_adv)
            Edge(compute_ref, calc_adv)
            Edge(compute_values, calc_adv)
            Edge(compute_rewards, calc_adv)
            
            Edge(calc_adv, make_batch)
            Edge(make_batch, update_actor)
            Edge(make_batch, update_critic)
            
            Edge(update_actor, end)
            Edge(update_critic, end)
            
    return g

if __name__ == "__main__":
    g = generate_graph()
    output_path = os.path.join(os.path.dirname(__file__), "workflow_generated.dot")
    with open(output_path, "w") as f:
        f.write(g.to_dot())
    print(f"Generated {output_path}")
