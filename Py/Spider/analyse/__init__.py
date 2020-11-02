# encoding: utf-8

from .compute import _DEFAULT_LIMIT, ComputeMean, ComputeBaseInfo
from sqlalchemy.engine import Engine


def compute(engine: Engine, limit: int = _DEFAULT_LIMIT, /) -> None:
    ComputeMean(engine, limit).compute_means()
    ComputeBaseInfo(engine).compute()