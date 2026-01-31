import torch
import math
from torch import Tensor

def sparse_mincut_pool_batch(
    x: Tensor,
    edge_index: Tensor,
    s: Tensor,
    batch: Tensor,
    edge_weight: Tensor = None,
    temp: float = 1.0,
    mask: Tensor = None,
    normalize: bool = True
) -> (Tensor, Tensor, Tensor, Tensor):
    """
    Batch-wise sparse MinCut pooling, refined to avoid inplace ops and reduce complexity.

    Returns:
        pooled_x: [B, C, F]
        pooled_adj: [B, C, C]
        mincut_loss: scalar
        ortho_loss: scalar
    """
    device = x.device
    N, F_in = x.size()
    C = s.size(-1)
    B = int(batch.max().item()) + 1

    # default edge_weight
    if edge_weight is None:
        edge_weight = torch.ones(edge_index.size(1), device=device, dtype=x.dtype)

    # soft assignment
    s = torch.softmax((s / temp) if temp != 1.0 else s, dim=-1)

    # optional node mask
    if mask is not None:
        x = x * mask.unsqueeze(-1)
        s = s * mask.unsqueeze(-1)

    # init outputs
    pooled_x = torch.zeros(B, C, F_in, device=device, dtype=x.dtype)
    pooled_adj = torch.zeros(B, C, C, device=device, dtype=x.dtype)
    mincut_losses = []
    ortho_losses = []

    # process each graph in batch
    for b in range(B):
        mask_b = (batch == b)
        x_b = x[mask_b]
        s_b = s[mask_b]

        # extract edges for this graph
        ei = edge_index
        mask_e = mask_b[ei[0]] & mask_b[ei[1]]
        ei_b = ei[:, mask_e]
        ew_b = edge_weight[mask_e]

        # re-index nodes
        idx = mask_b.nonzero(as_tuple=False).view(-1)
        idx_map = -torch.ones(N, device=device, dtype=torch.long)
        idx_map[idx] = torch.arange(idx.size(0), device=device)
        ei_b = idx_map[ei_b]

        row, col = ei_b
        # compute A * s
        s_col = s_b[col]               # [E_b, C]
        weighted_s = s_col * ew_b.unsqueeze(-1)
        A_s = torch.zeros(x_b.size(0), C, device=device, dtype=x.dtype)
        A_s = A_s.index_add(0, row, weighted_s)
        adj_b = torch.mm(s_b.t(), A_s) # [C, C]

        pooled_adj[b] = adj_b
        pooled_x[b]   = torch.mm(s_b.t(), x_b)

        # MinCut loss
        num = torch.trace(adj_b)
        deg = torch.zeros(x_b.size(0), device=device, dtype=x.dtype)
        deg = deg.index_add(0, row, ew_b)
        den = torch.trace(torch.mm(s_b.t(), deg.view(-1,1) * s_b)) + 1e-10
        mincut_losses.append(-num / den)

        # Orthogonality loss
        ss = torch.mm(s_b.t(), s_b)
        norm_ss = torch.norm(ss, p='fro') + 1e-10
        ss_norm = ss / norm_ss
        I = torch.eye(C, device=device, dtype=x.dtype) / math.sqrt(C)
        ortho_losses.append(torch.norm(ss_norm - I, p='fro'))

    # normalize pooled_adj across batch
    if normalize:
        # zero diag
        I = torch.eye(C, device=device, dtype=torch.bool).unsqueeze(0)  # [1,C,C]
        pooled_adj = pooled_adj.masked_fill(I, 0.0)
        # degree
        EPS = 1e-15
        d = pooled_adj.sum(dim=2)           # [B, C]
        d_sqrt = torch.sqrt(d) + EPS
        pooled_adj = pooled_adj / d_sqrt.unsqueeze(2) / d_sqrt.unsqueeze(1)

    return (
        pooled_x,
        pooled_adj,
        torch.stack(mincut_losses).mean(),
        torch.stack(ortho_losses).mean()
    )



