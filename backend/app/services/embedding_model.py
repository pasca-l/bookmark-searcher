from enum import Enum

import torch
from transformers import AutoModel, AutoTokenizer


class EmbeddingModelName(str, Enum):
    ALL_MINILM_L6_V2 = "sentence-transformers/all-MiniLM-L6-v2"  # 384 dim
    # ALL_MPNET_BASE_V2 = "sentence-transformers/all-mpnet-base-v2" # 768 dim
    MULTILINGUAL_E5_SMALL = "intfloat/multilingual-e5-small"  # 384 dim


class EmbeddingModel:
    def __init__(
        self,
        model_name: EmbeddingModelName = EmbeddingModelName.ALL_MINILM_L6_V2,
        device: str | None = None,
    ):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name.value)
        self.model = AutoModel.from_pretrained(model_name.value)

        if device is None:
            if torch.cuda.is_available():
                device = "cuda"
            elif torch.backends.mps.is_available():
                device = "mps"
            else:
                device = "cpu"

        self.device = torch.device(device)
        self.model.to(self.device)
        self.model.eval()

    # take attention mask into account for correct averaging
    def mean_pooling(
        self, model_output: torch.Tensor, attention_mask: torch.Tensor
    ) -> torch.Tensor:
        # first element of model_output contains all token embeddings
        embeddings = model_output[0]

        mask = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
        return torch.sum(embeddings * mask, 1) / torch.clamp(mask.sum(1), min=1e-9)

    @torch.no_grad()
    def encode(self, texts: list[str]) -> list[list[float]]:
        encoded = self.tokenizer(
            texts, padding=True, truncation=True, return_tensors="pt"
        )
        encoded = {k: v.to(self.device) for k, v in encoded.items()}

        out = self.model(**encoded)
        embeddings = self.mean_pooling(out, encoded["attention_mask"])
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

        return embeddings.cpu().numpy().tolist()

    @property
    def embedding_dim(self) -> int:
        return self.model.config.hidden_size


def new_embedding_model() -> EmbeddingModel:
    return EmbeddingModel()
