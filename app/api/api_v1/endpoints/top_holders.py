from fastapi import APIRouter, Request, Form
from app.api.deps import template
from .holders_insights import TopHoldersInsights
from app.settings.core import core_settings

router = APIRouter()


@router.post("/top-holders")
async def fetch_data(request: Request, ca: str = Form(...)):
    n=10
    try:
        thi = TopHoldersInsights(core_settings.HELIUS_API_KEY, ca)
        token_info = thi.get_token_info()
        top_holders = thi.get_crypto_holders()
        top_holders_fungibles = thi.get_holder_fungibles(top_holders, n)

        for owner, tokens in top_holders_fungibles.items():
            total_price = sum(token[3] for token in tokens)
            top_holders_fungibles[owner] = {'tokens': tokens, 'total_price': round(total_price, 2)}

        return template(
            "top_holders.html",
            {"request": request,
             "token_info": token_info[0], 
             "top_holders_fungibles": top_holders_fungibles, 
             "n_elements": n, 
             "ca": ca},
        )
    
    except Exception as e:
        return template(
            "home.html",
            {"request": request, "error": str(e)},
        )
    