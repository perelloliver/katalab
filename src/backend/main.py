from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import os
from typing import List, Optional

from src.backend.builder import KataBuilder
from src.backend.models import CompanyInfo, EmployeeInfo, KataPlan

app = FastAPI()

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store
from src.backend.sessions import session_manager

class InitResponse(BaseModel):
    session_id: str
    company_info: CompanyInfo
    employee_info: EmployeeInfo
    plan: KataPlan

class PlanRequest(BaseModel):
    session_id: str
    feedback: Optional[str] = None
    n_tasks: Optional[int] = 1

class BuildRequest(BaseModel):
    session_id: str

@app.post("/api/init", response_model=InitResponse)
async def init_session(company_files: List[UploadFile], employee_files: List[UploadFile], n_tasks: int = 5):
    session_id = str(uuid.uuid4())
    
    # Read company files content
    company_docs = []
    for file in company_files:
        content = await file.read()
        try:
            # Try decoding as utf-8
            text = content.decode("utf-8")
            company_docs.append(text)
        except UnicodeDecodeError:
            # Skip non-text files for now or handle gracefully
            print(f"Skipping binary file {file.filename}")
            pass
    
    # Read employee files content
    employee_docs = []
    for file in employee_files:
        content = await file.read()
        try:
            # Try decoding as utf-8
            text = content.decode("utf-8")
            employee_docs.append(text)
        except UnicodeDecodeError:
            # Skip non-text files for now or handle gracefully
            print(f"Skipping binary file {file.filename}")
            pass
    
    if not company_docs:
        raise HTTPException(status_code=400, detail="No valid company text documents uploaded.")
    if not employee_docs:
        raise HTTPException(status_code=400, detail="No valid employee text documents uploaded.")

    # Initialize Builder
    builder = KataBuilder(docs=company_docs, employee_docs=employee_docs, output_dir=f"downloads/{session_id}", n_tasks=n_tasks)
    session_manager.save_session(session_id, builder)
    
    # Parse and Plan
    try:
        company_info = builder._parse_data()
        employee_info = builder._parse_employee_data()
        plan = builder._plan_repo()
        session_manager.save_session(session_id, builder) # Save state after planning
        return InitResponse(session_id=session_id, company_info=company_info, employee_info=employee_info, plan=plan)
    except Exception as e:
        print(f"Error in init_session: {e}")
        import traceback
        traceback.print_exc()
        # del sessions[session_id] # Don't need to explicitly delete, next save will overwrite or it just stays
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/plan")
async def update_plan(request: PlanRequest):
    builder = session_manager.get_session(request.session_id)
    if not builder:
        raise HTTPException(status_code=404, detail="Session not found")
    try:
        new_plan = builder._plan_repo(feedback=request.feedback)
        session_manager.save_session(request.session_id, builder) 
        return new_plan
    except Exception as e:
        print(f"Error in update_plan: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/build")
async def build_repo(request: BuildRequest):
    builder = session_manager.get_session(request.session_id)
    if not builder:
        raise HTTPException(status_code=404, detail="Session not found")
    
    def event_stream():
        try:
            for event in builder._build_repo():
                import json
                yield json.dumps(event) + "\n"
            
            # Save session at end
            session_manager.save_session(request.session_id, builder)
            
            # Create the ZIP file explicitly here after streaming
            builder._output_repo()
            
            # Yield final success event with url
            yield json.dumps({"type": "complete", "download_url": f"/api/download/{request.session_id}"}) + "\n"
        except Exception as e:
            print(f"Error in event_stream: {e}")
            import traceback
            traceback.print_exc()
            yield json.dumps({"type": "error", "message": str(e)}) + "\n"

    from fastapi.responses import StreamingResponse
    return StreamingResponse(event_stream(), media_type="application/x-ndjson")

@app.get("/api/download/{session_id}")
async def download_repo(session_id: str):
    builder = session_manager.get_session(session_id)
    if not builder:
        raise HTTPException(status_code=404, detail="Session not found")
    # Re-construct expected path
    zip_path = os.path.join(builder.output_dir, "kata_repo.zip")
    
    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="Build artifact not found")
        
    return FileResponse(zip_path, filename="kata_repo.zip")

# Serve logo and assets from fig directory
if os.path.exists("fig"):
    app.mount("/fig", StaticFiles(directory="fig"), name="fig")

# Serve frontend
# Check if src/frontend exists to avoid startup error
if os.path.exists("src/frontend"):
    app.mount("/", StaticFiles(directory="src/frontend", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
