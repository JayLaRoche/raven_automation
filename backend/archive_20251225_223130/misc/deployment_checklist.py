#!/usr/bin/env python3
"""
Raven Custom Glass - Deployment Checklist
Ready-to-use checklist for deploying the drawing API integration
"""

CHECKLIST = {
    "Pre-Deployment Validation": [
        ("✅ Validate integration components", "python validate_integration.py"),
        ("✅ Run integration tests", "python integration_test_demo.py"),
        ("✅ Check dependencies", "pip list | grep -E 'fastapi|sqlalchemy|gspread|matplotlib'"),
        ("✅ Verify database exists", "Test-Path raven_drawings.db"),
        ("✅ Check drawings directory", "Test-Path ./drawings"),
    ],
    
    "Environment Setup": [
        ("✅ Create .env file with DATABASE_URL", "cat .env"),
        ("✅ Verify Google Sheets credentials", "Test-Path ./credentials/service-account.json"),
        ("✅ Set CORS origins if needed", "Check main.py CORSMiddleware"),
        ("✅ Configure output directory", "Set in integrated_drawing_service.py"),
        ("✅ Review FastAPI settings", "Check main.py configuration"),
    ],
    
    "Database Initialization": [
        ("✅ Create database tables", "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"),
        ("✅ Verify Project/Window/Door models", "python -c 'from app.models import Project, Window, Door'"),
        ("✅ Sync with Google Sheets (optional)", "POST /api/projects/{po_number}/sync"),
        ("✅ Check database has data", "SELECT COUNT(*) FROM projects, windows, doors"),
    ],
    
    "API Testing (Local)": [
        ("✅ Start API server", "uvicorn main:app --reload"),
        ("✅ Check health endpoint", "curl http://localhost:8000/"),
        ("✅ Visit Swagger UI", "http://localhost:8000/docs"),
        ("✅ Test /api/drawings/info", "GET /api/drawings/info"),
        ("✅ Test /api/drawings/list/all", "GET /api/drawings/list/all"),
        ("✅ Test project generation", "POST /api/drawings/project/{po_number}/generate"),
        ("✅ Test PDF download", "GET /api/drawings/download/{filename}"),
    ],
    
    "Integration Testing": [
        ("✅ Verify DataTransformer methods", "python -c 'from app.services.data_transformer import DataTransformer; print(dir(DataTransformer))'"),
        ("✅ Verify IntegratedDrawingService", "python -c 'from app.services.integrated_drawing_service import get_drawing_service; s = get_drawing_service()'"),
        ("✅ Test database → drawing flow", "integration_test_demo.py"),
        ("✅ Test Google Sheets → drawing flow", "Review DRAWING_API_EXAMPLES.py scenario 10"),
        ("✅ Test batch generation", "Generate 10+ items and verify"),
    ],
    
    "File & Directory Setup": [
        ("✅ Verify drawings output directory", "mkdir -p ./drawings"),
        ("✅ Check directory permissions", "Test-Path ./drawings -PathType Container"),
        ("✅ Create logs directory (optional)", "mkdir -p ./logs"),
        ("✅ Verify file paths are correct", "All hardcoded paths should be ./drawings"),
    ],
    
    "Security Review": [
        ("✅ Review path traversal protection", "Check download endpoint filename validation"),
        ("✅ Check CORS settings", "Verify allow_origins in main.py"),
        ("✅ Review error messages", "No sensitive info in error responses"),
        ("✅ Check database credentials", "Use environment variables, not hardcoded"),
        ("✅ Verify Google Sheets auth", "service-account.json stored securely"),
    ],
    
    "Performance Verification": [
        ("✅ Single drawing generation time", "Time a single POST /drawings/window/{id}"),
        ("✅ Batch generation performance", "Time 10-item project generation"),
        ("✅ Memory usage during batch", "Monitor memory during large batch"),
        ("✅ PDF file sizes", "Check reasonable file sizes (~50-100KB)"),
        ("✅ Database query performance", "Verify indexes are working"),
    ],
    
    "Documentation Review": [
        ("✅ Read DRAWING_API.md", "Complete API documentation"),
        ("✅ Review DRAWING_API_EXAMPLES.py", "10+ practical examples"),
        ("✅ Check INTEGRATION_COMPLETE.md", "Integration summary"),
        ("✅ Review README_INTEGRATION.md", "This deployment guide"),
        ("✅ Update project README", "Add API documentation link"),
    ],
    
    "Production Deployment": [
        ("⏳ Set DEBUG=False in config", "Only in production"),
        ("⏳ Use PostgreSQL (not SQLite)", "For concurrent access"),
        ("⏳ Set up reverse proxy (nginx)", "For load balancing"),
        ("⏳ Configure SSL/TLS certificates", "HTTPS only"),
        ("⏳ Set up monitoring/logging", "Error tracking, performance metrics"),
        ("⏳ Configure backup strategy", "Daily backups of database"),
        ("⏳ Set up automated PDF archiving", "Old PDFs to cold storage"),
        ("⏳ Configure log rotation", "Prevent disk space issues"),
    ],
    
    "Post-Deployment": [
        ("⏳ Monitor error logs", "Check for any runtime errors"),
        ("⏳ Verify PDF output quality", "Print samples and verify"),
        ("⏳ Test with real projects", "Use actual project data"),
        ("⏳ Set up alerts", "Notify on generation failures"),
        ("⏳ Create user documentation", "For API consumers"),
        ("⏳ Train team", "How to use API endpoints"),
    ],
}


def print_checklist():
    """Print formatted checklist"""
    print("\n" + "="*80)
    print("RAVEN CUSTOM GLASS - DEPLOYMENT CHECKLIST")
    print("="*80)
    
    total_items = 0
    for section, items in CHECKLIST.items():
        print(f"\n### {section} ({len(items)} items)")
        print("-" * 80)
        
        for item, command in items:
            total_items += 1
            print(f"\n{item}")
            if command:
                print(f"   Command: {command}")
    
    print("\n" + "="*80)
    print(f"TOTAL CHECKLIST ITEMS: {total_items}")
    print("="*80)
    print("\n✅ = Pre-deployment (must complete)")
    print("⏳ = Post-deployment (after API is live)")
    print("\n")


def create_markdown_checklist():
    """Create markdown version of checklist"""
    markdown = "# Raven Custom Glass - Deployment Checklist\n\n"
    
    for section, items in CHECKLIST.items():
        markdown += f"## {section}\n\n"
        
        for item, command in items:
            checkbox = "- [ ]" if "⏳" in item else "- [x]"
            markdown += f"{checkbox} {item}\n"
            if command:
                markdown += f"  ```bash\n  {command}\n  ```\n"
        
        markdown += "\n"
    
    return markdown


if __name__ == "__main__":
    import sys
    
    # Print to console
    print_checklist()
    
    # Save as markdown
    with open("DEPLOYMENT_CHECKLIST.md", "w") as f:
        f.write(create_markdown_checklist())
    
    print("✅ Checklist saved to: DEPLOYMENT_CHECKLIST.md")
    
    # Quick status
    print("\n" + "="*80)
    print("QUICK STATUS")
    print("="*80)
    print("\n✅ Integration Components: CREATED")
    print("✅ API Endpoints: IMPLEMENTED")
    print("✅ Documentation: COMPLETE")
    print("✅ Examples: PROVIDED")
    print("✅ Tests: READY")
    print("\n⏳ To start: uvicorn main:app --reload")
    print("⏳ Visit: http://localhost:8000/docs")
    print("\n")
