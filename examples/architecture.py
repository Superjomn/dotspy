import os
import sys

# Ensure dotspy is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotspy import Edge, EdgeStyle, Graph, GraphStyle, Node, NodeStyle, Subgraph


def generate_graph():
    with Graph(
        "Architecture", rankdir="TB", fontname="Helvetica", nodesep=0.5, ranksep=0.8
    ) as g:

        with NodeStyle(shape="box", style="filled", fillcolor="white"):

            # cluster_driver
            with Subgraph(
                "cluster_driver",
                label="Driver Node (CPU/Head)",
                styles=GraphStyle(style="filled"),
                fillcolor="#e1f5fe",
            ) as s_driver:
                trainer = Node(
                    "Trainer",
                    label="RayPPOTrainer\n(Controller)",
                    shape="component",
                    fillcolor="#b3e5fc",
                )
                res_manager = Node("ResourceManager", label="ResourcePoolManager")

                Edge(trainer, res_manager, label="allocates")

            # cluster_cluster
            with Subgraph(
                "cluster_cluster",
                label="Ray Cluster (GPU Nodes)",
                styles=GraphStyle(style="filled"),
                fillcolor="#f3e5f5",
            ) as s_cluster:

                # cluster_pool1
                with Subgraph(
                    "cluster_pool1",
                    label="Resource Pool A (e.g. 4 GPUs)",
                    styles=GraphStyle(style="dashed"),
                    color="#7b1fa2",
                ) as s_pool1:
                    wg1 = Node(
                        "WorkerGroup1",
                        label="ActorRolloutRef\nWorkerGroup",
                        shape="folder",
                        fillcolor="#e1bee7",
                    )

                    with NodeStyle(shape="ellipse", fillcolor="#f8bbd0"):
                        w1_actor = Node("W1_Actor", label="Actor\n(FSDP/Megatron)")
                        w1_rollout = Node("W1_Rollout", label="Rollout\n(vLLM/SGLang)")
                        w1_ref = Node("W1_Ref", label="RefPolicy")

                    Edge(wg1, w1_actor)
                    Edge(wg1, w1_rollout)
                    Edge(wg1, w1_ref)

                    # rank=same
                    # Creating dummy nodes with same names to reference them in rank=same subgraph
                    # NOTE: In graphviz, referring to node by name works.
                    # In dotspy, creating a Node registers it.
                    # If we create Node("W1_Actor") again inside this subgraph, it will be added to this subgraph.
                    # {rank=same; A; B} is a subgraph.
                    # We want: subgraph { rank=same; W1_Actor; ... }
                    with Subgraph(rank="same", cluster=False):
                        # We just need to ensure these nodes are outputted here.
                        # If we re-create them without attrs, they are just references.
                        Node("W1_Actor")
                        Node("W1_Rollout")
                        Node("W1_Ref")

                # cluster_pool2
                with Subgraph(
                    "cluster_pool2",
                    label="Resource Pool B (e.g. 2 GPUs)",
                    styles=GraphStyle(style="dashed"),
                    color="#7b1fa2",
                ) as s_pool2:
                    wg2 = Node(
                        "WorkerGroup2",
                        label="Critic\nWorkerGroup",
                        shape="folder",
                        fillcolor="#e1bee7",
                    )
                    w2_critic = Node(
                        "W2_Critic",
                        label="Critic Model",
                        shape="ellipse",
                        fillcolor="#f8bbd0",
                    )

                    Edge(wg2, w2_critic)

                # cluster_pool3
                with Subgraph(
                    "cluster_pool3",
                    label="Resource Pool C (Optional)",
                    styles=GraphStyle(style="dashed"),
                    color="#7b1fa2",
                ) as s_pool3:
                    wg3 = Node(
                        "WorkerGroup3",
                        label="RewardModel\nWorkerGroup",
                        shape="folder",
                        fillcolor="#e1bee7",
                    )
                    w3_rm = Node(
                        "W3_RM",
                        label="Reward Model",
                        shape="ellipse",
                        fillcolor="#f8bbd0",
                    )

                    Edge(wg3, w3_rm)

            # Main graph edges (RPC)
            Edge(trainer, wg1, label="RPC: update_actor(), generate()", color="blue")
            Edge(
                trainer,
                wg2,
                label="RPC: compute_values(), update_critic()",
                color="blue",
            )
            Edge(trainer, wg3, label="RPC: compute_reward()", color="blue")

            # Data flow annotations
            with EdgeStyle(color="#ef5350", style="dotted", fontsize=10):
                Edge(w1_rollout, trainer, label="DataProto\n(Prompts, Responses)")
                Edge(trainer, w3_rm, label="Prompts, Responses")
                Edge(w3_rm, trainer, label="Scores")
                Edge(trainer, w1_actor, label="Training Batch")

    return g


if __name__ == "__main__":
    g = generate_graph()
    output_path = os.path.join(os.path.dirname(__file__), "architecture_generated.dot")
    with open(output_path, "w") as f:
        f.write(g.to_dot())
    print(f"Generated {output_path}")
