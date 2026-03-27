
from fastapi import APIRouter
router=APIRouter()
metrics={"requests":0}

@router.get("/metrics")
def m(): return metrics
