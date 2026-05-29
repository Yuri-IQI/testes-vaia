"""
conftest.py (integração) — Fixture do modelo real.

Este conftest é específico para a pasta tests/integration/.
Ele tenta carregar o modelo de IA real (Qwen + adapter LoRA se disponível).

Se o modelo não puder ser carregado (sem memória, sem GPU, modelo não baixado),
todos os testes de integração são pulados automaticamente com uma mensagem clara —
em vez de falhar com um erro de import ou CUDA.

Isso permite que a suíte de testes unitários (tests/) continue rodando
normalmente em qualquer máquina, enquanto os testes de integração só
executam quando o ambiente está preparado.
"""

import os
import pytest
from pathlib import Path

from code_assistant import CodeAssistant
from generator.chart_pipeline import ChartPipeline


PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_MODEL  = os.getenv("BASE_MODEL",    "Qwen/Qwen2.5-0.5B-Instruct")
DEFAULT_ADAPTER = os.getenv("DEFAULT_ADAPTER", "financial_adapter")


def _try_load_pipeline() -> tuple[ChartPipeline | None, str]:
    """
    Tenta instanciar e carregar o pipeline com o modelo real.
    Retorna (pipeline, "") em caso de sucesso ou (None, mensagem_de_erro).
    """
    try:
        # Tenta carregar com o adapter LoRA se ele existir
        adapter_path = PROJECT_DIR / DEFAULT_ADAPTER
        adapter_exists = adapter_path.exists()

        if adapter_exists:
            # Importa aqui para não quebrar em ambientes sem peft instalado
            from peft import PeftModel
            from code_assistant import CodeAssistant as _Base

            class _FineTunedAssistant(_Base):
                def _ensure_loaded(self) -> None:
                    super()._ensure_loaded()
                    self._model = PeftModel.from_pretrained(self._model, str(adapter_path))
                    self._model = self._model.merge_and_unload()

            assistant = _FineTunedAssistant(model_name=DEFAULT_MODEL)
        else:
            assistant = CodeAssistant(model_name=DEFAULT_MODEL)

        # Força o carregamento agora para capturar erros cedo
        assistant._ensure_loaded()

        source = "modelo base" if not adapter_exists else f"modelo + adapter ({DEFAULT_ADAPTER})"
        return ChartPipeline(assistant=assistant), source

    except Exception as exc:
        return None, str(exc)


# Carrega uma vez por sessão de testes — modelos são pesados
_PIPELINE_CACHE: ChartPipeline | None = None
_LOAD_ERROR: str = ""
_LOAD_SOURCE: str = ""

def _get_cached_pipeline():
    global _PIPELINE_CACHE, _LOAD_ERROR, _LOAD_SOURCE
    if _PIPELINE_CACHE is None and not _LOAD_ERROR:
        _PIPELINE_CACHE, result = _try_load_pipeline()
        if _PIPELINE_CACHE is None:
            _LOAD_ERROR = result
        else:
            _LOAD_SOURCE = result
    return _PIPELINE_CACHE, _LOAD_ERROR, _LOAD_SOURCE


@pytest.fixture(scope="session")
def real_pipeline() -> ChartPipeline:
    """
    Fixture de sessão: carrega o modelo real UMA vez e reutiliza em todos
    os testes de integração. Se não conseguir carregar, pula o teste.
    """
    pipeline, error, source = _get_cached_pipeline()

    if pipeline is None:
        pytest.skip(
            f"Modelo não disponível — testes de integração pulados.\n"
            f"Motivo: {error}\n"
            f"Execute 'python train.py' para gerar o adapter e tente novamente."
        )

    print(f"\n[integração] Usando: {source}")
    return pipeline


@pytest.fixture(scope="session")
def real_pipeline_source() -> str:
    """Retorna de onde o modelo foi carregado (base ou com adapter)."""
    _, _, source = _get_cached_pipeline()
    return source
