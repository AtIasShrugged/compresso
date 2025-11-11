"""Page routes (SSR with Jinja2)."""
from fastapi import APIRouter, Request, Form, Response, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from loguru import logger

from ...config import settings
from ...infra.auth import session_manager
from ...infra.i18n import locale_manager
from ...infra.cache import redis_cache
from ...core.entities import SummaryOptions, SummaryMode, DetailLevel
from ..dependencies import get_summarize_usecase


router = APIRouter()
templates = Jinja2Templates(directory="app/web/templates")


def get_locale_from_request(request: Request) -> str:
    """Get locale from cookie or Accept-Language header."""
    # Try cookie first
    lang = request.cookies.get("lang")
    if lang and lang in settings.allowed_locales_list:
        return lang
    
    # Try Accept-Language header
    accept_lang = request.headers.get("Accept-Language", "")
    for locale in settings.allowed_locales_list:
        if locale in accept_lang:
            return locale
    
    return settings.app_locale_default


def get_translations(request: Request) -> dict:
    """Get translations for current locale."""
    locale = get_locale_from_request(request)
    # Create translation function
    def _(key: str) -> str:
        return locale_manager.get(key, locale)
    
    return {"_": _, "locale": locale}


def require_auth(request: Request) -> str:
    """Check authentication and return username."""
    session_token = request.cookies.get(settings.session_cookie_name)
    if not session_token:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    
    username = session_manager.validate_session(session_token)
    if not username:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    
    return username


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page."""
    context = {
        "request": request,
        **get_translations(request)
    }
    return templates.TemplateResponse("login.html", context)


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    """Handle login."""
    if session_manager.verify_credentials(username, password):
        # Create session
        session_token = session_manager.create_session(username)
        
        # Redirect to main page with session cookie
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(
            key=settings.session_cookie_name,
            value=session_token,
            max_age=settings.session_max_age,
            httponly=True,
            secure=settings.is_prod,
            samesite="lax"
        )
        
        logger.info(f"User logged in: {username}")
        return response
    else:
        # Return to login with error
        logger.warning(f"Failed login attempt for user: {username}")
        context = {
            "request": request,
            "error": True,
            **get_translations(request)
        }
        return templates.TemplateResponse("login.html", context, status_code=401)


@router.post("/logout")
async def logout():
    """Handle logout."""
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(settings.session_cookie_name)
    return response


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main page."""
    username = require_auth(request)
    
    context = {
        "request": request,
        "username": username,
        **get_translations(request)
    }
    return templates.TemplateResponse("index.html", context)


@router.post("/summarize")
async def summarize(
    request: Request,
    mode: str = Form(...),
    input_data: str = Form(...),
    detail: str = Form(...)
):
    """Handle summarization request."""
    require_auth(request)
    
    try:
        # Always use gpt-4o-mini
        model = "openai:gpt-4o-mini"
        
        # Parse options
        options = SummaryOptions(
            mode=SummaryMode(mode),
            detail=DetailLevel(detail),
            model=model,
            locale=get_locale_from_request(request)
        )
        
        # Execute summarization
        usecase = get_summarize_usecase(model)
        result = await usecase.execute(input_data, options)
        
        logger.info(f"Summarization completed: {result.id}")
        
        # Render result page
        context = {
            "request": request,
            "result": result,
            **get_translations(request)
        }
        return templates.TemplateResponse("result.html", context)
        
    except Exception as e:
        logger.error(f"Summarization error: {e}")
        context = {
            "request": request,
            "error": str(e),
            **get_translations(request)
        }
        return templates.TemplateResponse("error.html", context, status_code=500)


@router.get("/history", response_class=HTMLResponse)
async def history(request: Request):
    """History page."""
    require_auth(request)
    
    # Get recent summaries
    recent = await redis_cache.list_recent(settings.cache_max_items)
    
    context = {
        "request": request,
        "summaries": recent,
        **get_translations(request)
    }
    return templates.TemplateResponse("history.html", context)


@router.get("/summary/{summary_id}", response_class=HTMLResponse)
async def view_summary(request: Request, summary_id: str):
    """View a specific summary by ID."""
    require_auth(request)
    
    # Get summary from cache
    result = await redis_cache.get(summary_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Summary not found")
    
    context = {
        "request": request,
        "result": result,
        **get_translations(request)
    }
    return templates.TemplateResponse("result.html", context)


@router.get("/api/healthz")
async def healthz():
    """Health check endpoint for Render."""
    return {"status": "ok"}
