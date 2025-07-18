# ✅ IMPLEMENTED: Phase 1 - FastAPI server setup
# 🔗 PLAN REF: Implementation Plan -> Phase 1 -> FastAPI setup

"""
Reddit Scout API - FastAPI server with single endpoint architecture
Provides N8N compatible tools for Reddit data extraction
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Reddit Scout API",
    description="N8N compatible agentic tools for Reddit data extraction",
    version="0.1.0"
)

# 🔄 IN PROGRESS: Adding request/response models
class ToolRequest(BaseModel):
    """Request model for tool execution"""
    tool: str = Field(..., description="Tool name to execute")
    parameters: Dict[str, Any] = Field(..., description="Tool parameters")

class ToolResponse(BaseModel):
    """Response model for tool execution"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any]

# 📋 TODO: Implement tool routing system
AVAILABLE_TOOLS = {
    "view_subreddit": "Extract subreddit feeds with engagement metrics",
    "analyze_user": "Get user activity patterns and influence metrics", 
    "search_content": "Search Reddit with advanced filters",
    "extract_thread": "Get complete thread data with comment hierarchy",
    "scan_user_batch": "Analyze multiple users for comparison"
}

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway deployment"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Reddit Scout API",
        "version": "0.1.0",
        "available_tools": list(AVAILABLE_TOOLS.keys()),
        "endpoints": {
            "POST /api": "Execute any tool",
            "GET /health": "Health check", 
            "GET /docs": "API documentation"
        }
    }

@app.post("/api", response_model=ToolResponse)
async def execute_tool(request: ToolRequest):
    """
    Single endpoint for all tool execution
    🔗 PLAN REF: Implementation Plan -> Single endpoint architecture
    """
    start_time = time.time()
    
    try:
        # Validate tool exists
        if request.tool not in AVAILABLE_TOOLS:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown tool: {request.tool}. Available tools: {list(AVAILABLE_TOOLS.keys())}"
            )
        
        # 📋 TODO: Route to actual tool implementations
        # For now, return mock response
        result_data = {
            "tool": request.tool,
            "parameters": request.parameters,
            "message": f"Tool {request.tool} executed successfully (mock response)",
            "description": AVAILABLE_TOOLS[request.tool]
        }
        
        execution_time = time.time() - start_time
        
        return ToolResponse(
            success=True,
            data=result_data,
            metadata={
                "execution_time": round(execution_time, 3),
                "cached": False,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Tool execution error: {str(e)}")
        
        return ToolResponse(
            success=False,
            error={
                "type": type(e).__name__,
                "message": str(e),
                "details": {}
            },
            metadata={
                "execution_time": round(execution_time, 3),
                "timestamp": datetime.utcnow().isoformat()
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)